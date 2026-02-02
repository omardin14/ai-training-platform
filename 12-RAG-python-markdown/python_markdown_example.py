"""
Markdown and Python Document Loaders with LangChain

This example demonstrates how to load and split Markdown and Python files
using LangChain's specialized loaders and language-aware splitters.

Markdown is commonly used for documentation, and Python files can be loaded
to create code-aware RAG applications that can answer questions about codebases.
"""

import os
import warnings
from dotenv import load_dotenv

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)

# Load environment variables from .env file
load_dotenv()


def main():
    """Example: Load and split Markdown and Python documents."""
    
    print("\n" + "="*70)
    print("📄 Markdown and Python Document Loaders")
    print("="*70)
    
    # Check for OpenAI API key - required for this module
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key or openai_api_key == "your-openai-api-key-here":
        print("\n❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("   Please set your OpenAI API key in the .env file or environment.")
        print("   Get your key from: https://platform.openai.com/api-keys")
        print("\n   Example .env file content:")
        print("   OPENAI_API_KEY=sk-your-actual-api-key-here")
        print("\n   Or export it in your shell:")
        print("   export OPENAI_API_KEY='sk-your-actual-api-key-here'")
        print("\n" + "="*70 + "\n")
        return
    
    # Get the path to sample documents
    base_dir = os.path.dirname(os.path.abspath(__file__))
    utils_dir = os.path.join(base_dir, "..", "utils", "docs")
    
    # ============================================================================
    # MARKDOWN LOADER
    # ============================================================================
    #
    # UnstructuredMarkdownLoader loads Markdown files
    # Markdown is a lightweight markup language for creating formatted documents
    # It's often the tool of choice for writing code documentation
    #
    print("\n" + "-"*70)
    print("📝 Loading Markdown Document:")
    print("-"*70)
    
    from langchain_community.document_loaders import UnstructuredMarkdownLoader
    
    markdown_path = os.path.join(utils_dir, "sample_documentation.md")
    
    if os.path.exists(markdown_path):
        # Create a document loader for Markdown file
        loader = UnstructuredMarkdownLoader(markdown_path)
        
        # Load the document
        markdown_data = loader.load()
        
        print(f"\n✓ Loaded Markdown document: {markdown_path}")
        print(f"  Number of documents: {len(markdown_data)}")
        print(f"  Document preview (first 200 characters):")
        print(f"  {markdown_data[0].page_content[:200]}...")
        print(f"\n  Metadata: {markdown_data[0].metadata}")
    else:
        print(f"⚠️  Markdown file not found: {markdown_path}")
        markdown_data = []
    
    # ============================================================================
    # PYTHON LOADER
    # ============================================================================
    #
    # PythonLoader loads Python source files
    # This is useful for creating RAG applications that can answer questions
    # about codebases
    # Can be tricky during splitting - use language-aware splitters!
    #
    print("\n" + "-"*70)
    print("🐍 Loading Python Document:")
    print("-"*70)
    
    from langchain_community.document_loaders import PythonLoader
    
    python_path = os.path.join(utils_dir, "sample_code.py")
    
    if os.path.exists(python_path):
        # Create a document loader for Python file
        loader = PythonLoader(python_path)
        
        # Load the document
        python_data = loader.load()
        
        print(f"\n✓ Loaded Python document: {python_path}")
        print(f"  Number of documents: {len(python_data)}")
        print(f"  Document preview (first 200 characters):")
        print(f"  {python_data[0].page_content[:200]}...")
        print(f"\n  Metadata: {python_data[0].metadata}")
    else:
        print(f"⚠️  Python file not found: {python_path}")
        python_data = []
    
    # ============================================================================
    # LANGUAGE-AWARE SPLITTING FOR PYTHON
    # ============================================================================
    #
    # RecursiveCharacterTextSplitter.from_language() creates a splitter
    # that understands the structure of Python code
    # Instead of splitting per text or document, it's best to use the recursive
    # text splitter with from_language method for code files
    #
    print("\n" + "-"*70)
    print("✂️  Splitting Python Code with Language-Aware Splitter:")
    print("-"*70)
    
    if python_data:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_text_splitters import Language
        
        # Create a Python-aware recursive character splitter
        # This splitter understands Python syntax and will split at appropriate
        # boundaries (functions, classes, etc.) rather than arbitrary text positions
        python_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size=300,
            chunk_overlap=100
        )
        
        # Split the Python content into chunks
        chunks = python_splitter.split_documents(python_data)
        
        print(f"\n✓ Split Python document into {len(chunks)} chunks")
        print(f"  Chunk size: 300 characters")
        print(f"  Chunk overlap: 100 characters")
        print(f"\n  First 3 chunks:")
        
        for i, chunk in enumerate(chunks[:3], 1):
            print(f"\n  ── Chunk {i} ──")
            print(f"  Length: {len(chunk.page_content)} characters")
            print(f"  Content preview:")
            # Show first 150 characters of each chunk
            preview = chunk.page_content[:150].replace('\n', ' ')
            print(f"  {preview}...")
    else:
        print("⚠️  No Python data to split")
    
    # ============================================================================
    # REGULAR SPLITTING FOR MARKDOWN
    # ============================================================================
    #
    # For Markdown, we can use the regular RecursiveCharacterTextSplitter
    # Markdown structure is less critical than code structure
    #
    print("\n" + "-"*70)
    print("✂️  Splitting Markdown Document:")
    print("-"*70)
    
    if markdown_data:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        
        # Create a regular recursive character splitter for Markdown
        markdown_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]  # Markdown-aware separators
        )
        
        # Split the Markdown content into chunks
        markdown_chunks = markdown_splitter.split_documents(markdown_data)
        
        print(f"\n✓ Split Markdown document into {len(markdown_chunks)} chunks")
        print(f"  Chunk size: 500 characters")
        print(f"  Chunk overlap: 50 characters")
        print(f"\n  First 2 chunks:")
        
        for i, chunk in enumerate(markdown_chunks[:2], 1):
            print(f"\n  ── Chunk {i} ──")
            print(f"  Length: {len(chunk.page_content)} characters")
            print(f"  Content preview:")
            preview = chunk.page_content[:150].replace('\n', ' ')
            print(f"  {preview}...")
    else:
        print("⚠️  No Markdown data to split")
    
    print("\n" + "="*70)
    print("✓ Example completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
