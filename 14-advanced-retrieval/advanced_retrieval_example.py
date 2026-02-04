"""
Advanced Document Retrieval with LangChain

This example demonstrates advanced retrieval methods beyond simple vector similarity:
- Dense Retrieval: Vector-based semantic search
- Sparse Retrieval: Keyword-based exact matching (BM25)

These methods address different retrieval needs and can be combined for better results.
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
    """Example: Advanced retrieval methods for RAG applications."""
    
    print("\n" + "="*70)
    print("🔍 Advanced Document Retrieval")
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
    
    # ============================================================================
    # PREPARE DOCUMENTS
    # ============================================================================
    #
    # We'll use sample chunks to demonstrate retrieval methods
    #
    print("\n" + "-"*70)
    print("📄 Preparing Sample Documents:")
    print("-"*70)
    
    chunks = [
        "LangChain was created to simplify building applications with language models.",
        "LangChain provides tools for document loading, splitting, and retrieval.",
        "Vector databases enable semantic search by storing document embeddings.",
        "RAG applications combine retrieval with generation for accurate answers.",
        "Embeddings convert text into numerical vectors for similarity search.",
        "Document splitters break large texts into manageable chunks."
    ]
    
    print(f"✓ Created {len(chunks)} sample document chunks")
    for i, chunk in enumerate(chunks, 1):
        print(f"  {i}. {chunk}")
    
    # ============================================================================
    # DENSE RETRIEVAL (Vector-Based)
    # ============================================================================
    #
    # Dense retrieval encodes entire chunks as single vectors
    # Most component values are non-zero, hence "dense"
    # Excels at capturing semantic meaning
    #
    print("\n" + "-"*70)
    print("🔷 Dense Retrieval (Vector-Based):")
    print("-"*70)
    
    from langchain_openai import OpenAIEmbeddings
    from langchain_chroma import Chroma
    from langchain_core.documents import Document
    
    print("  Creating embeddings and vector store...")
    
    # Convert chunks to Document objects
    documents = [Document(page_content=chunk) for chunk in chunks]
    
    # Create embeddings model
    embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
    
    # Create vector store
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings
    )
    
    # Create dense retriever
    dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    print("✓ Dense retriever created")
    print("\n  Query: 'What is LangChain used for?'")
    
    # Query with dense retrieval
    query = "What is LangChain used for?"
    dense_results = dense_retriever.invoke(query)
    
    print(f"\n  Retrieved {len(dense_results)} documents:")
    for i, doc in enumerate(dense_results, 1):
        print(f"    {i}. {doc.page_content}")
    
    print("\n  Characteristics of Dense Retrieval:")
    print("    ✓ Excels at capturing semantic meaning")
    print("    ✓ Can find conceptually similar content")
    print("    ✗ Computationally intensive")
    print("    ✗ May struggle with rare/technical terms")
    
    # ============================================================================
    # SPARSE RETRIEVAL (BM25)
    # ============================================================================
    #
    # Sparse retrieval matches specific keywords/terms
    # Resulting vectors contain many zeros, few non-zero terms
    # Allows for precise retrieval and exact word matching
    #
    print("\n" + "-"*70)
    print("🔸 Sparse Retrieval (BM25):")
    print("-"*70)
    
    from langchain_community.retrievers import BM25Retriever
    
    print("  Creating BM25 retriever...")
    
    # Create BM25 retriever from texts
    bm25_retriever = BM25Retriever.from_texts(chunks, k=3)
    
    print("✓ BM25 retriever created")
    print("\n  Query: 'What is LangChain used for?'")
    
    # Query with BM25
    sparse_results = bm25_retriever.invoke(query)
    
    print(f"\n  Retrieved {len(sparse_results)} documents:")
    for i, doc in enumerate(sparse_results, 1):
        print(f"    {i}. {doc.page_content}")
    
    print("\n  Characteristics of Sparse Retrieval:")
    print("    ✓ Precise retrieval, exact word matching")
    print("    ✓ Better representation of rare words")
    print("    ✓ More explainable (aligned with specific terms)")
    print("    ✗ May miss semantically similar content")
    
    # ============================================================================
    # COMPARISON: Dense vs Sparse
    # ============================================================================
    #
    print("\n" + "-"*70)
    print("📊 Comparison: Dense vs Sparse Retrieval")
    print("-"*70)
    
    print("\n  Dense Retrieval:")
    print("    - Encodes entire chunk as single dense vector")
    print("    - Most component values are non-zero")
    print("    - Best for: Semantic similarity, conceptual matching")
    print("    - Limitations: Computationally intensive, struggles with rare terms")
    
    print("\n  Sparse Retrieval:")
    print("    - Matches specific keywords/terms")
    print("    - Vectors contain many zeros, few non-zero terms")
    print("    - Best for: Exact word matching, rare terms, explainability")
    print("    - Limitations: May miss semantically similar content")
    
    # ============================================================================
    # BM25 IN RAG CHAIN
    # ============================================================================
    #
    # BM25 can be used in RAG chains just like dense retrievers
    #
    print("\n" + "-"*70)
    print("🔗 BM25 in RAG Chain:")
    print("-"*70)
    
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.output_parsers import StrOutputParser
    
    # Create LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the question using the provided context."),
        ("human", "Context: {context}\n\nQuestion: {question}\n\nAnswer:")
    ])
    
    # Create RAG chain with BM25 retriever
    rag_chain = (
        {
            "context": bm25_retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    print("✓ RAG chain created with BM25 retriever")
    print("\n  Query: 'What is LangChain used for?'")
    
    # Invoke the chain
    answer = rag_chain.invoke("What is LangChain used for?")
    
    print(f"\n  Answer: {answer}")
    
    print("\n" + "="*70)
    print("✓ Example completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
