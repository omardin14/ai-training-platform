"""Module 17: Neo4j Graph Store & Cypher Queries - Interactive lesson content."""

MODULE = {
    "id": "17",
    "title": "Neo4j Graph Store & Cypher Queries",
    "directory": "17-neo4j-graph-store",
    "examples": ["neo4j_graph_store_example.py"],
    "quiz": [
        {
            "question": "What does the include_source parameter do when adding graph documents to Neo4j?",
            "choices": [
                "It includes the Python source code as a node property",
                "It links nodes to their source documents via a MENTIONS relationship",
                "It saves the raw text content inside each node",
            ],
            "answer": 1,
            "explanation": (
                "Setting include_source=True links each extracted node to its "
                "source document by creating a MENTIONS relationship in the graph. "
                "This enables traceability from entities back to the original text."
            ),
        },
        {
            "question": "What is Cypher?",
            "choices": [
                "A Python library for encrypting database credentials",
                "A declarative query language for navigating and manipulating graph data",
                "A vector embedding algorithm used by Neo4j",
            ],
            "answer": 1,
            "explanation": (
                "Cypher is Neo4j's declarative query language, designed with a "
                "SQL-like syntax for intuitively navigating and manipulating "
                "graph data using pattern matching with MATCH and RETURN clauses."
            ),
        },
        {
            "question": "What does the baseEntityLabel parameter do?",
            "choices": [
                "Assigns an additional __Entity__ label to each node for better query performance",
                "Sets the default label for nodes that have no type",
                "Converts all node labels to lowercase for consistency",
            ],
            "answer": 0,
            "explanation": (
                "Setting baseEntityLabel=True assigns an additional __Entity__ "
                "label to every node in the graph. This allows you to query all "
                "entities regardless of their specific type (Person, Technology, etc.), "
                "improving query flexibility and performance."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Neo4j graph store and Cypher queries",
        "hints": [
            "Look at neo4j_graph_store_example.py for reference",
            "The first XXXX___ is the Neo4j graph class (Neo4jGraph)",
            "The second XXXX___ uses the same class to create a connection",
            "The third XXXX___ is the method to add graph documents (add_graph_documents)",
            "The fourth XXXX___ is the parameter for source linking (include_source)",
            "The fifth XXXX___ is the Cypher clause for pattern matching (MATCH)",
        ],
    },
    "setup": {
        "name": "Neo4j",
        "check": {
            "env_vars": ["NEO4J_PASSWORD"],
        },
        "env_values": {
            "NEO4J_URI": "bolt://localhost:7687",
            "NEO4J_USERNAME": "neo4j",
            "NEO4J_PASSWORD": "langchain-training",
        },
        "instructions": [
            "Run 'make setup-neo4j' in the 17-neo4j-graph-store/ directory",
            "This starts a Neo4j database using Docker",
            "Credentials are auto-configured (neo4j / langchain-training)",
        ],
        "make_target": "setup-neo4j",
        "module_dir": "17-neo4j-graph-store",
    },
}
