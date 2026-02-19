"""Module 01: LangChain Models - quiz and challenge config."""

MODULE = {
    "id": "01",
    "title": "LangChain Models",
    "directory": "01-langchain-models",
    "examples": ["openai_example.py", "huggingface_example.py"],
    "quiz": [
        {
            "question": "What method is used to send a prompt to a LangChain model?",
            "choices": [".call()", ".invoke()", ".run()"],
            "answer": 1,
            "explanation": (
                "The .invoke() method is the standard way to send prompts "
                "to any LangChain model, regardless of provider."
            ),
        },
        {
            "question": "Which class is used to load OpenAI chat models in LangChain?",
            "choices": ["OpenAI", "ChatOpenAI", "GPTModel"],
            "answer": 1,
            "explanation": (
                "ChatOpenAI is the class for OpenAI's chat models "
                "(like gpt-3.5-turbo and gpt-4)."
            ),
        },
        {
            "question": "What is a key advantage of using LangChain for models?",
            "choices": [
                "It provides a unified interface across different model providers",
                "It makes models run faster",
                "It reduces API costs",
            ],
            "answer": 0,
            "explanation": (
                "LangChain's main value is its unified interface -- "
                "you can swap providers by changing one class, "
                "while the rest of your code stays the same."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Loading and using models",
        "hints": [
            "The first XXXX___ should be a class name (ChatOpenAI)",
            "The second XXXX___ should be the same class name",
            "The third XXXX___ should be a method name (invoke)",
            "The fourth XXXX___ should be an attribute name (content)",
        ],
    },
}
