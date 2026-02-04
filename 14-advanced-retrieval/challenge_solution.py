"""
Challenge Solution: Advanced Document Retrieval

This is the complete solution for the advanced retrieval challenge.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key or openai_api_key == "your-openai-api-key-here":
    print("❌ Error: OPENAI_API_KEY not found. Please set it in .env file.")
    exit(1)

# Sample chunks
chunks = [
    "LangChain was created to simplify building applications with language models.",
    "LangChain provides tools for document loading, splitting, and retrieval.",
    "Vector databases enable semantic search by storing document embeddings."
]

# ============================================================================
# SOLUTION: Complete code
# ============================================================================

# Step 1: Create BM25 retriever
from langchain_community.retrievers import BM25Retriever

bm25_retriever = BM25Retriever.from_texts(chunks, k=3)

# Step 2: Query the retriever
query = "What is LangChain used for?"
results = bm25_retriever.invoke(query)

# Step 3: Print results
print("Most Relevant Document:")
print(results[0].page_content)

print("\n✓ Challenge completed!")
