"""
Challenge: Load and Split Markdown and Python Documents

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Loading Markdown files with UnstructuredMarkdownLoader
- Loading Python files with PythonLoader
- Splitting Python code with language-aware splitters
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the path to sample documents
base_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.join(base_dir, "..", "utils", "docs")

# ============================================================================
# CHALLENGE: Complete the code below
# ============================================================================

# Step 1: Load Markdown document
# Replace XXXX___ with the correct import (UnstructuredMarkdownLoader)
from langchain_community.document_loaders import XXXX___

markdown_path = os.path.join(utils_dir, "sample_documentation.md")
if os.path.exists(markdown_path):
    loader = XXXX___(markdown_path)
    # Replace XXXX___ with the correct method name (load)
    markdown_data = loader.XXXX___()
    print(f"✓ Loaded Markdown: {len(markdown_data)} document(s)")
else:
    print("⚠️  Markdown file not found")
    markdown_data = []

# Step 2: Load Python document
# Replace XXXX___ with the correct import (PythonLoader)
from langchain_community.document_loaders import XXXX___

python_path = os.path.join(utils_dir, "sample_code.py")
if os.path.exists(python_path):
    loader = XXXX___(python_path)
    python_data = loader.load()
    print(f"✓ Loaded Python: {len(python_data)} document(s)")
else:
    print("⚠️  Python file not found")
    python_data = []

# Step 3: Split Python code with language-aware splitter
if python_data:
    # Replace XXXX___ with the correct import (RecursiveCharacterTextSplitter)
    from langchain_text_splitters import XXXX___
    # Replace XXXX___ with the correct import (Language)
    from langchain_text_splitters import XXXX___
    
    # Replace XXXX___ with the correct method name (from_language)
    # Replace XXXX___ with Language.PYTHON
    python_splitter = XXXX___.XXXX___(
        language=XXXX___,
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
