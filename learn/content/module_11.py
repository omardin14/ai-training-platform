"""Module 11: LCEL Retrieval Chain - Interactive lesson content."""

MODULE = {
    "id": "11",
    "title": "LCEL Retrieval Chain",
    "directory": "11-lcel-retrival-chain",
    "examples": ["retrieval_chain_example.py"],
    "quiz": [
        {
            "question": "What does LCEL stand for?",
            "choices": [
                "LangChain Expression Language",
                "Language Chain Execution Logic",
                "Linear Chain Expression Language",
            ],
            "answer": 0,
            "explanation": (
                "LCEL stands for LangChain Expression Language, a declarative "
                "way to compose chains."
            ),
        },
        {
            "question": (
                "What is the purpose of RunnablePassthrough in a retrieval "
                "chain?"
            ),
            "choices": [
                "To retrieve documents",
                "To pass values through unchanged",
                "To format prompts",
            ],
            "answer": 1,
            "explanation": (
                "RunnablePassthrough passes values through unchanged, acting "
                "as a placeholder that preserves the original input."
            ),
        },
        {
            "question": (
                "In a retrieval chain, what does the retriever do?"
            ),
            "choices": [
                "Generates the final answer",
                "Searches the vector database and returns relevant documents",
                "Formats the prompt",
            ],
            "answer": 1,
            "explanation": (
                "The retriever searches the vector database for relevant "
                "documents based on the user's question."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Retrieval chains",
        "hints": [
            "Look at retrieval_chain_example.py for reference",
            "The first XXXX___ should be an import (ChatPromptTemplate)",
            "The second XXXX___ should be a method name (from_messages)",
            "The third XXXX___ should be an import (RunnablePassthrough)",
            "The fourth XXXX___ should be a method name (invoke)",
        ],
    },
}
