"""Module 14: Advanced Retrieval - Interactive lesson content."""

MODULE = {
    "id": "14",
    "title": "Advanced Retrieval",
    "directory": "14-advanced-retrieval",
    "examples": ["advanced_retrieval_example.py"],
    "quiz": [
        {
            "question": "What is a characteristic of dense retrieval?",
            "choices": [
                "Vectors contain many zeros",
                "Excels at capturing semantic meaning",
                "Matches exact keywords only",
            ],
            "answer": 1,
            "explanation": (
                "Dense retrieval excels at capturing semantic meaning. "
                "Dense vectors have mostly non-zero values and encode the full "
                "semantic content of text, enabling conceptual matching."
            ),
        },
        {
            "question": "What does BM25 stand for?",
            "choices": [
                "Best Matching 25",
                "Binary Matching 25",
                "Basic Matching 25",
            ],
            "answer": 0,
            "explanation": (
                "BM25 stands for Best Matching 25. It is an improvement on TF-IDF "
                "that prevents high-frequency words from being over-emphasized "
                "and includes length normalization."
            ),
        },
        {
            "question": "What is an advantage of sparse retrieval?",
            "choices": [
                "Better at semantic similarity",
                "More explainable due to alignment with specific terms",
                "Less computationally intensive",
            ],
            "answer": 1,
            "explanation": (
                "Sparse retrieval is more explainable because results align directly "
                "with specific terms, making it easy to understand why documents "
                "were retrieved."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Advanced retrieval",
        "hints": [
            "Look at advanced_retrieval_example.py for reference",
            "The first XXXX___ should be an import (BM25Retriever)",
            "The second XXXX___ should be a method name (from_texts)",
            "The third XXXX___ should be a method name (invoke)",
        ],
    },
}
