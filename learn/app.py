"""Main application loop for the interactive learning tool."""

import sys

from learn.content import MODULES, get_module, load_pages
from learn.ui import (
    clear,
    console,
    module_menu,
    module_picker,
    run_examples,
    run_lesson,
    run_quiz,
    show_challenge,
)


def main():
    """Entry point: module picker -> module menu -> lesson/quiz/challenge."""
    try:
        while True:
            selected_id = module_picker(MODULES)

            if selected_id is None:
                clear()
                console.print("[bold]Thanks for learning! Goodbye.[/bold]\n")
                sys.exit(0)

            module = get_module(selected_id)

            if module is None:
                clear()
                console.print(
                    f"\n[bold yellow]Module {selected_id} not found.[/bold yellow]\n"
                )
                console.input("[dim]Press Enter to go back...[/dim]")
                continue

            # Module menu loop
            while True:
                action = module_menu(module["title"])

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
                        run_lesson(pages, module["title"])
                elif action == "quiz":
                    run_quiz(module["quiz"], module["title"])
                elif action == "challenge":
                    show_challenge(
                        module["challenge"],
                        module["title"],
                        module["directory"],
                    )
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
                        )

    except KeyboardInterrupt:
        clear()
        console.print("\n[bold]Goodbye![/bold]\n")
        sys.exit(0)
