"""
Challenge Solution: Retrieval Chain

This is the complete solution for the retrieval chain challenge.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for API key
openai_api_key = os.getenv("OPENAI_API_KEY")
use_openai = openai_api_key and openai_api_key != "your-openai-api-key-here"

# Setup: Create a simple retriever with sample documents
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

documents = [
    Document(page_content="Python is a programming language.", metadata={"source": "sample"}),
    Document(page_content="Machine learning uses algorithms to learn from data.", metadata={"source": "sample"})
]

splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
split_docs = splitter.split_documents(documents)

if use_openai:
    from langchain_openai import OpenAIEmbeddings
    embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
else:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(documents=split_docs, embedding=embedding_function)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})

# Load LLM
if use_openai:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
else:
    from langchain_huggingface import HuggingFacePipeline
    llm = HuggingFacePipeline.from_model_id(
        model_id="crumb/nano-mistral",
        task="text-generation",
        pipeline_kwargs={"max_new_tokens": 50}
    )

# ============================================================================
# SOLUTION: Complete code
# ============================================================================

# Step 1: Import and create prompt template
from langchain_core.prompts import ChatPromptTemplate

message = """Answer the question using the context.

Context: {context}
Question: {question}
Answer:"""

prompt_template = ChatPromptTemplate.from_messages([("human", message)])

# Step 2: Import RunnablePassthrough
from langchain_core.runnables import RunnablePassthrough

# Step 3: Build the retrieval chain
retrieval_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | prompt_template
    | llm
)

# Step 4: Invoke the chain
question = "What is Python?"
response = retrieval_chain.invoke(question)

# Extract and print response
if use_openai:
    answer = response.content
else:
    answer = str(response).strip()

print(f"Question: {question}")
print(f"Answer: {answer}")

