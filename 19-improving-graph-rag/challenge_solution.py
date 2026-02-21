"""
Challenge Solution: Improving Graph RAG Architecture

This is the complete solution for the improving Graph RAG challenge.
"""

import os
import warnings
from dotenv import load_dotenv

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)

# Load environment variables
load_dotenv()

# Check for API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key or openai_api_key == "your-openai-api-key-here":
    print("Error: OPENAI_API_KEY not found. Please set it in .env file.")
    exit(1)

neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
neo4j_user = os.getenv("NEO4J_USERNAME", "neo4j")
neo4j_password = os.getenv("NEO4J_PASSWORD")

if not neo4j_password:
    print("Error: NEO4J_PASSWORD not found. Please set it in .env file.")
    exit(1)

# ============================================================================
# SOLUTION: Complete code
# ============================================================================

# Step 1: Connect to Neo4j
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_openai import ChatOpenAI

graph = Neo4jGraph(url=neo4j_uri, username=neo4j_user, password=neo4j_password)
graph.refresh_schema()
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
print("Connected to Neo4j")

# Step 2: Create a filtered chain
chain_filtered = GraphCypherQAChain.from_llm(
    graph=graph,
    llm=llm,
    exclude_types=["Concept"],
    verbose=True,
    allow_dangerous_requests=True
)
print("Filtered chain created")

# Step 3: Create a validated chain
chain_validated = GraphCypherQAChain.from_llm(
    graph=graph,
    llm=llm,
    verbose=True,
    validate_cypher=True,
    allow_dangerous_requests=True
)
print("Validated chain created")

# Step 4: Build a few-shot prompt
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

examples = [
    {
        "question": "How many technologies are in the graph?",
        "query": "MATCH (t:Technology) RETURN count(DISTINCT t) AS total",
    },
]

example_prompt = PromptTemplate.from_template(
    "User input: {question}\nCypher query: {query}"
)

cypher_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=(
        "You are a Neo4j expert. Given an input question, create a "
        "syntactically correct Cypher query to run.\n\n"
        "Here is the schema information\n{schema}.\n\n"
        "Below are examples of questions and their Cypher queries."
    ),
    suffix="User input: {question}\nCypher query: ",
    input_variables=["question"],
)

# Step 5: Create the final chain with few-shot prompt
chain_fewshot = GraphCypherQAChain.from_llm(
    graph=graph,
    llm=llm,
    cypher_prompt=cypher_prompt,
    verbose=True,
    validate_cypher=True,
    allow_dangerous_requests=True
)

result = chain_fewshot.invoke({"query": "What technologies are in the graph?"})
print(f"\nAnswer: {result['result']}")

print("\nChallenge completed!")
