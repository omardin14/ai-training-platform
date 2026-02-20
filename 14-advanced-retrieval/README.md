# Advanced Document Retrieval

This module introduces **advanced retrieval methods** that go beyond simple vector similarity search. We'll explore both **dense** and **sparse** retrieval techniques, each with their own strengths and use cases.

<!-- lesson:page Dense Retrieval -->
## Overview

Traditional RAG applications use vector databases with embeddings for document retrieval. However, different retrieval methods excel in different scenarios:

- **Dense Retrieval**: Best for semantic similarity and conceptual matching
- **Sparse Retrieval**: Best for exact keyword matching and rare terms

Understanding both methods allows you to choose the right approach for your use case, or even combine them for better results.

![RAG Vector Database Process](../utils/media/rag_vector_db_optimised.png)

## Dense Retrieval

### What is Dense Retrieval?

Document retrieval has traditionally consisted of a **vector database containing embedded documents**. The input to the RAG application is then used to query the vectors, using a **distance metric** to determine which vectors are closest and therefore most similar and relevant.

**Dense retrieval methods** encode the entire chunk as a single vector that is said to be **"dense"**, that is, most of its component values are non-zero.

### Characteristics

**Strengths:**
- **Excels at capturing semantic meaning**: Understands concepts and relationships
- **Conceptual matching**: Can find related content even without exact word matches
- **Context-aware**: Considers the full meaning of text

**Limitations:**
- **Computationally intensive**: Requires embedding generation and vector operations
- **May struggle with rare words**: Common words dominate the embeddings
- **May struggle with highly specific technical terms**: Technical jargon may not be well-represented

### How It Works

1. Documents are embedded into dense vectors (e.g., using OpenAI embeddings)
2. Query is also embedded into a dense vector
3. Similarity is calculated using distance metrics (cosine similarity, dot product)
4. Most similar documents are retrieved

### Example

```python
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Create embeddings and vector store
embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
vectorstore = Chroma.from_documents(documents, embedding=embeddings)

# Create dense retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
results = retriever.invoke("What is LangChain used for?")
```

<!-- lesson:page Sparse Retrieval: TF-IDF and BM25 -->
## Sparse Retrieval

### What is Sparse Retrieval?

**Sparse retrieval** is a method of finding information by matching specific keywords or terms in a query with those in documents.

The resulting vectors contain **many zeros**, with only a few non-zero terms, which is why they are said to be **"sparse"**.

### Characteristics

**Strengths:**
- **Precise retrieval**: Matches exact words and terms
- **Better representation of rare words**: Rare terms are better represented in the embeddings
- **More explainable**: Due to the alignment with specific terms, it's easier to understand why documents were retrieved
- **Efficient**: No need for embedding generation

**Limitations:**
- **May miss semantically similar content**: Won't find conceptually related content without exact word matches
- **Less context-aware**: Focuses on keywords rather than meaning

### Sparse Retrieval Methods

There are two main sparse retrieval methods:

#### 1. TF-IDF (Term Frequency-Inverse Document Frequency)

**TF-IDF** creates a sparse vector that measures:
- **Term Frequency (TF)**: How often a term appears in a document
- **Inverse Document Frequency (IDF)**: How rare the term is across all documents

This helps in identifying words that best represent the document's unique content.

**How it works:**
- Terms that appear frequently in a document but rarely in other documents get high scores
- Common words (like "the", "is") get low scores
- Unique, document-specific terms get high scores

#### 2. BM25 (Best Matching 25)

**BM25**, or **best matching 25**, is an improvement on TF-IDF that prevents high-frequency words from being over-emphasized in the encoding.

**Key improvements over TF-IDF:**
- **Saturation**: Prevents very frequent terms from dominating
- **Length normalization**: Accounts for document length
- **Better ranking**: More accurate relevance scoring

**Example scenario:**
When asking "When was football created?" in a paragraph with multiple facts about football:
- BM25 returns the statement with similar terms to the input that were also unique to that statement
- It identifies the most relevant sentence based on term matching and uniqueness

<!-- lesson:page BM25Retriever in LangChain -->
### BM25Retriever in LangChain

#### Step 1: Define Your Text Chunks

Create a list of text chunks to search over:

```python
from langchain_community.retrievers import BM25Retriever

chunks = [
    "LangChain was created to simplify building applications with language models.",
    "LangChain provides tools for document loading, splitting, and retrieval.",
    "Vector databases enable semantic search by storing document embeddings."
]
```

#### Step 2: Create the BM25 Retriever

Build a retriever from the text chunks. The `k` parameter controls how many results to return:

```python
bm25_retriever = BM25Retriever.from_texts(chunks, k=3)
```

#### Step 3: Query the Retriever

Invoke the retriever with a query. BM25 matches based on term frequency and uniqueness:

```python
results = bm25_retriever.invoke("What is LangChain used for?")

print("Most Relevant Document:")
print(results[0].page_content)
# Output: "LangChain was created to simplify building applications with language models."
```

## BM25 in RAG Chains

BM25 can be used in RAG chains just like dense retrievers:

#### Step 1: Create the BM25 Retriever

```python
from langchain_community.retrievers import BM25Retriever

retriever = BM25Retriever.from_documents(
    documents=chunks,
    k=5
)
```

#### Step 2: Create the Prompt Template

Define a prompt that takes both retrieved context and the user's question:

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the question using the provided context."),
    ("human", "Context: {context}\n\nQuestion: {question}\n\nAnswer:")
])
```

#### Step 3: Build the Chain

Wire up the retriever, prompt, LLM, and output parser using LCEL:

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

#### Step 4: Invoke the Chain

```python
answer = chain.invoke("How can LLM hallucination impact a RAG application?")
```

## Concepts Covered

- **Dense Retrieval**: Vector-based semantic search
- **Sparse Retrieval**: Keyword-based exact matching
- **TF-IDF**: Term frequency-inverse document frequency
- **BM25**: Best Matching 25 algorithm
- **Retriever Comparison**: When to use each method
- **RAG Integration**: Using sparse retrievers in RAG chains

<!-- lesson:page When to Use Each Method -->
## When to Use Each Method

### Use Dense Retrieval When:
- You need semantic understanding
- Queries are conceptual rather than keyword-based
- Documents contain related concepts
- You want to find similar content without exact word matches

### Use Sparse Retrieval When:
- You need exact keyword matching
- Queries contain specific technical terms
- Rare words are important
- You need explainable results
- You want to avoid embedding costs

### Combine Both Methods:
- **Hybrid Retrieval**: Use both methods and combine results
- **Best of both worlds**: Semantic understanding + exact matching
- **Improved recall**: Catch more relevant documents

## Best Practices

1. **Choose Based on Use Case**
   - Dense for semantic queries
   - Sparse for keyword queries
   - Hybrid for best results

2. **Tune Parameters**
   - For BM25: Adjust `k` (number of results)
   - For dense: Adjust similarity threshold

3. **Consider Costs**
   - Dense retrieval requires embedding API calls
   - Sparse retrieval is free but requires preprocessing

4. **Test and Compare**
   - Try both methods on your queries
   - Measure retrieval quality
   - Choose based on results

## Summary

This module introduced:
- **Dense retrieval** for semantic similarity
- **Sparse retrieval** for exact keyword matching
- **TF-IDF and BM25** as sparse retrieval methods
- **When to use each method** based on your use case

Understanding both dense and sparse retrieval methods allows you to build more effective RAG applications by choosing the right retrieval strategy for your specific needs.

<!-- lesson:end -->

## Prerequisites

This module builds on concepts from:
- **010-RAG-document-storage**: Understanding embeddings and vector databases
- **011-lcel-retrival-chain**: Understanding retrieval chains

### Setting Up Your Environment

**Complete Setup Steps:**

1. **Create the `.env` file** using the Makefile:
   ```bash
   make setup
   ```
   This creates a `.env` file from `.env.example` (or creates a template if it doesn't exist).

2. **Edit the `.env` file** and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   ```
   > **Note:** This module requires an OpenAI API key for dense retrieval examples. Get your key from: https://platform.openai.com/api-keys

3. **Set up virtual environment and install dependencies:**
   ```bash
   make install
   ```
   This creates a Python virtual environment and installs all required packages.

## Installation

The Makefile automatically sets up a Python virtual environment and installs all dependencies. Simply run:

```bash
make install
```

This will:
1. Create a virtual environment (`venv/`) if it doesn't exist
2. Install/upgrade pip
3. Install all required dependencies from `requirements.txt`

> **Note:** The virtual environment is created automatically and all Makefile commands will use it. You don't need to activate it manually.

### Dependencies

The module requires:
- `langchain-core`: For core functionality
- `langchain-community`: For BM25Retriever
- `langchain-openai`: For OpenAI embeddings (dense retrieval)
- `langchain-chroma`: For vector database (dense retrieval)
- `chromadb`: The Chroma vector database
- `rank-bm25`: For BM25 algorithm implementation
- `python-dotenv`: For environment variable management

All dependencies are listed in `requirements.txt` and installed automatically with `make install`.

### Manual Installation (Alternative)

If you prefer to set up manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Running the Examples

### Using Makefile (Recommended)

The Makefile automatically uses the virtual environment:

```bash
# Run the example (creates venv and installs deps if needed)
make run

# Test your knowledge with the quiz
make quiz

# Complete the coding challenge
make challenge
```

### Manual Execution

If you prefer to run manually:

```bash
# Activate virtual environment
source venv/bin/activate  # On macOS/Linux

# Run the example
python advanced_retrieval_example.py
```

## Code Examples

### Advanced Retrieval Example (`advanced_retrieval_example.py`)

This example demonstrates:
- Dense retrieval using vector embeddings
- Sparse retrieval using BM25
- Comparison of both methods
- Using BM25 in a RAG chain

### Key Components:

1. **Dense Retrieval**:
   ```python
   from langchain_openai import OpenAIEmbeddings
   from langchain_chroma import Chroma

   embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
   vectorstore = Chroma.from_documents(documents, embedding=embeddings)
   retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
   results = retriever.invoke(query)
   ```

2. **Sparse Retrieval (BM25)**:
   ```python
   from langchain_community.retrievers import BM25Retriever

   bm25_retriever = BM25Retriever.from_texts(chunks, k=3)
   results = bm25_retriever.invoke(query)
   ```

3. **BM25 in RAG Chain**:
   ```python
   chain = (
       {"context": bm25_retriever, "question": RunnablePassthrough()}
       | prompt
       | llm
       | StrOutputParser()
   )
   ```

## Common Issues and Solutions

### Issue: BM25 Not Finding Relevant Documents

**Problem:** BM25 returns documents that don't seem relevant.

**Solution:**
- Check if query terms match document terms
- Consider using dense retrieval for semantic queries
- Try hybrid retrieval combining both methods

### Issue: Dense Retrieval Missing Exact Matches

**Problem:** Dense retrieval doesn't find documents with exact keyword matches.

**Solution:**
- Use sparse retrieval for keyword-heavy queries
- Combine with BM25 for hybrid retrieval
- Adjust embedding model if needed

## Next Steps

After completing this module, you can:
- Combine dense and sparse retrieval (hybrid retrieval)
- Build RAG applications with better retrieval quality
- Experiment with different retrieval strategies
- Optimize retrieval for your specific use case

## Quiz

Test your understanding with:

```bash
make quiz
```

## Challenge

Complete the coding challenge:

```bash
make challenge
```

The challenge tests your ability to:
- Create a BM25 retriever
- Query the retriever
- Use it in a RAG chain
