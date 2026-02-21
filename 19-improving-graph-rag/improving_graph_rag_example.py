"""
Improving Graph RAG Architecture

This example demonstrates three techniques to improve the reliability
of Graph RAG chains: filtering, Cypher validation, and few-shot prompting.

Topics covered:
- Filtering the graph schema with exclude_types
- Validating generated Cypher queries against the schema
- Using few-shot prompting to guide Cypher generation
- Combining all techniques for maximum reliability
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
    """Example: Improve Graph RAG with filtering, validation, and few-shot prompting."""

    print("\n" + "=" * 70)
    print("Improving Graph RAG Architecture")
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
    # STEP 1: Connect to Neo4j and Ensure Graph Has Data
    # ========================================================================
    print("\n" + "-" * 70)
    print("Step 1: Connecting to Neo4j")
    print("-" * 70)

    try:
        from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
        from langchain_openai import ChatOpenAI
    except ImportError as e:
        print(f"\n  Missing dependency: {e}")
        print("  Install with: pip install langchain-neo4j langchain-openai neo4j")
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

    # Check if graph has data
    entity_count = graph.query(
        "MATCH (n:__Entity__) RETURN count(n) AS count"
    )
    count = entity_count[0]["count"] if entity_count else 0

    if count == 0:
        print("\n  Graph is empty. Populating with Wikipedia data...")
        try:
            from langchain_community.document_loaders import WikipediaLoader
            from langchain_text_splitters import TokenTextSplitter
            from langchain_experimental.graph_transformers import LLMGraphTransformer
        except ImportError as e:
            print(f"\n  Missing dependency: {e}")
            print("\n" + "=" * 70 + "\n")
            return

        raw_documents = WikipediaLoader(query="Machine Learning").load()
        text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=20)
        documents = text_splitter.split_documents(raw_documents[:3])

        llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
        llm_transformer = LLMGraphTransformer(llm=llm)

        print("  Extracting entities and relationships...")
        graph_documents = llm_transformer.convert_to_graph_documents(documents[:5])
        graph.add_graph_documents(
            graph_documents,
            include_source=True,
            baseEntityLabel=True
        )
        total_nodes = sum(len(doc.nodes) for doc in graph_documents)
        print(f"  Stored {total_nodes} nodes in Neo4j")
    else:
        print(f"\n  Graph has {count} entities. Ready to query.")

    # Refresh schema
    graph.refresh_schema()
    print(f"\n  Current Schema:")
    for line in graph.get_schema.strip().split("\n")[:15]:
        print(f"    {line}")

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    # ========================================================================
    # STEP 2: Technique 1 — Filtering with exclude_types
    # ========================================================================
    #
    # Exclude irrelevant node types from the schema to reduce confusion
    # and improve query accuracy.
    #
    print("\n" + "-" * 70)
    print("Step 2: Technique 1 — Filtering with exclude_types")
    print("-" * 70)

    chain_filtered = GraphCypherQAChain.from_llm(
        graph=graph,
        llm=llm,
        exclude_types=["Concept"],
        verbose=True,
        allow_dangerous_requests=True
    )
    print("\n  Created chain with exclude_types=['Concept']")
    print("  The LLM will not see Concept nodes or their relationships.")

    print("\n  Query: 'How many nodes are in the database?'")
    print("  " + "-" * 50)
    try:
        result = chain_filtered.invoke(
            {"query": "How many nodes are in the database?"}
        )
        print(f"\n  Answer: {result['result']}")
    except Exception as e:
        print(f"  Error: {e}")

    # ========================================================================
    # STEP 3: Technique 2 — Cypher Validation
    # ========================================================================
    #
    # Enable validate_cypher to automatically detect and fix incorrect
    # relationship directions in the generated Cypher.
    #
    print("\n" + "-" * 70)
    print("Step 3: Technique 2 — Cypher Validation")
    print("-" * 70)

    chain_validated = GraphCypherQAChain.from_llm(
        graph=graph,
        llm=llm,
        verbose=True,
        validate_cypher=True,
        allow_dangerous_requests=True
    )
    print("\n  Created chain with validate_cypher=True")
    print("  Relationship directions will be checked against the schema.")

    print("\n  Validation steps:")
    print("    1. Detects nodes and relationships in generated Cypher")
    print("    2. Determines the direction of each relationship")
    print("    3. Checks the graph schema for correct directions")
    print("    4. Updates relationship directions if needed")

    print("\n  Query: 'What are the names of all people in the graph?'")
    print("  " + "-" * 50)
    try:
        result = chain_validated.invoke(
            {"query": "What are the names of all people in the graph?"}
        )
        print(f"\n  Answer: {result['result']}")
    except Exception as e:
        print(f"  Error: {e}")

    # ========================================================================
    # STEP 4: Technique 3 — Few-Shot Prompting
    # ========================================================================
    #
    # Provide example question-to-Cypher pairs to guide the LLM toward
    # correct query patterns for our specific graph structure.
    #
    print("\n" + "-" * 70)
    print("Step 4: Technique 3 — Few-Shot Prompting")
    print("-" * 70)

    from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

    # Query the actual graph to build accurate few-shot examples
    sample_rels = graph.query(
        "MATCH (n)-[r]->(m) RETURN n.id AS src, type(r) AS rel, m.id AS tgt, "
        "labels(n) AS src_labels, labels(m) AS tgt_labels LIMIT 5"
    )

    # Define example question-Cypher pairs tailored to the actual graph
    # These examples teach the LLM the correct node labels and patterns
    examples = [
        {
            "question": "How many entities are in the graph?",
            "query": "MATCH (n:__Entity__) RETURN count(n) AS total",
        },
        {
            "question": "What types of entities exist and how many of each?",
            "query": "MATCH (n:__Entity__) RETURN labels(n) AS types, count(n) AS count ORDER BY count DESC",
        },
        {
            "question": "Show me all relationships between entities",
            "query": "MATCH (n:__Entity__)-[r]->(m:__Entity__) RETURN n.id, type(r), m.id LIMIT 10",
        },
    ]

    # Add a dynamic example if we found actual relationships
    if sample_rels:
        row = sample_rels[0]
        src_label = [l for l in row["src_labels"] if l != "__Entity__"][0] if row["src_labels"] else "Entity"
        tgt_label = [l for l in row["tgt_labels"] if l != "__Entity__"][0] if row["tgt_labels"] else "Entity"
        examples.append({
            "question": f"What {tgt_label.lower()} entities have a {row['rel']} relationship?",
            "query": f"MATCH (n:{src_label})-[:{row['rel']}]->(m:{tgt_label}) RETURN n.id, m.id LIMIT 10",
        })

    print(f"\n  Defined {len(examples)} example question-Cypher pairs")
    for i, ex in enumerate(examples):
        print(f"    {i+1}. \"{ex['question']}\"")

    # Create the example prompt template
    example_prompt = PromptTemplate.from_template(
        "User input: {question}\nCypher query: {query}"
    )

    # Build the few-shot prompt
    cypher_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix=(
            "You are a Neo4j expert. Given an input question, create a "
            "syntactically correct Cypher query to run.\n\n"
            "Here is the schema information\n{schema}.\n\n"
            "Below are a number of examples of questions and their "
            "corresponding Cypher queries."
        ),
        suffix="User input: {question}\nCypher query: ",
        input_variables=["question"],
    )
    print("  Built FewShotPromptTemplate with custom Cypher examples")

    # Create chain with few-shot prompt AND validation
    chain_fewshot = GraphCypherQAChain.from_llm(
        graph=graph,
        llm=llm,
        cypher_prompt=cypher_prompt,
        verbose=True,
        validate_cypher=True,
        allow_dangerous_requests=True
    )
    print("  Created chain with cypher_prompt + validate_cypher=True")

    print("\n  Query: 'How many entities are in the knowledge graph?'")
    print("  " + "-" * 50)
    try:
        result = chain_fewshot.invoke(
            {"query": "How many entities are in the knowledge graph?"}
        )
        print(f"\n  Answer: {result['result']}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n  Query: 'What types of entities exist and how many of each?'")
    print("  " + "-" * 50)
    try:
        result = chain_fewshot.invoke(
            {"query": "What types of entities exist and how many of each?"}
        )
        print(f"\n  Answer: {result['result']}")
    except Exception as e:
        print(f"  Error: {e}")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)

    print("\n  Three Techniques to Improve Graph RAG:")
    print("    1. Filtering (exclude_types): Reduce schema noise")
    print("    2. Cypher Validation (validate_cypher): Fix relationship directions")
    print("    3. Few-Shot Prompting (cypher_prompt): Guide query generation")

    print("\n  Best Practice — Combine All Three:")
    print("    chain = GraphCypherQAChain.from_llm(")
    print("        graph=graph, llm=llm,")
    print("        exclude_types=[...],       # Filter irrelevant nodes")
    print("        cypher_prompt=cypher_prompt, # Few-shot examples")
    print("        validate_cypher=True,       # Fix directions")
    print("    )")

    print("\n  When to Use Each Technique:")
    print("    - Filtering: Large graphs with irrelevant node types")
    print("    - Validation: Always — it's a low-cost safety net")
    print("    - Few-Shot: Complex or domain-specific query patterns")

    print("\n" + "=" * 70)
    print("Example completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
