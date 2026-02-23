"""LangChain Fundamentals course - module registry."""

from learn.content.loader import discover_modules

LANGCHAIN_MODULES = discover_modules(__name__, "courses/langchain-fundamentals")
