"""
Challenge: Improving Graph RAG Architecture

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Filtering the graph schema with exclude_types
- Validating generated Cypher queries
- Building a few-shot prompt for Cypher generation
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
# CHALLENGE: Complete the code below
# ============================================================================

# Step 1: Connect to Neo4j (provided for you)
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_openai import ChatOpenAI

graph = Neo4jGraph(url=neo4j_uri, username=neo4j_user, password=neo4j_password)
graph.refresh_schema()
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
print("Connected to Neo4j")

# Step 2: Create a filtered chain
# Replace XXXX___ with the correct parameter to exclude node types (exclude_types)
chain_filtered = GraphCypherQAChain.from_llm(
    graph=graph,
    llm=llm,
    XXXX___=["Concept"],
    verbose=True,
    allow_dangerous_requests=True
)
print("Filtered chain created")

# Step 3: Create a validated chain
# Replace XXXX___ with the parameter to enable Cypher validation (validate_cypher)
chain_validated = GraphCypherQAChain.from_llm(
    graph=graph,
    llm=llm,
    verbose=True,
    XXXX___=True,
    allow_dangerous_requests=True
)
print("Validated chain created")

# Step 4: Build a few-shot prompt
# Replace XXXX___ with the correct class (FewShotPromptTemplate)
from langchain_core.prompts import XXXX___, PromptTemplate

examples = [
    {
        "question": "How many entities are in the graph?",
        "query": "MATCH (n:__Entity__) RETURN count(n) AS total",
    },
    {
        "question": "What types of entities exist and how many of each?",
        "query": "MATCH (n:__Entity__) RETURN labels(n) AS types, count(n) AS count ORDER BY count DESC",
    },
]

example_prompt = PromptTemplate.from_template(
    "User input: {question}\nCypher query: {query}"
)

# Replace XXXX___ with the correct parameter for the prompt prefix (prefix)
cypher_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    XXXX___=(
        "You are a Neo4j expert. Given an input question, create a "
        "syntactically correct Cypher query to run.\n\n"
        "Here is the schema information\n{schema}.\n\n"
        "Below are examples of questions and their Cypher queries."
    ),
    suffix="User input: {question}\nCypher query: ",
    input_variables=["question"],
)

# Step 5: Create the final chain with few-shot prompt
# Replace XXXX___ with the parameter to pass the custom prompt (cypher_prompt)
chain_fewshot = GraphCypherQAChain.from_llm(
    graph=graph,
    llm=llm,
    XXXX___=cypher_prompt,
    verbose=True,
    validate_cypher=True,
    allow_dangerous_requests=True
)

result = chain_fewshot.invoke({"query": "How many entities are in the graph?"})
print(f"\nAnswer: {result['result']}")

print("\nChallenge completed!")
