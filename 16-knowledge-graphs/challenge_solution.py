"""
Challenge Solution: Knowledge Graphs

This is the complete solution for the knowledge graphs challenge.
"""

import os
import warnings
from dotenv import load_dotenv

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)

# Load environment variables
load_dotenv()

# Check for API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key or openai_api_key == "your-openai-api-key-here":
    print("Error: OPENAI_API_KEY not found. Please set it in .env file.")
    exit(1)

# ============================================================================
# SOLUTION: Complete code
# ============================================================================

# Step 1: Load documents from Wikipedia
from langchain_community.document_loaders import WikipediaLoader

raw_documents = WikipediaLoader(query="Machine Learning").load()
print(f"Loaded {len(raw_documents)} document(s)")

# Step 2: Split documents into chunks
from langchain_text_splitters import TokenTextSplitter

text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=20)
documents = text_splitter.split_documents(raw_documents[:3])
print(f"Split into {len(documents)} chunk(s)")

# Step 3: Create the LLM and graph transformer
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
llm_transformer = LLMGraphTransformer(llm=llm)
print("Graph transformer created")

# Step 4: Convert documents to graph format
graph_documents = llm_transformer.convert_to_graph_documents(documents[:3])

# Display results
for i, doc in enumerate(graph_documents):
    print(f"\nDocument {i + 1}:")
    print(f"  Nodes: {len(doc.nodes)}")
    print(f"  Relationships: {len(doc.relationships)}")
    for node in doc.nodes[:3]:
        print(f"    Node(id='{node.id}', type='{node.type}')")
    for rel in doc.relationships[:3]:
        print(f"    {rel.source.id} --[{rel.type}]--> {rel.target.id}")

print("\nChallenge completed!")
