"""
Challenge: Complete the Document Loader

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Importing document loaders
- Creating loader instances
- Loading documents
- Accessing document content and metadata
"""

# ============================================================================
# CHALLENGE: Complete the code below
# ============================================================================

# Step 1: Import the PDF document loader
# Replace XXXX___ with the correct import (PyPDFLoader)
from langchain_community.document_loaders import XXXX___

# Step 2: Create a loader instance for a PDF file
# Replace XXXX___ with the correct class name
file_path = "sample_docs/example.pdf"
loader = XXXX___(file_path)

# Step 3: Load the document
# Replace XXXX___ with the correct method name
documents = loader.XXXX___()

# Step 4: Access the first document's content and metadata
if len(documents) > 0:
    first_doc = documents[0]
    print(f"Content preview: {first_doc.page_content[:100]}...")
    print(f"Metadata: {first_doc.metadata}")
else:
    print("No documents loaded. Make sure the PDF file exists.")

