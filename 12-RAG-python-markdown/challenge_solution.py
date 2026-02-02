"""
Challenge Solution: Load and Split Markdown and Python Documents

This is the complete solution for the Markdown and Python loader challenge.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the path to sample documents
base_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.join(base_dir, "..", "utils", "docs")

# ============================================================================
# SOLUTION: Complete code
# ============================================================================

# Step 1: Load Markdown document
from langchain_community.document_loaders import UnstructuredMarkdownLoader

markdown_path = os.path.join(utils_dir, "sample_documentation.md")
if os.path.exists(markdown_path):
    loader = UnstructuredMarkdownLoader(markdown_path)
    markdown_data = loader.load()
    print(f"✓ Loaded Markdown: {len(markdown_data)} document(s)")
else:
    print("⚠️  Markdown file not found")
    markdown_data = []

# Step 2: Load Python document
from langchain_community.document_loaders import PythonLoader

python_path = os.path.join(utils_dir, "sample_code.py")
if os.path.exists(python_path):
    loader = PythonLoader(python_path)
    python_data = loader.load()
    print(f"✓ Loaded Python: {len(python_data)} document(s)")
else:
    print("⚠️  Python file not found")
    python_data = []

# Step 3: Split Python code with language-aware splitter
if python_data:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_text_splitters import Language
    
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=300,
        chunk_overlap=100
    )
    
    chunks = python_splitter.split_documents(python_data)
    print(f"✓ Split Python into {len(chunks)} chunks")
    
    # Print first chunk preview
    if chunks:
        print(f"\nFirst chunk preview (first 100 chars):")
        print(chunks[0].page_content[:100] + "...")
else:
    print("⚠️  No Python data to split")

print("\n✓ Challenge completed!")
