"""Module 19: Improving Graph RAG Architecture - Interactive lesson content."""

MODULE = {
    "id": "19",
    "title": "Improving Graph RAG Architecture",
    "directory": "19-improving-graph-rag",
    "examples": ["improving_graph_rag_example.py"],
    "quiz": [
        {
            "question": "What does the exclude_types parameter do in GraphCypherQAChain?",
            "choices": [
                "Deletes specified node types from the Neo4j database",
                "Removes specified node types from the schema the LLM sees when generating Cypher",
                "Prevents the LLM from returning results containing those node types",
            ],
            "answer": 1,
            "explanation": (
                "The exclude_types parameter filters the graph schema that the LLM "
                "receives, hiding specified node types and their relationships. This "
                "reduces the search space and helps the model generate more accurate "
                "Cypher queries. It does not delete anything from the database."
            ),
        },
        {
            "question": "What does validate_cypher=True fix in generated Cypher queries?",
            "choices": [
                "Incorrect relationship directions by checking them against the schema",
                "Spelling errors in node property names",
                "Missing RETURN clauses in the generated queries",
            ],
            "answer": 0,
            "explanation": (
                "The validate_cypher option detects nodes and relationships in the "
                "generated Cypher, determines relationship directions, checks them "
                "against the graph schema, and corrects any direction errors. LLMs "
                "commonly get relationship directions wrong in Cypher statements."
            ),
        },
        {
            "question": "What is the purpose of few-shot prompting in Graph RAG?",
            "choices": [
                "To limit the number of results returned from Neo4j",
                "To provide example question-to-Cypher pairs that guide the LLM's query generation",
                "To automatically populate the graph with sample data",
            ],
            "answer": 1,
            "explanation": (
                "Few-shot prompting provides the LLM with example pairs of user "
                "questions and their corresponding Cypher queries. This guides the "
                "model toward correct query patterns for your specific graph structure, "
                "improving performance on complex or domain-specific queries."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Improving Graph RAG with filtering, validation, and few-shot prompting",
        "hints": [
            "Look at improving_graph_rag_example.py for reference",
            "The first XXXX___ is the parameter to exclude node types (exclude_types)",
            "The second XXXX___ enables Cypher validation (validate_cypher)",
            "The third XXXX___ is the class for few-shot prompts (FewShotPromptTemplate)",
            "The fourth XXXX___ is the parameter for the prompt instructions (prefix)",
            "The fifth XXXX___ passes the custom prompt to the chain (cypher_prompt)",
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
            "Run 'make setup-neo4j' in the 19-improving-graph-rag/ directory",
            "This starts a Neo4j database using Docker",
            "Credentials are auto-configured (neo4j / langchain-training)",
        ],
        "make_target": "setup-neo4j",
        "module_dir": "19-improving-graph-rag",
    },
}
