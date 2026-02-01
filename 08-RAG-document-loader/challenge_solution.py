"""
Challenge Solution: Document Loader

This is the complete solution for the document loader challenge.
"""

# ============================================================================
# SOLUTION: Complete code
# ============================================================================

# Step 1: Import the PDF document loader
from langchain_community.document_loaders import PyPDFLoader

# Step 2: Create a loader instance for a PDF file
file_path = "sample_docs/example.pdf"
loader = PyPDFLoader(file_path)

# Step 3: Load the document
documents = loader.load()

# Step 4: Access the first document's content and metadata
if len(documents) > 0:
    first_doc = documents[0]
    print(f"Content preview: {first_doc.page_content[:100]}...")
    print(f"Metadata: {first_doc.metadata}")
else:
    print("No documents loaded. Make sure the PDF file exists.")

