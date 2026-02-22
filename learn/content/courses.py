"""Course registry for the AI Training platform."""

from learn.content.langchain_fundamentals import LANGCHAIN_MODULES
from learn.content.langchain_agents import AGENTS_MODULES
from learn.content.ai_theory import AI_THEORY_MODULES
from learn.theme import register_course_theme

COURSES = [
    {
        "id": "ai-theory",
        "title": "AI Theory & Foundations",
        "description": "Machine learning, LLMs, alignment, prompt engineering, and AI safety.",
        "modules": AI_THEORY_MODULES,
        "status": "available",
        "color": "cyan",
        "art": r"""
        .---.
       / o o \    AI Theory
      |   <   |   & Foundations
       \ --- /
        '---'
""",
    },
    {
        "id": "langchain-fundamentals",
        "title": "Getting Started with LangChain",
        "description": "Learn LangChain from basics through RAG and knowledge graphs.",
        "modules": LANGCHAIN_MODULES,
        "status": "available",
        "color": "green",
        "art": r"""
      .-Chain-.
      |  <>  |    LangChain
      |--><--|    Fundamentals
      |  <>  |
      '-Chain-'
""",
    },
    {
        "id": "langchain-agents",
        "title": "LangChain Agents & LangGraph",
        "description": "Agent architectures, multi-agent systems, and LangGraph.",
        "modules": AGENTS_MODULES,
        "status": "available",
        "color": "magenta",
        "art": r"""
        [o_o]
       /| = |\    LangGraph
        | = |     Agents
       / \ / \
""",
    },
]

# Register each course's visual theme so theme.py can look it up by ID.
for _c in COURSES:
    register_course_theme(_c["id"], color=_c.get("color"), art=_c.get("art"))
