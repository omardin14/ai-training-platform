"""Module 02: Prompt Templates - Interactive lesson content."""

MODULE = {
    "id": "02",
    "title": "Prompt Templates",
    "directory": "02-prompt-templates",
    "examples": ["prompt_template_example.py"],
    "quiz": [
        {
            "question": (
                "What class is used to create prompt templates "
                "with system and human messages?"
            ),
            "choices": [
                "PromptTemplate",
                "ChatPromptTemplate",
                "MessageTemplate",
            ],
            "answer": 1,
            "explanation": (
                "ChatPromptTemplate is used for chat-style prompts "
                "with system and human messages."
            ),
        },
        {
            "question": "How do you fill in a variable in a prompt template?",
            "choices": [
                "Use .format() method",
                "Use .format_messages() method",
                "Use .fill() method",
            ],
            "answer": 1,
            "explanation": (
                ".format_messages() fills in variables "
                "in chat prompt templates."
            ),
        },
        {
            "question": (
                "What syntax is used to define a variable "
                "placeholder in a template?"
            ),
            "choices": [
                "{{variable_name}}",
                "{variable_name}",
                "[variable_name]",
            ],
            "answer": 1,
            "explanation": (
                "Variables use {variable_name} syntax "
                "with single curly braces."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Prompt templates",
        "hints": [
            "The first XXXX___ should be a class name (ChatPromptTemplate)",
            "The second XXXX___ should be a method name (from_messages)",
            "The third XXXX___ should be a method name (format_messages)",
        ],
    },
}
