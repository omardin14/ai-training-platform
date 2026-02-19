"""Rich + InquirerPy rendering helpers for the interactive learning tool."""

import os
import random
import re
import subprocess
import sys

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich import box
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

console = Console()


def clear():
    # Print blank lines to push old content into scrollback consistently.
    # Using \033[2J (console.clear) is unreliable — some terminals preserve
    # scrollback, others don't, leading to inconsistent behavior.
    console.print("\n" * console.height)


def render_page(page, current, total, module_title):
    """Render a single lesson page inside a styled panel."""
    clear()
    content = Markdown(page["content"])
    console.print(
        Panel(
            content,
            title=f"[bold]{module_title}[/bold] — Page {current}/{total}",
            subtitle=f"Page {current}/{total}",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )


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


def show_challenge(challenge, module_title, module_dir):
    """Show challenge instructions with validate option."""
    while True:
        clear()
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
    choices.append(Separator())
    choices.append(Choice(value=None, name="Quit"))

    selected = inquirer.select(
        message="Select a module:",
        choices=choices,
        pointer=">>>",
    ).execute()

    return selected


def module_menu(module_title):
    """Show the menu for a selected module. Returns the chosen action."""
    console.print()
    action = inquirer.select(
        message=f"{module_title}:",
        choices=[
            Choice(value="lesson", name="Start Lesson"),
            Choice(value="quiz", name="Take Quiz"),
            Choice(value="challenge", name="Coding Challenge"),
            Choice(value="examples", name="Run Examples"),
            Separator(),
            Choice(value="back", name="Back to Modules"),
        ],
        pointer=">>>",
    ).execute()

    return action
