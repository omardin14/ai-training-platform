"""
Neo4j Graph Store & Cypher Queries

This example demonstrates how to store knowledge graph documents
in a Neo4j database and query them using Cypher.

Topics covered:
- Connecting to a Neo4j database
- Storing graph documents extracted with LLMGraphTransformer
- Viewing the database schema
- Querying the graph with Cypher
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
    """Example: Store and query knowledge graphs in Neo4j."""

    print("\n" + "=" * 70)
    print("Neo4j Graph Store & Cypher Queries")
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
        print("\n   Download Neo4j Desktop: https://neo4j.com/download/")
        print("   Or use Neo4j Aura (cloud): https://neo4j.com/cloud/aura/")
        print("\n" + "=" * 70 + "\n")
        return

    # ========================================================================
    # STEP 1: Connect to Neo4j
    # ========================================================================
    #
    # We use LangChain's Neo4jGraph class to connect to a Neo4j instance.
    # The connection URL, username, and password are loaded from environment
    # variables for security.
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
    # STEP 2: Load and Transform Documents
    # ========================================================================
    #
    # We reuse the pattern from Module 16: load Wikipedia articles, split
    # them into chunks, and extract graph documents using LLMGraphTransformer.
    #
    print("\n" + "-" * 70)
    print("Step 2: Loading and Transforming Documents")
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

    print("\n  Loading Wikipedia articles about 'Machine Learning'...")
    raw_documents = WikipediaLoader(query="Machine Learning").load()
    print(f"  Loaded {len(raw_documents)} raw document(s)")

    # Split into manageable chunks
    text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=20)
    documents = text_splitter.split_documents(raw_documents[:3])
    print(f"  Split into {len(documents)} chunk(s)")

    # Create graph transformer
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    llm_transformer = LLMGraphTransformer(llm=llm)
    print("  LLM Graph Transformer created")

    # Transform documents to graph format
    print("\n  Converting documents to graph format...")
    print("  (This may take a moment as the LLM processes each chunk)")
    graph_documents = llm_transformer.convert_to_graph_documents(documents[:5])
    print(f"  Converted {len(graph_documents)} document(s) to graph format")

    total_nodes = sum(len(doc.nodes) for doc in graph_documents)
    total_rels = sum(len(doc.relationships) for doc in graph_documents)
    print(f"  Total nodes: {total_nodes}, Total relationships: {total_rels}")

    # ========================================================================
    # STEP 3: Store Graph Documents in Neo4j
    # ========================================================================
    #
    # We store the extracted graph documents in Neo4j using
    # .add_graph_documents(). The include_source parameter links nodes
    # to their source documents, and baseEntityLabel adds an __Entity__
    # label for better query performance.
    #
    print("\n" + "-" * 70)
    print("Step 3: Storing Graph Documents in Neo4j")
    print("-" * 70)

    try:
        graph.add_graph_documents(
            graph_documents,
            include_source=True,
            baseEntityLabel=True
        )
        print("\n  Graph documents stored in Neo4j!")
        print("  - include_source=True: Nodes linked to source docs via MENTIONS")
        print("  - baseEntityLabel=True: All nodes have __Entity__ label")
    except Exception as e:
        print(f"\n  Error storing documents: {e}")
        print("\n" + "=" * 70 + "\n")
        return

    # ========================================================================
    # STEP 4: View the Database Schema
    # ========================================================================
    #
    # The .get_schema attribute shows the graph structure: node types,
    # relationship types, and their directions.
    #
    print("\n" + "-" * 70)
    print("Step 4: Viewing the Database Schema")
    print("-" * 70)

    schema = graph.get_schema
    print(f"\n  Database Schema:")
    for line in schema.strip().split("\n"):
        print(f"    {line}")

    # ========================================================================
    # STEP 5: Query with Cypher
    # ========================================================================
    #
    # We use Cypher queries to traverse the graph and find relationships
    # between entities.
    #
    print("\n" + "-" * 70)
    print("Step 5: Querying with Cypher")
    print("-" * 70)

    # Query 1: Find all entity types and their counts
    print("\n  Query 1: Entity types and counts")
    try:
        result = graph.query(
            "MATCH (n:__Entity__) RETURN labels(n) AS types, count(n) AS count ORDER BY count DESC LIMIT 10"
        )
        for row in result:
            print(f"    {row['types']}: {row['count']}")
    except Exception as e:
        print(f"    Error: {e}")

    # Query 2: Find relationships from a specific entity
    print("\n  Query 2: Sample relationships")
    try:
        result = graph.query(
            "MATCH (n)-[r]->(m) RETURN n.id AS source, type(r) AS relationship, m.id AS target LIMIT 10"
        )
        for row in result:
            print(f"    {row['source']} --[{row['relationship']}]--> {row['target']}")
    except Exception as e:
        print(f"    Error: {e}")

    # Query 3: Find source documents (from include_source=True)
    print("\n  Query 3: Source document traceability")
    try:
        result = graph.query(
            "MATCH (n:__Entity__)-[:MENTIONS]-(d:Document) RETURN n.id AS entity, count(d) AS sources LIMIT 5"
        )
        for row in result:
            print(f"    Entity '{row['entity']}' found in {row['sources']} source document(s)")
    except Exception as e:
        print(f"    Error: {e}")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)

    print("\n  Neo4j Graph Store Pipeline:")
    print("    1. Connect to Neo4j (Neo4jGraph)")
    print("    2. Extract graph documents (LLMGraphTransformer)")
    print("    3. Store in database (add_graph_documents)")
    print("    4. View schema (get_schema)")
    print("    5. Query with Cypher (MATCH / RETURN)")

    print("\n  Key Parameters:")
    print("    - include_source: Links entities to source documents")
    print("    - baseEntityLabel: Adds __Entity__ label for easier querying")

    print("\n  Next Steps:")
    print("    - Build graph-based RAG chains using Neo4j as the retriever")
    print("    - Combine graph retrieval with vector search for hybrid RAG")
    print("    - Explore more advanced Cypher queries for multi-hop reasoning")

    print("\n" + "=" * 70)
    print("Example completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
