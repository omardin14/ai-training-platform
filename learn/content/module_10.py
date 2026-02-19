"""Module 10: RAG Document Storage - Interactive lesson content."""

MODULE = {
    "id": "10",
    "title": "RAG Document Storage",
    "directory": "10-RAG-document-storage",
    "examples": ["document_storage_example.py"],
    "quiz": [
        {
            "question": (
                "What is the purpose of embeddings in vector databases?"
            ),
            "choices": [
                "To compress documents",
                "To convert text into numerical vectors that capture semantic meaning",
                "To encrypt documents",
            ],
            "answer": 1,
            "explanation": (
                "Embeddings convert text to numerical vectors that capture "
                "semantic meaning, enabling semantic search."
            ),
        },
        {
            "question": (
                "What is the main purpose of storing documents in a vector "
                "database?"
            ),
            "choices": [
                "To compress documents",
                "To enable semantic search and retrieval of similar documents",
                "To encrypt documents",
            ],
            "answer": 1,
            "explanation": (
                "Vector databases enable semantic search and retrieval of "
                "similar documents based on meaning."
            ),
        },
        {
            "question": "What is Chroma?",
            "choices": [
                "A programming language",
                "A vector database for storing embeddings",
                "A text editor",
            ],
            "answer": 1,
            "explanation": (
                "Chroma is a lightweight vector database used for storing "
                "and retrieving embeddings."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Document storage",
        "hints": [
            "Look at document_storage_example.py for reference",
            "The first XXXX___ should be an import (OpenAIEmbeddings or HuggingFaceEmbeddings)",
            "The second XXXX___ should be a class name (Chroma)",
            "The third XXXX___ should be a method name (from_documents)",
        ],
    },
}
