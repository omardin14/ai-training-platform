"""Module 09: RAG Document Splitters - Interactive lesson content."""

MODULE = {
    "id": "09",
    "title": "RAG Document Splitters",
    "directory": "09-RAG-document-splitter",
    "examples": ["document_splitter_example.py"],
    "quiz": [
        {
            "question": (
                "What is the main difference between CharacterTextSplitter "
                "and RecursiveCharacterTextSplitter?"
            ),
            "choices": [
                "CharacterTextSplitter is faster",
                "RecursiveCharacterTextSplitter tries multiple separators in order",
                "They are the same thing",
            ],
            "answer": 1,
            "explanation": (
                "RecursiveCharacterTextSplitter tries multiple separators "
                "intelligently, working through the list to find the best "
                "splitting strategy."
            ),
        },
        {
            "question": (
                "What is the purpose of chunk_overlap in document splitting?"
            ),
            "choices": [
                "To make chunks smaller",
                "To prevent losing context at chunk boundaries",
                "To speed up processing",
            ],
            "answer": 1,
            "explanation": (
                "chunk_overlap maintains continuity between chunks by sharing "
                "characters at the boundaries, preventing context loss."
            ),
        },
        {
            "question": (
                "What is the difference between split_text() and "
                "split_documents()?"
            ),
            "choices": [
                "split_text() works with strings, split_documents() works with Document objects",
                "split_text() is faster",
                "There is no difference",
            ],
            "answer": 0,
            "explanation": (
                "split_text() returns strings, while split_documents() "
                "returns Document objects and preserves metadata."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Document splitters",
        "hints": [
            "Look at document_splitter_example.py for reference",
            "The first XXXX___ should be an import (RecursiveCharacterTextSplitter)",
            "The second XXXX___ should be a class name (RecursiveCharacterTextSplitter)",
            "The third XXXX___ should be a method name (split_documents)",
        ],
    },
}
