"""
Challenge: Advanced Document Retrieval

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- BM25 sparse retrieval
- Using retrievers in RAG chains
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
# CHALLENGE: Complete the code below
# ============================================================================

# Step 1: Create BM25 retriever
# Replace XXXX___ with the correct import (BM25Retriever)
from langchain_community.retrievers import XXXX___

# Replace XXXX___ with the correct method name (from_texts)
bm25_retriever = XXXX___.XXXX___(chunks, k=3)

# Step 2: Query the retriever
# Replace XXXX___ with the correct method name (invoke)
query = "What is LangChain used for?"
results = bm25_retriever.XXXX___(query)

# Step 3: Print results
print("Most Relevant Document:")
print(results[0].page_content)

print("\n✓ Challenge completed!")
