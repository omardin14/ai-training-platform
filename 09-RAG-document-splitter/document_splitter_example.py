"""
Document Splitters with LangChain

This example demonstrates how to split documents into smaller chunks using LangChain's
text splitters. Document splitting is essential for RAG applications to handle
large documents and improve retrieval accuracy.
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
    """Example: Split documents using different splitting strategies."""
    
    print("\n" + "="*70)
    print("✂️  Document Splitter Example")
    print("="*70)
    
    # ============================================================================
    # CHARACTER TEXT SPLITTER
    # ============================================================================
    #
    # CharacterTextSplitter splits text by a specific separator character
    # Simple and straightforward, but may break words or sentences
    #
    print("\n" + "-"*70)
    print("📝 Character Text Splitter:")
    print("-"*70)
    
    from langchain_text_splitters import CharacterTextSplitter
    
    # Sample text to split
    sample_text = 'Learning is a journey that never ends.\nEach day brings new opportunities.\nKnowledge grows with every experience.\nPractice makes perfect.'
    
    print("  Original text:")
    print(f"    {sample_text}\n")
    
    # Define splitting parameters
    chunk_size = 30
    chunk_overlap = 10
    
    print(f"  Splitting parameters:")
    print(f"    → chunk_size: {chunk_size} characters")
    print(f"    → chunk_overlap: {chunk_overlap} characters")
    print(f"    → separator: newline (\\n)\n")
    
    # Create the splitter
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    print("  Creating CharacterTextSplitter...")
    print("  ✓ Splitter created\n")
    
    # Split the text
    print("  Splitting text...")
    chunks = splitter.split_text(sample_text)
    
    print(f"  ✓ Created {len(chunks)} chunk(s)\n")
    print("  Chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"    Chunk {i} ({len(chunk)} chars): {chunk}")
    print()
    
    # ============================================================================
    # RECURSIVE CHARACTER TEXT SPLITTER
    # ============================================================================
    #
    # RecursiveCharacterTextSplitter tries multiple separators in order
    # More intelligent splitting that tries to keep sentences/words together
    #
    print("-"*70)
    print("🔄 Recursive Character Text Splitter:")
    print("-"*70)
    
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    
    # Sample text to split
    sample_text = 'Artificial intelligence transforms how we work.\nMachine learning enables new possibilities.\nDeep learning powers advanced applications.\nNatural language processing understands human communication.'
    
    print("  Original text:")
    print(f"    {sample_text}\n")
    
    # Define splitting parameters
    chunk_size = 40
    chunk_overlap = 15
    
    print(f"  Splitting parameters:")
    print(f"    → chunk_size: {chunk_size} characters")
    print(f"    → chunk_overlap: {chunk_overlap} characters")
    print(f"    → separators: [\"\\n\", \" \", \"\"] (tries newlines, then spaces, then characters)\n")
    
    # Create the recursive splitter
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    print("  Creating RecursiveCharacterTextSplitter...")
    print("  ✓ Splitter created\n")
    
    # Split the text
    print("  Splitting text...")
    chunks = splitter.split_text(sample_text)
    
    print(f"  ✓ Created {len(chunks)} chunk(s)\n")
    print("  Chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"    Chunk {i} ({len(chunk)} chars): {chunk}")
    print()
    
    # ============================================================================
    # SPLITTING DOCUMENTS (HTML Example)
    # ============================================================================
    #
    # When working with Document objects from loaders, use split_documents()
    # This preserves metadata while splitting the content
    #
    print("-"*70)
    print("📄 Splitting HTML Documents:")
    print("-"*70)
    
    try:
        from langchain_community.document_loaders import UnstructuredHTMLLoader
        
        # Load an HTML document
        html_path = "../08-RAG-document-loader/sample_docs/sample_page.html"
        
        if os.path.exists(html_path):
            print(f"  Loading HTML document: {html_path}")
            loader = UnstructuredHTMLLoader(html_path)
            documents = loader.load()
            print(f"  ✓ Loaded {len(documents)} document(s)\n")
            
            # Define splitting parameters
            chunk_size = 300
            chunk_overlap = 100
            
            print(f"  Splitting parameters:")
            print(f"    → chunk_size: {chunk_size} characters")
            print(f"    → chunk_overlap: {chunk_overlap} characters")
            print(f"    → separators: [\".\", \"\\n\", \" \", \"\"] (tries periods, newlines, spaces, then characters)\n")
            
            # Create the recursive splitter for documents
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=[".", "\n", " ", ""]
            )
            
            print("  Creating RecursiveCharacterTextSplitter...")
            print("  ✓ Splitter created\n")
            
            # Split the documents
            print("  Splitting documents...")
            split_docs = splitter.split_documents(documents)
            
            print(f"  ✓ Created {len(split_docs)} chunk(s) from {len(documents)} document(s)\n")
            print("  First few chunks:")
            for i, doc in enumerate(split_docs[:3], 1):
                print(f"    Chunk {i} ({len(doc.page_content)} chars):")
                print(f"      Content: {doc.page_content[:80]}...")
                print(f"      Metadata: {doc.metadata}\n")
            
            if len(split_docs) > 3:
                print(f"    ... and {len(split_docs) - 3} more chunk(s)\n")
        else:
            print(f"  ⚠️  HTML file not found: {html_path}")
            print("  Structure:")
            print("    loader = UnstructuredHTMLLoader('path/to/file.html')")
            print("    documents = loader.load()")
            print("    splitter = RecursiveCharacterTextSplitter(...)")
            print("    split_docs = splitter.split_documents(documents)\n")
            
    except ImportError:
        print("  ⚠️  UnstructuredHTMLLoader not available.")
        print("  Install with: pip install unstructured\n")
    
    # ============================================================================
    # SPLITTING PARAMETERS EXPLAINED
    # ============================================================================
    #
    # Understanding chunk_size and chunk_overlap
    #
    print("="*70)
    print("📊 Splitting Parameters Explained:")
    print("="*70)
    print("\nKey Concepts:")
    print("  1. chunk_size: Maximum size of each chunk (in characters)")
    print("     → Larger chunks = more context, but may exceed model limits")
    print("     → Smaller chunks = better precision, but may lose context")
    print()
    print("  2. chunk_overlap: Number of characters to overlap between chunks")
    print("     → Prevents losing context at chunk boundaries")
    print("     → Helps maintain continuity across chunks")
    print("     → Typically 10-20% of chunk_size")
    print()
    print("  3. separators: Characters/strings to split on (in order of preference)")
    print("     → CharacterTextSplitter: Single separator")
    print("     → RecursiveCharacterTextSplitter: Multiple separators tried in order")
    print()
    print("  4. split_text() vs split_documents():")
    print("     → split_text(): For plain strings, returns list of strings")
    print("     → split_documents(): For Document objects, returns list of Documents")
    print("       (preserves metadata)\n")
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("="*70)
    print("📊 Summary")
    print("="*70)
    print("\nKey Concepts:")
    print("  1. CharacterTextSplitter: Simple splitting by a single separator")
    print("  2. RecursiveCharacterTextSplitter: Intelligent splitting with multiple separators")
    print("  3. split_text(): Splits plain strings into chunks")
    print("  4. split_documents(): Splits Document objects while preserving metadata")
    print("  5. chunk_size and chunk_overlap control chunk size and continuity")
    print("\nDocument splitters are essential for processing large documents in RAG!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

