"""LangChain Agents course - module registry."""

from learn.content.loader import discover_modules

AGENTS_MODULES = discover_modules(__name__, "courses/langchain-agents")
