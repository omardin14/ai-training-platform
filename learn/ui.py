"""Rich + InquirerPy rendering helpers for the interactive learning tool."""

import base64
import os
import random
import re
import subprocess
import sys

from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich import box
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from learn.parser import IMG_DELIM

# Optional: rich-pixels for fallback terminal image rendering
try:
    from rich_pixels import Pixels
    from PIL import Image

    _HAS_PIXELS = True
except ImportError:
    _HAS_PIXELS = False

console = Console()

# Pattern to parse image markers produced by the parser.
# Matches: \x00IMG[alt text](/absolute/path.png)\x00
_IMG_MARKER = re.compile(
    re.escape(IMG_DELIM) + r"IMG\[(.*?)\]\((.*?)\)" + re.escape(IMG_DELIM)
)

# Panel border (2) + padding 2 chars each side (2*2) = 6
_PANEL_OVERHEAD = 6

# Terminals that support the iTerm2 inline image protocol (full resolution).
_NATIVE_IMAGE_TERMINALS = {"iTerm.app", "iTerm2", "WezTerm"}

_IMAGE_NOTICE_SHOWN = False


def _terminal_supports_native_images():
    """Check if the terminal supports full-resolution inline images."""
    term_program = os.environ.get("TERM_PROGRAM", "")
    return term_program in _NATIVE_IMAGE_TERMINALS


def _draw_image_native(abs_path):
    """Render an image at full resolution using the iTerm2 inline image protocol.

    Supported by iTerm2 and WezTerm. Returns True on success.
    """
    if not os.path.isfile(abs_path):
        return False

    try:
        with open(abs_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")

        name_b64 = base64.b64encode(
            os.path.basename(abs_path).encode()
        ).decode("ascii")

        sys.stdout.write(
            f"\033]1337;File=name={name_b64};inline=1;width=auto:{data}\a\n"
        )
        sys.stdout.flush()
        return True
    except Exception:
        return False


def _render_image_pixels(abs_path, max_width):
    """Fallback: render image as colored half-blocks via rich-pixels.

    Returns a Pixels renderable or None.
    """
    if not _HAS_PIXELS or not os.path.isfile(abs_path):
        return None

    try:
        img = Image.open(abs_path)
        if img.mode != "RGBA":
            img = img.convert("RGBA")

        orig_w, orig_h = img.size
        if orig_w > max_width:
            scale = max_width / orig_w
            img = img.resize(
                (max_width, int(orig_h * scale)), Image.Resampling.LANCZOS
            )

        return Pixels.from_image(img)
    except Exception:
        return None


def _show_image_notice():
    """Show a one-time notice about image quality."""
    global _IMAGE_NOTICE_SHOWN
    if _IMAGE_NOTICE_SHOWN:
        return
    _IMAGE_NOTICE_SHOWN = True

    if not _terminal_supports_native_images():
        console.print(
            "\n[dim]  Note: Diagrams are rendered as low-res terminal art.\n"
            "  For full quality, use a terminal with inline image support:\n"
            "  - iTerm2 (recommended): https://iterm2.com\n"
            "  - WezTerm: https://wezfurlong.org/wezterm[/dim]"
        )


def _split_page_segments(raw_content):
    """Split page content on image markers into (type, value) segments."""
    parts = _IMG_MARKER.split(raw_content)
    segments = []
    i = 0
    while i < len(parts):
        if i % 3 == 0:
            text = parts[i].strip()
            if text:
                segments.append(("text", text))
        elif i % 3 == 1:
            alt = parts[i]
            path = parts[i + 1] if i + 1 < len(parts) else ""
            i += 1
            segments.append(("image", (alt, path)))
        i += 1
    return segments


def _build_page_content_fallback(raw_content):
    """Build page content using rich-pixels (for non-native terminals).

    Returns a Group renderable with Markdown + pixel art inside a Panel.
    """
    max_img_width = console.width - _PANEL_OVERHEAD
    parts = _IMG_MARKER.split(raw_content)

    renderables = []
    i = 0
    while i < len(parts):
        if i % 3 == 0:
            segment = parts[i].strip()
            if segment:
                renderables.append(Markdown(segment))
        elif i % 3 == 1:
            alt = parts[i]
            path = parts[i + 1] if i + 1 < len(parts) else ""
            i += 1

            img_renderable = _render_image_pixels(path, max_img_width)
            if img_renderable is not None:
                renderables.append(Text())
                renderables.append(img_renderable)
                renderables.append(Text(f"  {alt}", style="dim italic"))
                renderables.append(Text())
            else:
                renderables.append(
                    Text(f"  [Image: {alt}]", style="dim italic")
                )
        i += 1

    if not renderables:
        return Markdown(raw_content)
    return Group(*renderables)


def clear():
    # Print blank lines to push old content into scrollback consistently.
    # Using \033[2J (console.clear) is unreliable — some terminals preserve
    # scrollback, others don't, leading to inconsistent behavior.
    console.print("\n" * console.height)


def render_page(page, current, total, module_title):
    """Render a single lesson page inside a styled panel.

    Uses full-resolution native images in iTerm2/WezTerm.
    Falls back to rich-pixels (low-res) in other terminals.
    """
    clear()
    raw = page["content"]
    title = f"[bold]{module_title}[/bold] — Page {current}/{total}"
    subtitle = f"Page {current}/{total}"
    has_images = IMG_DELIM in raw

    if not has_images:
        # No images — single panel
        console.print(
            Panel(
                Markdown(raw),
                title=title,
                subtitle=subtitle,
                box=box.ROUNDED,
                padding=(1, 2),
            )
        )
        return

    if _terminal_supports_native_images():
        # iTerm2 / WezTerm — render text in panel, images natively between
        segments = _split_page_segments(raw)

        console.print(
            Panel(
                f"[bold]{module_title}[/bold] — Page {current}/{total}",
                box=box.ROUNDED,
                padding=(0, 2),
            )
        )

        for seg_type, seg_value in segments:
            if seg_type == "text":
                console.print()
                console.print(Markdown(seg_value))
            else:
                alt, path = seg_value
                console.print()
                if not _draw_image_native(path):
                    console.print(f"  [dim italic]\\[Image: {alt}][/dim italic]")
    else:
        # Fallback — rich-pixels inside panel
        content = _build_page_content_fallback(raw)
        console.print(
            Panel(
                content,
                title=title,
                subtitle=subtitle,
                box=box.ROUNDED,
                padding=(1, 2),
            )
        )
        _show_image_notice()


def wait_for_enter(message="Press Enter to continue..."):
    console.print()
    console.input(f"[dim]{message}[/dim]")


def run_lesson(pages, module_title):
    """Walk through lesson pages one at a time."""
    for i, page in enumerate(pages):
        render_page(page, i + 1, len(pages), module_title)
        if i < len(pages) - 1:
            wait_for_enter()
        else:
            console.print()
            console.print("[bold green]Lesson complete![/bold green]")
            wait_for_enter("Press Enter to return to menu...")


def run_quiz(questions, module_title):
    """Run an interactive quiz with arrow-key selection."""
    clear()
    score = 0
    total = len(questions)

    for i, q in enumerate(questions):
        clear()
        console.print(
            Panel(
                Markdown(q["question"]),
                title=f"[bold]Quiz: Question {i + 1} of {total}[/bold]",
                box=box.ROUNDED,
                padding=(1, 2),
            )
        )
        console.print()

        # Shuffle choices so the correct answer isn't always in the same position
        indexed_choices = list(enumerate(q["choices"]))
        random.shuffle(indexed_choices)

        choices = [
            Choice(value=orig_idx, name=text)
            for orig_idx, text in indexed_choices
        ]

        answer = inquirer.select(
            message="Your answer:",
            choices=choices,
            pointer=">>>",
        ).execute()

        console.print()
        if answer == q["answer"]:
            score += 1
            console.print(f"[bold green]  Correct![/bold green] {q['explanation']}")
        else:
            correct_text = q["choices"][q["answer"]]
            console.print(
                f"[bold red]  Incorrect.[/bold red] The correct answer is: {correct_text}"
            )
            console.print(f"  {q['explanation']}")

        wait_for_enter()

    # Show results
    clear()
    if score == total:
        grade = "[bold green]Perfect! You've mastered this topic![/bold green]"
    elif score >= total * 0.66:
        grade = "[bold yellow]Great job! Review the concepts you missed.[/bold yellow]"
    elif score >= total * 0.33:
        grade = "[bold yellow]Good start! Review the lesson and try again.[/bold yellow]"
    else:
        grade = "[bold]Keep learning! Review the lesson and examples.[/bold]"

    console.print(
        Panel(
            f"[bold]Score: {score}/{total}[/bold]\n\n{grade}",
            title=f"[bold]Quiz Results: {module_title}[/bold]",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )
    wait_for_enter("Press Enter to return to menu...")


def _get_project_root():
    """Resolve the project root (parent of learn/ package)."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _strip_comments(code):
    """Remove docstrings, full-line comments, and inline comments from code."""
    # Strip triple-quoted docstrings
    code = re.sub(r'""".*?"""', "", code, flags=re.DOTALL)
    code = re.sub(r"'''.*?'''", "", code, flags=re.DOTALL)
    # Strip comments (full-line and inline)
    code = re.sub(r"#.*", "", code)
    return code


def _check_placeholders(challenge_path):
    """Check if challenge file still has XXXX___ placeholders in code.

    Returns True if placeholders remain. Ignores placeholders in
    comments and docstrings (hint text).
    """
    with open(challenge_path, encoding="utf-8") as f:
        code = f.read()
    return "XXXX___" in _strip_comments(code)


def _validate_challenge(challenge, module_dir):
    """Validate the challenge solution inline."""
    project_root = _get_project_root()
    challenge_path = os.path.join(project_root, module_dir, challenge["file"])

    if not os.path.isfile(challenge_path):
        console.print(
            f"\n[bold red]  Error: {module_dir}/{challenge['file']} not found![/bold red]\n"
        )
        wait_for_enter()
        return

    console.print()

    if _check_placeholders(challenge_path):
        # Count remaining placeholders (in code only, not comments/docstrings)
        with open(challenge_path, encoding="utf-8") as f:
            code = _strip_comments(f.read())
        count = code.count("XXXX___")

        console.print(
            Panel(
                f"[bold yellow]INCOMPLETE[/bold yellow] -- "
                f"{count} placeholder{'s' if count != 1 else ''} remaining.\n\n"
                "Open the file in your editor and replace each "
                "[bold]XXXX___[/bold] with the correct code.",
                title="[bold yellow]Validation Result[/bold yellow]",
                box=box.ROUNDED,
                padding=(1, 2),
            )
        )
    else:
        console.print("[dim]  Running your solution...[/dim]\n")

        try:
            result = subprocess.run(
                [sys.executable, challenge["file"]],
                cwd=os.path.join(project_root, module_dir),
                capture_output=True,
                text=True,
                timeout=120,
            )
        except subprocess.TimeoutExpired:
            console.print(
                Panel(
                    "[bold red]TIMEOUT[/bold red] -- "
                    "Your solution took too long (>2 min).",
                    title="[bold red]Validation Result[/bold red]",
                    box=box.ROUNDED,
                    padding=(1, 2),
                )
            )
            wait_for_enter()
            return

        if result.returncode == 0:
            output = result.stdout.strip()
            console.print(
                Panel(
                    f"[bold green]PASSED[/bold green] -- Your solution works!\n\n"
                    f"[dim]{output}[/dim]" if output else
                    "[bold green]PASSED[/bold green] -- Your solution works!",
                    title="[bold green]Validation Result[/bold green]",
                    box=box.ROUNDED,
                    padding=(1, 2),
                )
            )
        else:
            error = result.stderr.strip() or result.stdout.strip()
            # Truncate long errors
            if len(error) > 800:
                error = error[:800] + "\n..."
            console.print(
                Panel(
                    f"[bold red]FAILED[/bold red] -- Your code has errors.\n\n"
                    f"```\n{error}\n```",
                    title="[bold red]Validation Result[/bold red]",
                    box=box.ROUNDED,
                    padding=(1, 2),
                )
            )

    wait_for_enter()


def _reset_challenge(challenge, module_dir):
    """Reset challenge file back to XXXX___ placeholders using git."""
    project_root = _get_project_root()
    challenge_rel = os.path.join(module_dir, challenge["file"])
    challenge_path = os.path.join(project_root, challenge_rel)

    if not os.path.isfile(challenge_path):
        console.print(
            f"\n[bold red]  Error: {challenge_rel} not found![/bold red]\n"
        )
        wait_for_enter()
        return

    # Check if already has placeholders
    if _check_placeholders(challenge_path):
        console.print(
            "\n[dim]  Challenge already has XXXX___ placeholders. Nothing to reset.[/dim]"
        )
        wait_for_enter()
        return

    try:
        result = subprocess.run(
            ["git", "checkout", "--", challenge_rel],
            cwd=project_root,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            console.print(
                "\n[bold green]  Challenge reset to original placeholders.[/bold green]"
            )
        else:
            console.print(
                f"\n[bold red]  Reset failed: {result.stderr.strip()}[/bold red]"
            )
    except FileNotFoundError:
        console.print(
            "\n[bold red]  Error: git not found. Cannot reset.[/bold red]"
        )

    wait_for_enter()


def show_challenge(challenge, module_title, module_dir, setup_config=None):
    """Show challenge instructions with validate option."""
    while True:
        clear()

        # Show setup warning if external dependency is not configured
        if setup_config and not _check_setup(setup_config):
            name = setup_config["name"]
            instructions = setup_config.get("instructions", [])
            steps = "\n".join(f"  {i + 1}. {s}" for i, s in enumerate(instructions))
            console.print(
                Panel(
                    f"[bold]{name}[/bold] is not configured. The challenge will "
                    f"fail without it.\n\n"
                    f"[bold]To set up:[/bold]\n{steps}\n\n"
                    f"[dim]Go back and select [bold]Setup {name}[/bold] from the "
                    f"module menu, or set up manually.[/dim]",
                    title=f"[bold yellow]Setup Required[/bold yellow]",
                    box=box.ROUNDED,
                    padding=(1, 2),
                )
            )
            console.print()

        hints_text = "\n".join(
            f"  {i + 1}. {h}" for i, h in enumerate(challenge["hints"])
        )

        content = f"""\
**File:** `{module_dir}/{challenge['file']}`
**Topic:** {challenge['topic']}

### Instructions

1. Open `{module_dir}/{challenge['file']}` in your editor
2. Replace each `XXXX___` placeholder with the correct code
3. Select **Validate Solution** below to test

### Hints

{hints_text}

### Need more help?

- Look at the example files in `{module_dir}/` for reference
- Check `challenge_solution.py` if you're completely stuck
"""

        console.print(
            Panel(
                Markdown(content),
                title=f"[bold]Coding Challenge: {module_title}[/bold]",
                box=box.ROUNDED,
                padding=(1, 2),
            )
        )
        console.print()

        action = inquirer.select(
            message="Challenge:",
            choices=[
                Choice(value="validate", name="Validate Solution"),
                Choice(value="reset", name="Reset Challenge"),
                Separator(),
                Choice(value="back", name="Back to Menu"),
            ],
            pointer=">>>",
        ).execute()

        if action == "back":
            break
        elif action == "validate":
            _validate_challenge(challenge, module_dir)
        elif action == "reset":
            _reset_challenge(challenge, module_dir)


def run_examples(examples, module_title, module_dir):
    """Run example scripts from within the learn tool."""
    project_root = _get_project_root()
    cwd = os.path.join(project_root, module_dir)

    # If multiple examples, let the user pick; otherwise run the only one
    if len(examples) > 1:
        clear()
        console.print(
            Panel(
                f"[bold]{module_title}[/bold] has {len(examples)} example scripts.",
                title="[bold]Run Examples[/bold]",
                box=box.ROUNDED,
                padding=(1, 2),
            )
        )
        console.print()

        choices = [
            Choice(value=ex, name=ex) for ex in examples
        ]
        choices.append(Separator())
        choices.append(Choice(value=None, name="Back"))

        selected = inquirer.select(
            message="Select an example to run:",
            choices=choices,
            pointer=">>>",
        ).execute()

        if selected is None:
            return
        scripts = [selected]
    else:
        scripts = examples

    for script in scripts:
        script_path = os.path.join(cwd, script)
        if not os.path.isfile(script_path):
            console.print(f"\n[bold red]  Error: {script} not found![/bold red]\n")
            wait_for_enter()
            return

        clear()
        console.print(
            Panel(
                f"Running [bold]{script}[/bold]...",
                title=f"[bold]{module_title}[/bold]",
                box=box.ROUNDED,
                padding=(1, 2),
            )
        )
        console.print()

        result = subprocess.run(
            [sys.executable, script],
            cwd=cwd,
            timeout=120,
        )

        console.print()
        if result.returncode == 0:
            console.print("[bold green]  Example finished successfully.[/bold green]")
        else:
            console.print("[bold red]  Example exited with errors.[/bold red]")

        wait_for_enter()


def module_picker(modules):
    """Show the main module selection menu. Returns a module dict or None to quit."""
    clear()
    console.print(
        Panel(
            "[bold]Welcome to the LangChain Training Course![/bold]\n\n"
            "Select a module to start learning.",
            title="[bold]LangChain Training[/bold]",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )
    console.print()

    choices = []
    for m in modules:
        choices.append(Choice(value=m["id"], name=f"{m['id']} - {m['title']}"))
    choices.append(Choice(value=None, name="Quit"))

    selected = inquirer.fuzzy(
        message="Select a module (type to filter):",
        choices=choices,
        pointer=">>>",
    ).execute()

    return selected


def _write_env_values(env_values):
    """Write environment variables to the project's .env file.

    Skips keys that are already present. Updates os.environ so the
    running process picks up the changes immediately.
    """
    project_root = _get_project_root()
    env_path = os.path.join(project_root, ".env")

    # Read existing .env content
    existing = ""
    if os.path.isfile(env_path):
        with open(env_path, encoding="utf-8") as f:
            existing = f.read()

    # Determine which keys need to be added
    to_add = {}
    for key, value in env_values.items():
        # Check if key is already defined (as KEY= at start of line)
        if re.search(rf"^{re.escape(key)}\s*=", existing, re.MULTILINE):
            continue
        to_add[key] = value

    if not to_add:
        console.print(f"\n[dim]  Credentials already in .env file.[/dim]")
        return

    # Append new values
    lines = []
    if existing and not existing.endswith("\n"):
        lines.append("")  # ensure newline before our block
    for key, value in to_add.items():
        lines.append(f"{key}={value}")
        # Also set in current process so checks pass immediately
        os.environ[key] = value

    with open(env_path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    added = ", ".join(to_add.keys())
    console.print(f"\n[green]  Added to .env: {added}[/green]")


def _check_setup(setup_config):
    """Check if a module's external dependencies are configured.

    Returns True if all required env vars are set.
    """
    if not setup_config:
        return True
    env_vars = setup_config.get("check", {}).get("env_vars", [])
    return all(os.environ.get(v) for v in env_vars)


def show_setup_notice(setup_config):
    """Show a notice panel about required external setup."""
    if not setup_config or _check_setup(setup_config):
        return

    name = setup_config["name"]
    instructions = setup_config.get("instructions", [])
    steps = "\n".join(f"  {i + 1}. {s}" for i, s in enumerate(instructions))

    console.print(
        Panel(
            f"This module requires [bold]{name}[/bold] to run the "
            f"challenge and examples.\n\n"
            f"[bold]To set up:[/bold]\n{steps}\n\n"
            f"[dim]Select [bold]Setup {name}[/bold] from the menu below, "
            f"or set up manually.[/dim]",
            title=f"[bold yellow]Setup Required: {name}[/bold yellow]",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )


def run_setup(setup_config):
    """Run the setup make target for a module's external dependency."""
    if not setup_config:
        return

    name = setup_config["name"]
    make_target = setup_config.get("make_target")
    module_dir = setup_config.get("module_dir")

    if not make_target or not module_dir:
        console.print(f"\n[bold red]  No setup target configured for {name}.[/bold red]\n")
        wait_for_enter()
        return

    clear()
    console.print(
        Panel(
            f"Setting up [bold]{name}[/bold]...\n\n"
            f"Running [dim]make {make_target}[/dim] in [dim]{module_dir}/[/dim]",
            title=f"[bold]Setup: {name}[/bold]",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )
    console.print()

    project_root = _get_project_root()
    cwd = os.path.join(project_root, module_dir)

    result = subprocess.run(
        ["make", make_target],
        cwd=cwd,
        timeout=120,
    )

    console.print()
    if result.returncode == 0:
        console.print(f"[bold green]  {name} setup completed![/bold green]")

        # Auto-write credentials to .env
        env_values = setup_config.get("env_values", {})
        if env_values:
            _write_env_values(env_values)
    else:
        console.print(f"[bold red]  {name} setup had errors. Check the output above.[/bold red]")

    wait_for_enter()


def module_menu(module_title, setup_config=None):
    """Show the menu for a selected module. Returns the chosen action."""
    console.print()

    choices = [
        Choice(value="lesson", name="Start Lesson"),
        Choice(value="quiz", name="Take Quiz"),
        Choice(value="challenge", name="Coding Challenge"),
        Choice(value="examples", name="Run Examples"),
    ]

    if setup_config:
        name = setup_config["name"]
        status = "[dim](configured)[/dim]" if _check_setup(setup_config) else ""
        choices.append(
            Choice(value="setup", name=f"Setup {name}")
        )

    choices.append(Separator())
    choices.append(Choice(value="back", name="Back to Modules"))

    action = inquirer.select(
        message=f"{module_title}:",
        choices=choices,
        pointer=">>>",
    ).execute()

    return action
