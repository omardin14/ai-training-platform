"""
Challenge: Graph RAG Chain

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Refreshing the graph schema
- Creating a GraphCypherQAChain
- Querying the graph with natural language
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
from langchain_neo4j import Neo4jGraph

graph = Neo4jGraph(url=neo4j_uri, username=neo4j_user, password=neo4j_password)
print("Connected to Neo4j")

# Step 2: Refresh the schema
# Replace XXXX___ with the correct method to refresh the schema
graph.XXXX___()
print("\nSchema refreshed")
print(graph.get_schema)

# Step 3: Create the Graph RAG Chain
# Replace XXXX___ with the correct class (GraphCypherQAChain)
from langchain_neo4j import XXXX___
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# Replace XXXX___ with the correct factory method (from_llm)
chain = GraphCypherQAChain.XXXX___(
    llm=llm,
    graph=graph,
    verbose=True,
    allow_dangerous_requests=True
)
print("GraphCypherQAChain created")

# Step 4: Query with natural language
# Replace XXXX___ with the correct method to run the chain (invoke)
result = chain.XXXX___({"query": "What entities are in the graph?"})
print(f"\nAnswer: {result['result']}")

print("\nChallenge completed!")
