"""Module 18: Graph RAG Chain - Interactive lesson content."""

MODULE = {
    "id": "18",
    "title": "Graph RAG Chain",
    "directory": "18-graph-rag-chain",
    "examples": ["graph_rag_chain_example.py"],
    "quiz": [
        {
            "question": "What does GraphCypherQAChain do?",
            "choices": [
                "Embeds user queries into vectors for similarity search",
                "Translates natural language questions into Cypher queries and returns natural language answers",
                "Stores graph documents in a Neo4j database",
            ],
            "answer": 1,
            "explanation": (
                "GraphCypherQAChain bridges natural language and graph databases. "
                "It takes a user's question, generates a Cypher query using the graph "
                "schema, executes it against Neo4j, and returns the result as a "
                "natural language response."
            ),
        },
        {
            "question": "What two sub-chains does GraphCypherQAChain consist of?",
            "choices": [
                "An embedding chain and a retrieval chain",
                "A generate Cypher chain and a summarize results chain",
                "A document loader chain and a text splitter chain",
            ],
            "answer": 1,
            "explanation": (
                "GraphCypherQAChain is composed of two sequential sub-chains: "
                "the generate Cypher chain (which translates the user's question "
                "into a Cypher query using the graph schema) and the summarize "
                "results chain (which converts the raw query results into a "
                "natural language response)."
            ),
        },
        {
            "question": "Why should you call refresh_schema() before querying?",
            "choices": [
                "It deletes old nodes that are no longer relevant",
                "It ensures the chain has the most up-to-date view of the graph structure",
                "It optimizes the database indexes for faster queries",
            ],
            "answer": 1,
            "explanation": (
                "Calling refresh_schema() updates the chain's view of the graph "
                "structure (node types, properties, relationships). This is especially "
                "important when the graph is being auto-populated, so the LLM has "
                "accurate schema information when generating Cypher queries."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Graph RAG chain with GraphCypherQAChain",
        "hints": [
            "Look at graph_rag_chain_example.py for reference",
            "The first XXXX___ is the method to refresh the schema (refresh_schema)",
            "The second XXXX___ is the chain class (GraphCypherQAChain)",
            "The third XXXX___ is the factory method to create the chain (from_llm)",
            "The fourth XXXX___ is the method to run the chain (invoke)",
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
            "Run 'make setup-neo4j' in the 18-graph-rag-chain/ directory",
            "This starts a Neo4j database using Docker",
            "Credentials are auto-configured (neo4j / langchain-training)",
        ],
        "make_target": "setup-neo4j",
        "module_dir": "18-graph-rag-chain",
    },
}
