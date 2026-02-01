"""
Challenge: Complete the Document Splitter

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Importing document splitters
- Creating splitter instances
- Splitting documents
- Understanding chunk parameters
"""

from langchain_community.document_loaders import TextLoader

# Load a document first
loader = TextLoader("../08-RAG-document-loader/sample_docs/sample_text.txt")
documents = loader.load()

# ============================================================================
# CHALLENGE: Complete the code below
# ============================================================================

# Step 1: Import the recursive character splitter
# Replace XXXX___ with the correct import (RecursiveCharacterTextSplitter)
from langchain_text_splitters import XXXX___

# Step 2: Create a splitter instance
# Replace XXXX___ with the correct class name
splitter = XXXX___(
    chunk_size=100,
    chunk_overlap=20,
    separators=["\n", " ", ""]
)

# Step 3: Split the documents
# Replace XXXX___ with the correct method name
split_docs = splitter.XXXX___(documents)

# Step 4: Print results
print(f"Original documents: {len(documents)}")
print(f"Split into chunks: {len(split_docs)}")
if len(split_docs) > 0:
    print(f"\nFirst chunk preview: {split_docs[0].page_content[:80]}...")

