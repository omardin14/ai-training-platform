"""
Challenge: Complete the Retrieval Chain

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Creating prompt templates
- Building retrieval chains with LCEL
- Using RunnablePassthrough
- Invoking retrieval chains
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
# CHALLENGE: Complete the code below
# ============================================================================

# Step 1: Import and create prompt template
# Replace XXXX___ with the correct import (ChatPromptTemplate)
from langchain_core.prompts import XXXX___

message = """Answer the question using the context.

Context: {context}
Question: {question}
Answer:"""

# Replace XXXX___ with the correct method name (from_messages)
prompt_template = XXXX___.XXXX___([("human", message)])

# Step 2: Import RunnablePassthrough
# Replace XXXX___ with the correct import (RunnablePassthrough)
from langchain_core.runnables import XXXX___

# Step 3: Build the retrieval chain
retrieval_chain = (
    {
        "context": retriever,
        "question": XXXX___()  # Replace XXXX___ with RunnablePassthrough
    }
    | prompt_template
    | llm
)

# Step 4: Invoke the chain
# Replace XXXX___ with the correct method name (invoke)
question = "What is Python?"
response = retrieval_chain.XXXX___(question)

# Extract and print response
if use_openai:
    answer = response.content
else:
    answer = str(response).strip()

print(f"Question: {question}")
print(f"Answer: {answer}")

