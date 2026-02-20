"""
Graph RAG Chain

This example demonstrates how to build a natural language question-answering
system over a Neo4j knowledge graph using GraphCypherQAChain.

Topics covered:
- Populating a Neo4j graph with extracted knowledge
- Using GraphCypherQAChain to translate questions into Cypher
- Querying the graph with natural language
- Customizing the chain with validation and result limits
"""

import os
import warnings
from dotenv import load_dotenv

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)

# Load environment variables from .env file
load_dotenv()


def main():
    """Example: Query a knowledge graph using natural language."""

    print("\n" + "=" * 70)
    print("Graph RAG Chain")
    print("=" * 70)

    # Check for OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key or openai_api_key == "your-openai-api-key-here":
        print("\nError: OPENAI_API_KEY not found in environment variables.")
        print("   Please set your OpenAI API key in the .env file.")
        print("   Get your key from: https://platform.openai.com/api-keys")
        print("\n" + "=" * 70 + "\n")
        return

    # Check for Neo4j credentials
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USERNAME", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD")

    if not neo4j_password:
        print("\nError: NEO4J_PASSWORD not found in environment variables.")
        print("   Please set your Neo4j credentials in the .env file:")
        print("     NEO4J_URI=bolt://localhost:7687")
        print("     NEO4J_USERNAME=neo4j")
        print("     NEO4J_PASSWORD=your-neo4j-password")
        print("\n   Run 'make setup-neo4j' to start a local Neo4j instance.")
        print("\n" + "=" * 70 + "\n")
        return

    # ========================================================================
    # STEP 1: Connect to Neo4j
    # ========================================================================
    #
    # Connect to the Neo4j database using credentials from environment
    # variables. This is the same graph we populated in Module 17.
    #
    print("\n" + "-" * 70)
    print("Step 1: Connecting to Neo4j")
    print("-" * 70)

    try:
        from langchain_neo4j import Neo4jGraph
    except ImportError as e:
        print(f"\n  Missing dependency: {e}")
        print("  Install with: pip install langchain-neo4j neo4j")
        print("\n" + "=" * 70 + "\n")
        return

    try:
        graph = Neo4jGraph(
            url=neo4j_uri,
            username=neo4j_user,
            password=neo4j_password
        )
        print(f"\n  Connected to Neo4j at {neo4j_uri}")
    except Exception as e:
        print(f"\n  Failed to connect to Neo4j: {e}")
        print("  Make sure Neo4j is running and credentials are correct.")
        print("\n" + "=" * 70 + "\n")
        return

    # ========================================================================
    # STEP 2: Populate the Graph (if empty)
    # ========================================================================
    #
    # Check if the graph already has data from Module 17. If not, populate
    # it by extracting knowledge from Wikipedia articles.
    #
    print("\n" + "-" * 70)
    print("Step 2: Checking Graph Data")
    print("-" * 70)

    try:
        from langchain_community.document_loaders import WikipediaLoader
        from langchain_text_splitters import TokenTextSplitter
        from langchain_openai import ChatOpenAI
        from langchain_experimental.graph_transformers import LLMGraphTransformer
    except ImportError as e:
        print(f"\n  Missing dependency: {e}")
        print("  Install with: pip install wikipedia langchain-experimental langchain-openai")
        print("\n" + "=" * 70 + "\n")
        return

    # Check if graph already has entities
    entity_count = graph.query(
        "MATCH (n:__Entity__) RETURN count(n) AS count"
    )
    count = entity_count[0]["count"] if entity_count else 0

    if count > 0:
        print(f"\n  Graph already has {count} entities. Skipping population.")
    else:
        print("\n  Graph is empty. Populating with Wikipedia data...")
        print("  Loading articles about 'Machine Learning'...")
        raw_documents = WikipediaLoader(query="Machine Learning").load()
        print(f"  Loaded {len(raw_documents)} raw document(s)")

        text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=20)
        documents = text_splitter.split_documents(raw_documents[:3])
        print(f"  Split into {len(documents)} chunk(s)")

        llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
        llm_transformer = LLMGraphTransformer(llm=llm)

        print("  Extracting entities and relationships...")
        print("  (This may take a moment as the LLM processes each chunk)")
        graph_documents = llm_transformer.convert_to_graph_documents(documents[:5])

        graph.add_graph_documents(
            graph_documents,
            include_source=True,
            baseEntityLabel=True
        )
        total_nodes = sum(len(doc.nodes) for doc in graph_documents)
        total_rels = sum(len(doc.relationships) for doc in graph_documents)
        print(f"  Stored {total_nodes} nodes and {total_rels} relationships")

    # ========================================================================
    # STEP 3: Refresh the Schema
    # ========================================================================
    #
    # Refresh the schema to ensure we have the latest graph structure.
    # This is important when the graph has been recently populated.
    #
    print("\n" + "-" * 70)
    print("Step 3: Refreshing the Graph Schema")
    print("-" * 70)

    graph.refresh_schema()
    schema = graph.get_schema
    print(f"\n  Current Schema:")
    for line in schema.strip().split("\n"):
        print(f"    {line}")

    # ========================================================================
    # STEP 4: Create the Graph RAG Chain
    # ========================================================================
    #
    # GraphCypherQAChain translates natural language questions into Cypher
    # queries, executes them, and returns answers in natural language.
    # It uses two sub-chains: one for Cypher generation, one for summarization.
    #
    print("\n" + "-" * 70)
    print("Step 4: Creating the Graph RAG Chain")
    print("-" * 70)

    try:
        from langchain_neo4j import GraphCypherQAChain
    except ImportError as e:
        print(f"\n  Missing dependency: {e}")
        print("  Install with: pip install langchain-neo4j")
        print("\n" + "=" * 70 + "\n")
        return

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=True,
        top_k=10,
        allow_dangerous_requests=True
    )
    print("\n  GraphCypherQAChain created!")
    print("  - verbose=True: Will show generated Cypher and raw results")
    print("  - top_k=10: Limits results to 10 rows")

    # ========================================================================
    # STEP 5: Ask Questions in Natural Language
    # ========================================================================
    #
    # The chain handles the full pipeline: inspect schema, generate Cypher,
    # execute query, and summarize the results.
    #
    print("\n" + "-" * 70)
    print("Step 5: Querying with Natural Language")
    print("-" * 70)

    # Query 1: Explore relationships
    print("\n  Query 1: 'What entities are related to machine learning?'")
    print("  " + "-" * 50)
    try:
        result = chain.invoke({"query": "What entities are related to machine learning?"})
        print(f"\n  Answer: {result['result']}")
    except Exception as e:
        print(f"  Error: {e}")

    # Query 2: Find specific connections
    print("\n  Query 2: 'What types of entities exist in the graph?'")
    print("  " + "-" * 50)
    try:
        result = chain.invoke({"query": "What types of entities exist in the graph?"})
        print(f"\n  Answer: {result['result']}")
    except Exception as e:
        print(f"  Error: {e}")

    # Query 3: Multi-hop reasoning
    print("\n  Query 3: 'How many relationships are in the graph?'")
    print("  " + "-" * 50)
    try:
        result = chain.invoke({"query": "How many relationships are in the graph?"})
        print(f"\n  Answer: {result['result']}")
    except Exception as e:
        print(f"  Error: {e}")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)

    print("\n  Graph RAG Chain Pipeline:")
    print("    1. Connect to Neo4j (Neo4jGraph)")
    print("    2. Populate graph with knowledge (LLMGraphTransformer)")
    print("    3. Refresh schema (refresh_schema)")
    print("    4. Create chain (GraphCypherQAChain.from_llm)")
    print("    5. Query in natural language (chain.invoke)")

    print("\n  How It Works:")
    print("    - User asks a question in natural language")
    print("    - Generate Cypher Chain: Translates question into Cypher")
    print("    - Cypher query executes against Neo4j")
    print("    - Summarize Results Chain: Formats results as natural language")

    print("\n  Key Parameters:")
    print("    - verbose: Show generated Cypher and raw results")
    print("    - top_k: Limit number of query results")
    print("    - validate_cypher: Check Cypher syntax before execution")
    print("    - cypher_llm / qa_llm: Use different models per sub-chain")

    print("\n" + "=" * 70)
    print("Example completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
