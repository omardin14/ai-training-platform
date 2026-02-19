"""Module 07: Custom Agent Tools - Interactive lesson content."""

MODULE = {
    "id": "07",
    "title": "Custom Agent Tools",
    "directory": "07-custom-agent-tools",
    "examples": ["custom_tool_example.py"],
    "quiz": [
        {
            "question": "What decorator is used to convert a function into a tool?",
            "choices": ["@tool", "@function", "@agent"],
            "answer": 0,
            "explanation": (
                "The @tool decorator from langchain_core.tools converts "
                "functions into tools that agents can use."
            ),
        },
        {
            "question": (
                "What is used by the LLM to decide when to call a custom tool?"
            ),
            "choices": [
                "The tool's name",
                "The tool's description (docstring)",
                "The tool's arguments",
            ],
            "answer": 1,
            "explanation": (
                "The tool's description (from the docstring) helps the LLM "
                "decide when to use the tool."
            ),
        },
        {
            "question": "What are the key attributes of a custom tool?",
            "choices": [
                "name, description, and args",
                "name, type, and value",
                "function, decorator, and result",
            ],
            "answer": 0,
            "explanation": (
                "Tools have name, description, and args attributes that "
                "the agent uses to understand and call the tool."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Custom tools",
        "hints": [
            "Look at custom_tool_example.py for reference",
            "The first XXXX___ should be an import (@tool decorator)",
            "The second XXXX___ should be the decorator name (@tool)",
            "The third XXXX___ should be an import (create_react_agent)",
            "The fourth XXXX___ should be a function name (create_react_agent)",
            "The fifth XXXX___ should be a method name (invoke)",
        ],
    },
}
