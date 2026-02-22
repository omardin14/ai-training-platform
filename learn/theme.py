"""Visual theming: ASCII art, course colors, tips, and shortcut text."""

# ── F1: Welcome Banner ───────────────────────────────────────────

WELCOME_BANNER = r"""
    _    ___   _____ ____      _    ___ _   _ ___ _   _  ____
   / \  |_ _| |_   _|  _ \   / \  |_ _| \ | |_ _| \ | |/ ___|
  / _ \  | |    | | | |_) | / _ \  | ||  \| || ||  \| | |  _
 / ___ \ | |    | | |  _ < / ___ \ | || |\  || || |\  | |_| |
/_/   \_\___|   |_| |_| \_/_/   \_\___|_| \_|___|_| \_|\____|
"""

# ── F2: Course Header Art ────────────────────────────────────────
# Art and colors are registered by each course in courses.py at import time.
# This keeps theme.py as a low-level utility with no content imports.

_COURSE_ART = {}
_COURSE_COLORS = {}

_DEFAULT_COLOR = "blue"

DEFAULT_ART = r"""
      .---.
     / o o \    AI Training
    |   ^   |   Platform
     \ --- /
      '---'
"""


def register_course_theme(course_id, color=None, art=None):
    """Register a course's visual theme (called from courses.py)."""
    if color:
        _COURSE_COLORS[course_id] = color
    if art:
        _COURSE_ART[course_id] = art


def get_course_color(course_id):
    """Return the Rich color string for a course."""
    return _COURSE_COLORS.get(course_id, _DEFAULT_COLOR)


def get_course_art(course_id):
    """Return the ASCII art header for a course."""
    return _COURSE_ART.get(course_id, DEFAULT_ART)


# ── F11: Keyboard Shortcut Hints ─────────────────────────────────

SHORTCUTS = {
    "course_picker": "[dim]  [Enter] Select  [Ctrl+C] Quit[/dim]",
    "module_picker": "[dim]  [Enter] Select  [Type] Filter  [Ctrl+C] Quit[/dim]",
    "module_menu": "[dim]  [Enter] Select  [Ctrl+C] Quit[/dim]",
    "lesson": "[dim]  [Enter] Next Page  [Ctrl+C] Quit[/dim]",
    "quiz": "[dim]  [Enter] Confirm Answer  [Ctrl+C] Quit[/dim]",
    "challenge": "[dim]  [Enter] Select  [Ctrl+C] Quit[/dim]",
}

# ── F12: Tips and Encouragement ──────────────────────────────────

TIPS = [
    "Tip: Use the flipped prompt when you're stuck -- ask the AI what it needs from you.",
    "Did you know? ReAct combines reasoning and acting for better agent decision-making.",
    "Tip: RAG systems work best when documents are split at natural boundaries.",
    "Tip: Always test prompts with edge cases before deploying to production.",
    "Did you know? LangChain's LCEL lets you compose chains using the | operator.",
    "Tip: Knowledge graphs capture relationships that vector search alone can miss.",
    "Tip: Few-shot prompting can dramatically improve output quality with just 2-3 examples.",
    "Did you know? Agents use tool descriptions to decide which tool to call.",
    "Tip: Set temperature to 0 for deterministic outputs, higher for creative tasks.",
    "Tip: Chain-of-thought prompting helps models reason through multi-step problems.",
    "Did you know? LangGraph gives you fine-grained control over agent execution flow.",
    "Tip: Document your prompt templates -- future you will thank present you.",
    "Tip: Start with simple chains before building complex agent architectures.",
    "Did you know? Embedding models convert text into vectors for semantic search.",
    "Tip: Use streaming for long-running agent tasks to provide real-time feedback.",
    "Tip: Validate challenge solutions often -- small fixes are easier than big rewrites.",
    "Did you know? Neo4j's Cypher language is designed for pattern matching in graphs.",
    "Tip: Multi-agent systems work best with clearly defined roles and responsibilities.",
]
