"""Main application loop for the interactive learning tool."""

import random
import sys

from rich.panel import Panel
from rich import box

from learn.content import COURSES, get_course, get_module, load_pages
from learn.progress import (
    load_progress,
    save_progress,
    update_streak,
    mark_lesson,
    mark_quiz,
    mark_challenge,
    get_module_progress,
)
from learn.theme import TIPS
from learn.ui import (
    clear,
    console,
    course_picker,
    module_menu,
    module_picker,
    run_examples,
    run_lesson,
    run_quiz,
    run_setup,
    show_challenge,
    show_lesson_toc,
    show_setup_notice,
)


def _show_session_summary(session):
    """Show a summary of what was accomplished in this session."""
    parts = []
    if session["lessons"]:
        n = session["lessons"]
        parts.append(f"{n} lesson{'s' if n != 1 else ''}")
    if session["quizzes"]:
        n = session["quizzes"]
        parts.append(f"{n} quiz{'zes' if n != 1 else ''}")
    if session["challenges"]:
        n = session["challenges"]
        parts.append(f"{n} challenge{'s' if n != 1 else ''}")

    clear()
    if parts:
        summary = "Completed: " + ", ".join(parts)
        console.print(
            Panel(
                f"[bold]{summary}[/bold]\n\nGreat work! See you next time.",
                title="[bold]Session Summary[/bold]",
                box=box.ROUNDED,
                padding=(1, 2),
            )
        )
    else:
        console.print("[bold]Thanks for learning! Goodbye.[/bold]\n")


def main():
    """Entry point: course picker -> module picker -> module menu -> actions."""
    progress = load_progress()
    streak = update_streak(progress)
    save_progress(progress)
    session = {"lessons": 0, "quizzes": 0, "challenges": 0}

    try:
        while True:
            # Course selection
            course_id = course_picker(COURSES, streak=streak)

            if course_id is None:
                _show_session_summary(session)
                sys.exit(0)

            course = get_course(course_id)
            if course is None:
                continue

            if course["status"] == "coming_soon":
                clear()
                console.print(
                    Panel(
                        f"[bold]{course['title']}[/bold]\n\n"
                        f"{course['description']}\n\n"
                        "This course is currently in development. "
                        "Check back soon!",
                        title="[bold yellow]Coming Soon[/bold yellow]",
                        box=box.ROUNDED,
                        padding=(1, 2),
                    )
                )
                console.input("\n[dim]Press Enter to go back...[/dim]")
                continue

            # Module selection loop (within a course)
            while True:
                selected_id = module_picker(
                    course["modules"],
                    course["title"],
                    course_id=course["id"],
                    progress=progress,
                )

                if selected_id is None:
                    break  # back to course picker

                module = get_module(course, selected_id)

                if module is None:
                    clear()
                    console.print(
                        f"\n[bold yellow]Module {selected_id} not found.[/bold yellow]\n"
                    )
                    console.input("[dim]Press Enter to go back...[/dim]")
                    continue

                setup_config = module.get("setup")

                # Show one-time setup notice when entering a module with dependencies
                show_setup_notice(setup_config)

                # Module menu loop
                while True:
                    mod_progress = get_module_progress(
                        progress, course["id"], module["id"]
                    )
                    action = module_menu(
                        module["title"],
                        setup_config=setup_config,
                        has_challenge="challenge" in module,
                        has_examples=bool(module.get("examples")),
                        course_id=course["id"],
                        mod_progress=mod_progress,
                    )

                    if action == "back":
                        break
                    elif action == "lesson":
                        pages = load_pages(module)
                        if not pages:
                            clear()
                            console.print(
                                "\n[bold yellow]No lesson markers found in this "
                                "module's README.md yet.[/bold yellow]\n"
                            )
                            console.input("[dim]Press Enter to go back...[/dim]")
                        else:
                            show_lesson_toc(
                                pages, module["title"],
                                course_id=course["id"],
                            )
                            run_lesson(
                                pages, module["title"],
                                course_id=course["id"],
                            )
                            mark_lesson(progress, course["id"], module["id"])
                            save_progress(progress)
                            session["lessons"] += 1
                    elif action == "quiz":
                        score, total = run_quiz(
                            module["quiz"], module["title"],
                            course_id=course["id"],
                        )
                        mark_quiz(
                            progress, course["id"], module["id"], score, total
                        )
                        save_progress(progress)
                        session["quizzes"] += 1
                    elif action == "challenge":
                        passed = show_challenge(
                            module["challenge"],
                            module["title"],
                            module["directory"],
                            setup_config=setup_config,
                            course_id=course["id"],
                        )
                        if passed:
                            mark_challenge(
                                progress, course["id"], module["id"]
                            )
                            save_progress(progress)
                        session["challenges"] += 1
                    elif action == "examples":
                        examples = module.get("examples", [])
                        if not examples:
                            clear()
                            console.print(
                                "\n[bold yellow]No example scripts configured "
                                "for this module.[/bold yellow]\n"
                            )
                            console.input("[dim]Press Enter to go back...[/dim]")
                        else:
                            run_examples(
                                examples,
                                module["title"],
                                module["directory"],
                                course_id=course["id"],
                            )
                    elif action == "setup":
                        run_setup(setup_config)

                    # F12: Random tip after non-back actions
                    if action != "back":
                        console.print(
                            f"\n  [dim italic]{random.choice(TIPS)}[/dim italic]\n"
                        )

    except KeyboardInterrupt:
        _show_session_summary(session)
        sys.exit(0)
