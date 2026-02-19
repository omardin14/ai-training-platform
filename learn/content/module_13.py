"""Module 13: Advanced Splitting - Interactive lesson content."""

MODULE = {
    "id": "13",
    "title": "Advanced Splitting",
    "directory": "13-advanced-splitting",
    "examples": ["advanced_splitting_example.py"],
    "quiz": [
        {
            "question": "What is a limitation of character-based text splitters?",
            "choices": [
                "They are too slow",
                "They don't consider context and may split related information",
                "They require API keys",
            ],
            "answer": 1,
            "explanation": (
                "Character splitters don't consider context. They split text at arbitrary "
                "character positions, potentially separating related information and "
                "lowering RAG application quality."
            ),
        },
        {
            "question": "In token-based splitting, what does chunk_size refer to?",
            "choices": [
                "Number of characters",
                "Number of words",
                "Number of tokens",
            ],
            "answer": 2,
            "explanation": (
                "In token-based splitting, chunk_size refers to the number of tokens. "
                "This ensures chunks fit within model context windows, unlike character-based "
                "splitting where token count is unpredictable."
            ),
        },
        {
            "question": "What does semantic splitting detect?",
            "choices": [
                "Character boundaries",
                "Shifts in semantic meaning",
                "Token boundaries",
            ],
            "answer": 1,
            "explanation": (
                "Semantic splitting detects shifts in semantic meaning using embeddings. "
                "It splits at natural topic transitions, keeping related information together "
                "for better retrieval quality."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Advanced splitting",
        "hints": [
            "Look at advanced_splitting_example.py for reference",
            "The first XXXX___ should be an import (tiktoken)",
            "The second XXXX___ should be a method name (encoding_for_model)",
            "The third XXXX___ should be an import (TokenTextSplitter)",
            "The fourth XXXX___ should be an import (OpenAIEmbeddings)",
            "The fifth XXXX___ should be an import (SemanticChunker)",
        ],
    },
}
