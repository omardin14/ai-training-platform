"""AI Theory & Foundations course - module registry."""

from learn.content.loader import discover_modules

AI_THEORY_MODULES = discover_modules(__name__, "courses/ai-theory")
