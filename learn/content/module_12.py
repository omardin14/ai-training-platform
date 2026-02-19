"""Module 12: RAG with Python & Markdown - Interactive lesson content."""

MODULE = {
    "id": "12",
    "title": "RAG with Python & Markdown",
    "directory": "12-RAG-python-markdown",
    "examples": ["python_markdown_example.py"],
    "quiz": [
        {
            "question": "What loader is used to load Markdown files?",
            "choices": [
                "MarkdownLoader",
                "TextLoader",
                "UnstructuredMarkdownLoader",
            ],
            "answer": 2,
            "explanation": (
                "UnstructuredMarkdownLoader is the correct loader for Markdown files. "
                "It preserves Markdown structure including headers, lists, and code blocks."
            ),
        },
        {
            "question": "What is the best way to split Python code files?",
            "choices": [
                "CharacterTextSplitter",
                "Simple split by lines",
                "RecursiveCharacterTextSplitter.from_language(Language.PYTHON)",
            ],
            "answer": 2,
            "explanation": (
                "RecursiveCharacterTextSplitter.from_language() is designed for code files. "
                "It splits at appropriate boundaries like functions and classes, "
                "preserving code structure."
            ),
        },
        {
            "question": "What loader is used to load Python source files?",
            "choices": [
                "PythonFileLoader",
                "CodeLoader",
                "PythonLoader",
            ],
            "answer": 2,
            "explanation": (
                "PythonLoader is the correct class for loading Python source files "
                "into LangChain documents."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Markdown and Python loaders",
        "hints": [
            "Look at python_markdown_example.py for reference",
            "The first XXXX___ should be an import (UnstructuredMarkdownLoader)",
            "The second XXXX___ should be a method name (load)",
            "The third XXXX___ should be an import (PythonLoader)",
            "The fourth XXXX___ should be an import (RecursiveCharacterTextSplitter)",
            "The fifth XXXX___ should be an import (Language)",
            "The sixth XXXX___ should be a method name (from_language)",
            "The seventh XXXX___ should be Language.PYTHON",
        ],
    },
}
