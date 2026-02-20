"""
Challenge: Neo4j Graph Store & Cypher Queries

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Connecting to Neo4j with Neo4jGraph
- Storing graph documents in the database
- Querying the graph with Cypher
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

# Step 1: Connect to Neo4j
# Replace XXXX___ with the correct class (Neo4jGraph)
from langchain_neo4j import Neo4jGraph

graph = Neo4jGraph(url=neo4j_uri, username=neo4j_user, password=neo4j_password)
print("Connected to Neo4j")

# Step 2: Create graph documents (provided for you)
from langchain_community.document_loaders import WikipediaLoader
from langchain_text_splitters import TokenTextSplitter
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer

raw_documents = WikipediaLoader(query="Machine Learning").load()
text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=20)
documents = text_splitter.split_documents(raw_documents[:3])

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
llm_transformer = LLMGraphTransformer(llm=llm)
graph_documents = llm_transformer.convert_to_graph_documents(documents[:3])
print(f"Created {len(graph_documents)} graph document(s)")

# Step 3: Store graph documents in Neo4j
# Replace XXXX___ with the correct method (add_graph_documents)
# Replace XXXX___ with the correct parameter (include_source)
graph.add_graph_documents(
    graph_documents,
    include_source=True,
    baseEntityLabel=True
)
print("Graph documents stored in Neo4j")

# Step 4: View the schema
print("\nDatabase Schema:")
print(graph.get_schema)

# Step 5: Query with Cypher
# Replace XXXX___ with the correct Cypher clause (MATCH)
result = graph.query(
    "MATCH (n)-[r]->(m) RETURN n.id AS source, type(r) AS rel, m.id AS target LIMIT 5"
)

print("\nSample Relationships:")
for row in result:
    print(f"  {row['source']} --[{row['rel']}]--> {row['target']}")

print("\nChallenge completed!")
