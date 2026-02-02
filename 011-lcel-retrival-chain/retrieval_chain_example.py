"""
LCEL Retrieval Chain with LangChain

This example demonstrates how to build retrieval chains using LangChain Expression Language (LCEL).
Retrieval chains combine document retrieval with LLM generation to create RAG applications.
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
    """Example: Build a retrieval chain using LCEL."""
    
    print("\n" + "="*70)
    print("🔗 LCEL Retrieval Chain Example")
    print("="*70)
    
    # Check for API key - use OpenAI if available, otherwise use Hugging Face
    openai_api_key = os.getenv("OPENAI_API_KEY")
    use_openai = openai_api_key and openai_api_key != "your-openai-api-key-here"
    
    if not use_openai:
        print("\n⚠️  Note: Retrieval chains work much better with OpenAI models.")
        print("   Hugging Face models may not follow the format as precisely.")
        print("   For best results, consider using an OpenAI API key.\n")
    
    # ============================================================================
    # STEP 1: LOAD AND PREPARE DOCUMENTS
    # ============================================================================
    #
    # First, we need to load documents, split them, and store them in a vector database
    # This is typically done once, and the vector store is reused
    #
    print("-"*70)
    print("📄 Step 1: Loading and Preparing Documents")
    print("-"*70)
    
    try:
        from langchain_community.document_loaders import TextLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_chroma import Chroma
        
        # Check for existing vector store
        persist_directory = "../010-RAG-document-storage/chroma_db"
        
        if os.path.exists(persist_directory):
            print(f"  Found existing vector store at: {persist_directory}")
            print("  Loading vector store...\n")
            
            # Load embeddings
            if use_openai:
                from langchain_openai import OpenAIEmbeddings
                embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
            else:
                from langchain_community.embeddings import HuggingFaceEmbeddings
                embedding_function = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )
            
            # Load existing vector store
            vectorstore = Chroma(
                persist_directory=persist_directory,
                embedding_function=embedding_function
            )
            print("  ✓ Vector store loaded successfully!\n")
        else:
            print("  ⚠️  Vector store not found. Creating sample documents...\n")
            # Create sample documents
            from langchain_core.documents import Document
            documents = [
                Document(page_content="Python is a versatile programming language used for web development, data science, and automation.", metadata={"source": "sample", "page": 1}),
                Document(page_content="Machine learning enables computers to learn patterns from data without explicit programming.", metadata={"source": "sample", "page": 2}),
                Document(page_content="Vector databases store embeddings that enable semantic search and retrieval.", metadata={"source": "sample", "page": 3})
            ]
            
            # Split documents
            splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
            split_docs = splitter.split_documents(documents)
            
            # Create embeddings
            if use_openai:
                from langchain_openai import OpenAIEmbeddings
                embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
            else:
                from langchain_community.embeddings import HuggingFaceEmbeddings
                embedding_function = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )
            
            # Create vector store
            vectorstore = Chroma.from_documents(
                documents=split_docs,
                embedding=embedding_function,
                persist_directory="./chroma_db"
            )
            print("  ✓ Created vector store with sample documents!\n")
            
    except ImportError as e:
        print(f"  ❌ Error: Required package not available: {e}")
        print("  Make sure you've completed module 010 first.\n")
        return
    
    # ============================================================================
    # STEP 2: CREATE RETRIEVER
    # ============================================================================
    #
    # A retriever searches the vector database and returns relevant documents
    #
    print("-"*70)
    print("🔍 Step 2: Creating Retriever")
    print("-"*70)
    
    # Configure the vector store as a retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 2}  # Return top 2 most similar documents
    )
    
    print("  Retriever configuration:")
    print("    → search_type: similarity")
    print("    → search_kwargs: k=2 (return top 2 results)")
    print("  ✓ Retriever created successfully!\n")
    
    # ============================================================================
    # STEP 3: CREATE PROMPT TEMPLATE
    # ============================================================================
    #
    # The prompt template defines how to format the retrieved documents and user query
    #
    print("-"*70)
    print("📝 Step 3: Creating Prompt Template")
    print("-"*70)
    
    from langchain_core.prompts import ChatPromptTemplate
    
    # Create a prompt template that uses retrieved context
    message = """You are a helpful AI assistant. Answer the question using the provided context.

Context:
{context}

Question: {question}

Answer:"""
    
    prompt_template = ChatPromptTemplate.from_messages([("human", message)])
    
    print("  Prompt template created:")
    print("    → Uses {context} variable for retrieved documents")
    print("    → Uses {question} variable for user query")
    print("  ✓ Prompt template created successfully!\n")
    
    # ============================================================================
    # STEP 4: CREATE LLM
    # ============================================================================
    #
    # Load the language model for generating responses
    #
    print("-"*70)
    print("🤖 Step 4: Loading Language Model")
    print("-"*70)
    
    if use_openai:
        from langchain_openai import ChatOpenAI
        print("  Loading OpenAI model (gpt-3.5-turbo)...")
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        print("  ✓ OpenAI model loaded successfully!\n")
    else:
        from langchain_huggingface import HuggingFacePipeline
        print("  Loading Hugging Face model (crumb/nano-mistral)...")
        print("  (This will download the model on first run - may take a few minutes)")
        llm = HuggingFacePipeline.from_model_id(
            model_id="crumb/nano-mistral",
            task="text-generation",
            pipeline_kwargs={"max_new_tokens": 150}
        )
        print("  ✓ Hugging Face model loaded successfully!\n")
    
    # ============================================================================
    # STEP 5: BUILD RETRIEVAL CHAIN WITH LCEL
    # ============================================================================
    #
    # LCEL (LangChain Expression Language) allows us to chain components together
    # using the pipe operator (|) and dictionary syntax
    #
    print("-"*70)
    print("🔗 Step 5: Building Retrieval Chain with LCEL")
    print("-"*70)
    
    from langchain_core.runnables import RunnablePassthrough
    
    # Build the retrieval chain
    # The chain:
    # 1. Takes a question as input
    # 2. Retrieves relevant documents using the retriever
    # 3. Formats them into context
    # 4. Passes both context and question to the prompt template
    # 5. Sends the formatted prompt to the LLM
    # 6. Returns the LLM's response
    
    retrieval_chain = (
        {
            "context": retriever,  # Retrieve documents based on question
            "question": RunnablePassthrough()  # Pass the question through as-is
        }
        | prompt_template  # Format the prompt with context and question
        | llm  # Generate response using LLM
    )
    
    print("  Chain structure:")
    print("    → Input: question")
    print("    → Step 1: Retrieve relevant documents (retriever)")
    print("    → Step 2: Format prompt with context and question (prompt_template)")
    print("    → Step 3: Generate answer (llm)")
    print("  ✓ Retrieval chain created successfully!\n")
    
    # ============================================================================
    # STEP 6: USE THE RETRIEVAL CHAIN
    # ============================================================================
    #
    # Invoke the chain with a question
    #
    print("="*70)
    print("💬 Using the Retrieval Chain")
    print("="*70)
    
    question = "What is machine learning?"
    print(f"\n📥 Question: '{question}'\n")
    
    print("  Processing:")
    print("    1. Retrieving relevant documents from vector database...")
    print("    2. Formatting prompt with retrieved context...")
    print("    3. Generating answer using LLM...\n")
    
    # Invoke the chain
    response = retrieval_chain.invoke(question)
    
    # Extract the response content
    if use_openai:
        answer = response.content
    else:
        answer = str(response).strip()
    
    print("="*70)
    print("✨ Response:")
    print("="*70)
    print(f"\n{answer}\n")
    print("="*70 + "\n")
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("="*70)
    print("📊 Summary")
    print("="*70)
    print("\nKey Concepts:")
    print("  1. Retrievers search vector databases for relevant documents")
    print("  2. LCEL chains components together using the pipe operator (|)")
    print("  3. Dictionary syntax allows multiple inputs to a chain")
    print("  4. RunnablePassthrough passes values through unchanged")
    print("  5. Retrieval chains combine retrieval with generation")
    print("\nRetrieval chains enable RAG applications that answer questions using")
    print("retrieved context from your documents!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

