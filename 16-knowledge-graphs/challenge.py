"""
Challenge: Knowledge Graphs

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Loading documents from Wikipedia
- Splitting documents into chunks
- Using LLMGraphTransformer to extract entities and relationships
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
# CHALLENGE: Complete the code below
# ============================================================================

# Step 1: Load documents from Wikipedia
# Replace XXXX___ with the correct loader class (WikipediaLoader)
from langchain_community.document_loaders import XXXX___

raw_documents = XXXX___(query="Machine Learning").load()
print(f"Loaded {len(raw_documents)} document(s)")

# Step 2: Split documents into chunks
# Replace XXXX___ with the correct splitter class (TokenTextSplitter)
from langchain_text_splitters import XXXX___

text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=20)
documents = text_splitter.split_documents(raw_documents[:3])
print(f"Split into {len(documents)} chunk(s)")

# Step 3: Create the LLM and graph transformer
from langchain_openai import ChatOpenAI

# Replace XXXX___ with the correct import (LLMGraphTransformer)
from langchain_experimental.graph_transformers import XXXX___

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
llm_transformer = LLMGraphTransformer(llm=llm)
print("Graph transformer created")

# Step 4: Convert documents to graph format
# Replace XXXX___ with the correct method name (convert_to_graph_documents)
graph_documents = llm_transformer.XXXX___(documents[:3])

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
