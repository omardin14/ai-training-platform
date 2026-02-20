"""
Knowledge Graphs with LangChain

This example demonstrates how to transform unstructured text into
structured knowledge graphs using LangChain's LLMGraphTransformer.

Topics covered:
- Loading documents from Wikipedia
- Splitting documents into chunks
- Extracting entities and relationships using an LLM
- Inspecting the resulting graph structure (nodes and edges)
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
    """Example: Build a knowledge graph from Wikipedia articles."""

    print("\n" + "=" * 70)
    print("Knowledge Graphs with LangChain")
    print("=" * 70)

    # Check for OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key or openai_api_key == "your-openai-api-key-here":
        print("\nError: OPENAI_API_KEY not found in environment variables.")
        print("   Please set your OpenAI API key in the .env file.")
        print("   Get your key from: https://platform.openai.com/api-keys")
        print("\n" + "=" * 70 + "\n")
        return

    # ========================================================================
    # STEP 1: Load and Split Documents
    # ========================================================================
    #
    # We load Wikipedia articles and split them into smaller chunks
    # for the LLM to process. Each chunk will be analyzed for entities
    # and relationships.
    #
    print("\n" + "-" * 70)
    print("Step 1: Loading and Splitting Documents")
    print("-" * 70)

    try:
        from langchain_community.document_loaders import WikipediaLoader
        from langchain_text_splitters import TokenTextSplitter
    except ImportError as e:
        print(f"\n  Missing dependency: {e}")
        print("  Install with: pip install wikipedia langchain-community")
        print("\n" + "=" * 70 + "\n")
        return

    print("\n  Loading Wikipedia articles about 'Machine Learning'...")
    raw_documents = WikipediaLoader(query="Machine Learning").load()
    print(f"  Loaded {len(raw_documents)} raw document(s)")

    # Split into manageable chunks
    text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=20)
    documents = text_splitter.split_documents(raw_documents[:3])

    print(f"  Split into {len(documents)} chunk(s)")
    print(f"\n  First chunk preview:")
    print(f"    {documents[0].page_content[:150]}...")

    # ========================================================================
    # STEP 2: Create the LLM Graph Transformer
    # ========================================================================
    #
    # The LLMGraphTransformer uses a language model to parse text and
    # extract structured graph data — identifying entities (nodes) and
    # the relationships (edges) between them.
    #
    print("\n" + "-" * 70)
    print("Step 2: Creating LLM Graph Transformer")
    print("-" * 70)

    try:
        from langchain_openai import ChatOpenAI
        from langchain_experimental.graph_transformers import LLMGraphTransformer
    except ImportError as e:
        print(f"\n  Missing dependency: {e}")
        print("  Install with: pip install langchain-experimental langchain-openai")
        print("\n" + "=" * 70 + "\n")
        return

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    llm_transformer = LLMGraphTransformer(llm=llm)
    print("\n  LLM Graph Transformer created (using gpt-4o-mini)")

    # ========================================================================
    # STEP 3: Transform Documents to Graph
    # ========================================================================
    #
    # The transformer analyzes each document chunk, identifies entities,
    # and infers relationships between them. The output is a list of
    # GraphDocument objects containing nodes and relationships.
    #
    print("\n" + "-" * 70)
    print("Step 3: Transforming Documents to Graph")
    print("-" * 70)

    print("\n  Converting documents to graph format...")
    print("  (This may take a moment as the LLM processes each chunk)")

    # Process a subset to keep the demo manageable
    graph_documents = llm_transformer.convert_to_graph_documents(documents[:5])

    print(f"\n  Converted {len(graph_documents)} document(s) to graph format")

    # ========================================================================
    # STEP 4: Inspect the Graph Structure
    # ========================================================================
    #
    # Each GraphDocument contains:
    # - nodes: entities extracted from the text (with id and type)
    # - relationships: connections between nodes (with source, target, type)
    #
    print("\n" + "-" * 70)
    print("Step 4: Inspecting the Graph Structure")
    print("-" * 70)

    total_nodes = 0
    total_relationships = 0

    for i, doc in enumerate(graph_documents):
        total_nodes += len(doc.nodes)
        total_relationships += len(doc.relationships)

    print(f"\n  Total nodes extracted: {total_nodes}")
    print(f"  Total relationships extracted: {total_relationships}")

    # Show sample nodes from the first document
    if graph_documents and graph_documents[0].nodes:
        print("\n  Sample Nodes:")
        for node in graph_documents[0].nodes[:5]:
            print(f"    Node(id='{node.id}', type='{node.type}')")

    # Show sample relationships from the first document
    if graph_documents and graph_documents[0].relationships:
        print("\n  Sample Relationships:")
        for rel in graph_documents[0].relationships[:5]:
            print(
                f"    {rel.source.id} --[{rel.type}]--> {rel.target.id}"
            )

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)

    print("\n  Knowledge Graph Pipeline:")
    print("    1. Load documents (WikipediaLoader)")
    print("    2. Split into chunks (TokenTextSplitter)")
    print("    3. Create transformer (LLMGraphTransformer)")
    print("    4. Extract graph (convert_to_graph_documents)")

    print("\n  Graph Components:")
    print("    - Nodes: entities with id and type (Person, Concept, Technology)")
    print("    - Edges: directional relationships between nodes (USES, CREATED)")
    print("    - Properties: key-value pairs on nodes and edges")

    print("\n  Next Steps:")
    print("    - Store the graph in Neo4j for querying")
    print("    - Combine with vector search for hybrid RAG")
    print("    - Use Cypher queries to traverse relationships")

    print("\n" + "=" * 70)
    print("Example completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
