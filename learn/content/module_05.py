"""Module 05: Sequential Chains - Interactive lesson content."""

MODULE = {
    "id": "05",
    "title": "Sequential Chains",
    "directory": "05-sequential-chain",
    "examples": ["sequential_chain_example.py"],
    "quiz": [
        {
            "question": (
                "What is the main purpose of StrOutputParser() "
                "in sequential chains?"
            ),
            "choices": [
                "To extract text from LLM responses so it can be used in the next chain",
                "To format the output nicely",
                "To reduce API costs",
            ],
            "answer": 0,
            "explanation": (
                "StrOutputParser() extracts text from LLM response objects "
                "so the output can be passed as a string to the next chain."
            ),
        },
        {
            "question": (
                "How do you pass the output of one chain "
                "to the next chain?"
            ),
            "choices": [
                "Using dictionary syntax like {'variable_name': chain}",
                "Using a list",
                "Using a tuple",
            ],
            "answer": 0,
            "explanation": (
                "Dictionary syntax like {'variable_name': chain} passes "
                "the output of one chain as a named variable to the next chain."
            ),
        },
        {
            "question": "What is the key advantage of sequential chains?",
            "choices": [
                "They make models run faster",
                "They reduce token usage",
                "They allow multi-step processing where each step builds on the previous",
            ],
            "answer": 2,
            "explanation": (
                "Sequential chains enable multi-step processing workflows "
                "where each step builds on the output of the previous step."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Sequential chains",
        "hints": [
            "The first XXXX___ should be imports (PromptTemplate, StrOutputParser)",
            "The second XXXX___ should be a class name (PromptTemplate)",
            "The third XXXX___ should be a method name (from_template)",
            "The fourth XXXX___ should be a class name (StrOutputParser)",
            "Remember to use StrOutputParser() with parentheses",
        ],
    },
}
