"""Module 16: Knowledge Graphs - Interactive lesson content."""

MODULE = {
    "id": "16",
    "title": "Knowledge Graphs",
    "directory": "16-knowledge-graphs",
    "examples": ["knowledge_graph_example.py"],
    "quiz": [
        {
            "question": "What is a key limitation of vector store RAG that knowledge graphs address?",
            "choices": [
                "Vector stores cannot store any text data",
                "Vector stores struggle to capture relationships between entities",
                "Vector stores require a GPU to operate",
            ],
            "answer": 1,
            "explanation": (
                "Vector embeddings capture semantic meaning but struggle to represent "
                "themes and relationships between entities across a document corpus. "
                "Knowledge graphs model these relationships natively using nodes and edges."
            ),
        },
        {
            "question": "In a knowledge graph, what do edges represent?",
            "choices": [
                "The properties of a single entity",
                "The raw text content of a document",
                "Directional relationships between entities",
            ],
            "answer": 2,
            "explanation": (
                "Edges (relationships) are directional connections between nodes. "
                "They have a label describing the relationship type, and they go "
                "from a source node to a target node."
            ),
        },
        {
            "question": "What does LLMGraphTransformer do?",
            "choices": [
                "Converts vector embeddings into graph embeddings",
                "Uses an LLM to extract entities and relationships from text",
                "Translates Cypher queries into SQL queries",
            ],
            "answer": 1,
            "explanation": (
                "LLMGraphTransformer uses a language model to parse unstructured "
                "text, identify entities (nodes), and infer relationships (edges) "
                "between them, producing structured GraphDocument objects."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Knowledge graphs with LLMGraphTransformer",
        "hints": [
            "Look at knowledge_graph_example.py for reference",
            "The first XXXX___ is the Wikipedia loader class (WikipediaLoader)",
            "The second XXXX___ uses the same class to load documents",
            "The third XXXX___ is the text splitter class (TokenTextSplitter)",
            "The fourth XXXX___ is the graph transformer class (LLMGraphTransformer)",
            "The fifth XXXX___ is the method that converts documents to graphs",
        ],
    },
}
