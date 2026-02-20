"""Module 15: RAG Evaluation - Interactive lesson content."""

MODULE = {
    "id": "15",
    "title": "RAG Evaluation",
    "directory": "15-rag-evaluation",
    "examples": ["rag_evaluation_example.py"],
    "quiz": [
        {
            "question": "What does the faithfulness metric measure?",
            "choices": [
                "Whether the generated output represents retrieved documents well",
                "The speed of the RAG system",
                "How relevant retrieved documents are",
            ],
            "answer": 0,
            "explanation": (
                "Faithfulness measures whether the generated output represents "
                "the retrieved documents well. It calculates the ratio of faithful "
                "claims that can be derived from the context."
            ),
        },
        {
            "question": "What does context precision measure?",
            "choices": [
                "How relevant the retrieved documents are to the query",
                "The length of the generated answer",
                "How fast documents are retrieved",
            ],
            "answer": 0,
            "explanation": (
                "Context precision measures how relevant the retrieved documents "
                "are to the query. A score closer to 1.0 means the retrieved "
                "context is highly relevant."
            ),
        },
        {
            "question": "What is RAGAS?",
            "choices": [
                "A RAG database system",
                "A language model",
                "A framework for evaluating RAG applications",
            ],
            "answer": 2,
            "explanation": (
                "RAGAS (RAG Assessment) is a framework designed to evaluate both "
                "the retrieval and generation components of a RAG application, "
                "providing specialized metrics like faithfulness and context precision."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "RAG evaluation",
        "hints": [
            "Look at rag_evaluation_example.py for reference",
            "The first two XXXX___ are for PromptTemplate (import and usage)",
            "Use ragas.evaluate(), EvaluationDataset, and SingleTurnSample",
            "Wrap the LangChain LLM with LangchainLLMWrapper for RAGAS",
            "The Faithfulness metric class is in ragas.metrics._faithfulness",
        ],
    },
}
