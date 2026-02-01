"""
Challenge Solution: Document Splitter

This is the complete solution for the document splitter challenge.
"""

from langchain_community.document_loaders import TextLoader

# Load a document first
loader = TextLoader("../08-RAG-document-loader/sample_docs/sample_text.txt")
documents = loader.load()

# ============================================================================
# SOLUTION: Complete code
# ============================================================================

# Step 1: Import the recursive character splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Step 2: Create a splitter instance
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    separators=["\n", " ", ""]
)

# Step 3: Split the documents
split_docs = splitter.split_documents(documents)

# Step 4: Print results
print(f"Original documents: {len(documents)}")
print(f"Split into chunks: {len(split_docs)}")
if len(split_docs) > 0:
    print(f"\nFirst chunk preview: {split_docs[0].page_content[:80]}...")

