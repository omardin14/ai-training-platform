"""
Challenge Solution: Graph RAG Chain

This is the complete solution for the Graph RAG Chain challenge.
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
from langchain_neo4j import Neo4jGraph

graph = Neo4jGraph(url=neo4j_uri, username=neo4j_user, password=neo4j_password)
print("Connected to Neo4j")

# Step 2: Refresh the schema
graph.refresh_schema()
print("\nSchema refreshed")
print(graph.get_schema)

# Step 3: Create the Graph RAG Chain
from langchain_neo4j import GraphCypherQAChain
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    allow_dangerous_requests=True
)
print("GraphCypherQAChain created")

# Step 4: Query with natural language
result = chain.invoke({"query": "What entities are in the graph?"})
print(f"\nAnswer: {result['result']}")

print("\nChallenge completed!")
