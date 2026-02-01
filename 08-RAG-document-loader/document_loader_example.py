"""
Document Loaders with LangChain

This example demonstrates how to load documents from various sources using LangChain's
document loaders. Document loaders are essential for RAG (Retrieval-Augmented Generation)
applications.
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
    """Example: Load documents from different sources using LangChain loaders."""
    
    print("\n" + "="*70)
    print("📄 Document Loader Example")
    print("="*70)
    
    # ============================================================================
    # PDF DOCUMENT LOADER
    # ============================================================================
    #
    # PyPDFLoader loads PDF files and extracts text content
    # Each page becomes a separate document
    #
    print("\n" + "-"*70)
    print("📕 Loading PDF Document:")
    print("-"*70)
    
    try:
        from langchain_community.document_loaders import PyPDFLoader
        
        # Create a document loader for a PDF file
        # Note: You would replace this with an actual PDF file path
        pdf_path = "sample_docs/sample_document.pdf"
        
        print(f"  Creating loader for: {pdf_path}")
        print("  (In a real application, you would provide an actual PDF file path)\n")
        
        # Check if file exists (for demonstration, we'll show the structure)
        if os.path.exists(pdf_path):
            loader = PyPDFLoader(pdf_path)
            print("  ✓ Loader created successfully")
            
            # Load the document
            print("  Loading document...")
            documents = loader.load()
            
            print(f"  ✓ Loaded {len(documents)} page(s)")
            print(f"    → First page preview: {documents[0].page_content[:100]}...")
            print(f"    → Metadata: {documents[0].metadata}\n")
        else:
            print("  ⚠️  PDF file not found (this is expected in the demo)")
            print("  Structure:")
            print("    loader = PyPDFLoader('path/to/file.pdf')")
            print("    documents = loader.load()")
            print("    # Each page becomes a Document object\n")
            
    except ImportError:
        print("  ⚠️  PyPDFLoader not available. Install with: pip install pypdf\n")
    
    # ============================================================================
    # CSV DOCUMENT LOADER
    # ============================================================================
    #
    # CSVLoader loads CSV files and converts each row into a document
    # Useful for structured data that needs to be processed as text
    #
    print("-"*70)
    print("📊 Loading CSV Document:")
    print("-"*70)
    
    try:
        from langchain_community.document_loaders.csv_loader import CSVLoader
        
        # Create a document loader for a CSV file
        csv_path = "sample_docs/sample_data.csv"
        
        print(f"  Creating loader for: {csv_path}")
        print("  (In a real application, you would provide an actual CSV file path)\n")
        
        # Check if file exists (for demonstration, we'll show the structure)
        if os.path.exists(csv_path):
            loader = CSVLoader(csv_path)
            print("  ✓ Loader created successfully")
            
            # Load the document
            print("  Loading document...")
            documents = loader.load()
            
            print(f"  ✓ Loaded {len(documents)} row(s)")
            print(f"    → First row preview: {documents[0].page_content[:100]}...")
            print(f"    → Metadata: {documents[0].metadata}\n")
        else:
            print("  ⚠️  CSV file not found (this is expected in the demo)")
            print("  Structure:")
            print("    loader = CSVLoader('path/to/file.csv')")
            print("    documents = loader.load()")
            print("    # Each row becomes a Document object\n")
            
    except ImportError:
        print("  ⚠️  CSVLoader not available. Install required dependencies.\n")
    
    # ============================================================================
    # HTML DOCUMENT LOADER
    # ============================================================================
    #
    # UnstructuredHTMLLoader loads HTML files and extracts text content
    # Useful for web pages and HTML documents
    #
    print("-"*70)
    print("🌐 Loading HTML Document:")
    print("-"*70)
    
    try:
        from langchain_community.document_loaders import UnstructuredHTMLLoader
        
        # Create a document loader for an HTML file
        html_path = "sample_docs/sample_page.html"
        
        print(f"  Creating loader for: {html_path}")
        print("  (In a real application, you would provide an actual HTML file path)\n")
        
        # Check if file exists (for demonstration, we'll show the structure)
        if os.path.exists(html_path):
            loader = UnstructuredHTMLLoader(html_path)
            print("  ✓ Loader created successfully")
            
            # Load the document
            print("  Loading document...")
            documents = loader.load()
            
            print(f"  ✓ Loaded {len(documents)} document(s)")
            print(f"    → Content preview: {documents[0].page_content[:100]}...")
            print(f"    → Metadata: {documents[0].metadata}\n")
        else:
            print("  ⚠️  HTML file not found (this is expected in the demo)")
            print("  Structure:")
            print("    loader = UnstructuredHTMLLoader('path/to/file.html')")
            print("    documents = loader.load()")
            print("    # HTML content is extracted as text\n")
            
    except ImportError:
        print("  ⚠️  UnstructuredHTMLLoader not available.")
        print("  Install with: pip install unstructured\n")
    
    # ============================================================================
    # TEXT FILE LOADER (Simple Example)
    # ============================================================================
    #
    # TextLoader loads plain text files
    # Simple but useful for many use cases
    #
    print("-"*70)
    print("📝 Loading Text Document:")
    print("-"*70)
    
    try:
        from langchain_community.document_loaders import TextLoader
        
        # Create a document loader for a text file
        text_path = "sample_docs/sample_text.txt"
        
        print(f"  Creating loader for: {text_path}")
        print("  (In a real application, you would provide an actual text file path)\n")
        
        # Check if file exists (for demonstration, we'll show the structure)
        if os.path.exists(text_path):
            loader = TextLoader(text_path)
            print("  ✓ Loader created successfully")
            
            # Load the document
            print("  Loading document...")
            documents = loader.load()
            
            print(f"  ✓ Loaded {len(documents)} document(s)")
            print(f"    → Content preview: {documents[0].page_content[:100]}...")
            print(f"    → Metadata: {documents[0].metadata}\n")
        else:
            print("  ⚠️  Text file not found (this is expected in the demo)")
            print("  Structure:")
            print("    loader = TextLoader('path/to/file.txt')")
            print("    documents = loader.load()")
            print("    # File content becomes a Document object\n")
            
    except ImportError:
        print("  ⚠️  TextLoader not available.\n")
    
    # ============================================================================
    # DOCUMENT STRUCTURE
    # ============================================================================
    #
    # All loaders return Document objects with:
    # - page_content: The text content of the document
    # - metadata: Information about the document (source, page number, etc.)
    #
    print("="*70)
    print("📋 Document Structure:")
    print("="*70)
    print("\nAll document loaders return Document objects with:")
    print("  - page_content: The text content extracted from the file")
    print("  - metadata: Dictionary containing information about the document")
    print("    → source: File path or URL")
    print("    → page: Page number (for PDFs)")
    print("    → row: Row number (for CSVs)")
    print("    → Other format-specific metadata\n")
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("="*70)
    print("📊 Summary")
    print("="*70)
    print("\nKey Concepts:")
    print("  1. Document loaders extract text from various file formats")
    print("  2. Each loader is designed for a specific file type")
    print("  3. Loaders return Document objects with content and metadata")
    print("  4. Documents can be used for RAG, search, and other applications")
    print("  5. Different loaders handle different formats (PDF, CSV, HTML, etc.)")
    print("\nDocument loaders are the first step in building RAG applications!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

