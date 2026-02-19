"""Module 08: RAG Document Loaders - Interactive lesson content."""

MODULE = {
    "id": "08",
    "title": "RAG Document Loaders",
    "directory": "08-RAG-document-loader",
    "examples": ["document_loader_example.py"],
    "quiz": [
        {
            "question": "What does a document loader return?",
            "choices": [
                "A list of Document objects with page_content and metadata",
                "A string containing the file content",
                "A dictionary with file information",
            ],
            "answer": 0,
            "explanation": (
                "Document loaders return Document objects with content "
                "and metadata."
            ),
        },
        {
            "question": "Which loader would you use for a PDF file?",
            "choices": ["TextLoader", "PyPDFLoader", "CSVLoader"],
            "answer": 1,
            "explanation": "PyPDFLoader is used for PDF files.",
        },
        {
            "question": (
                "What is the main purpose of document loaders in RAG "
                "applications?"
            ),
            "choices": [
                "To train models on new data",
                "To extract text content from files for retrieval and generation",
                "To compress documents",
            ],
            "answer": 1,
            "explanation": (
                "Document loaders extract text from files so it can be used "
                "for retrieval and generation in RAG applications."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Document loaders",
        "hints": [
            "Look at document_loader_example.py for reference",
            "The first XXXX___ should be an import (PyPDFLoader)",
            "The second XXXX___ should be a class name (PyPDFLoader)",
            "The third XXXX___ should be a method name (load)",
        ],
    },
}
