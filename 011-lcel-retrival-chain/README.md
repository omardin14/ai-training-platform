# LCEL Retrieval Chain

This module introduces **LCEL Retrieval Chains** - combining document retrieval with LLM generation using LangChain Expression Language (LCEL) to create complete RAG (Retrieval-Augmented Generation) applications.

## What is a Retrieval Chain?

A retrieval chain combines:
- **Document Retrieval**: Finding relevant documents from a vector database
- **Prompt Formatting**: Combining retrieved context with user queries
- **LLM Generation**: Using the LLM to generate answers based on retrieved context

Retrieval chains are the **final step** in building RAG applications - they bring together all the components (loaders, splitters, vector stores) to answer questions using your documents.

![Retrieval Chain](../utils/media/retrieval_chain.png)

## What is LCEL?

**LCEL (LangChain Expression Language)** is a declarative way to compose chains. It allows you to:
- Chain components together using the pipe operator (`|`)
- Use dictionary syntax for multiple inputs
- Create complex workflows with simple, readable code
- Build production-ready chains that are easy to debug and modify

## Concepts Covered

- **LCEL (LangChain Expression Language)**: Chaining components together
- **Retrievers**: Searching vector databases for relevant documents
- **RunnablePassthrough**: Passing values through chains unchanged
- **Dictionary Syntax**: Providing multiple inputs to chains
- **Retrieval Chains**: Complete RAG workflows

## How Retrieval Chains Work

A retrieval chain follows this process:

1. **User Query**: User asks a question
2. **Retrieve Documents**: Retriever searches vector database for relevant documents
3. **Format Prompt**: Combine retrieved context with user question
4. **Generate Answer**: LLM generates answer using the formatted prompt
5. **Return Response**: Return the LLM's answer to the user

### Example Flow:
```
User Question
  ↓
Retriever → Relevant Documents
  ↓
Prompt Template (context + question)
  ↓
LLM → Answer
```

## Prerequisites

This module builds on the concepts from **010-RAG-document-storage**. Make sure you've completed that module first, as we'll use the vector store created there.

### Setting Up Your Environment

**Complete Setup Steps:**

1. **Create the `.env` file** using the Makefile:
   ```bash
   make setup
   ```
   This creates a `.env` file from `.env.example` (or creates a template if it doesn't exist).

2. **Optional: Edit the `.env` file** and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   ```
   > **Note:** If you don't set an API key, the example will use a Hugging Face model instead. OpenAI models are recommended for best results.

3. **Set up virtual environment and install dependencies:**
   ```bash
   make install
   ```
   This creates a Python virtual environment and installs all required packages.

**Model Selection:**
- **If `OPENAI_API_KEY` is set**: Uses OpenAI's GPT-3.5-turbo model (recommended)
- **If `OPENAI_API_KEY` is not set**: Uses Hugging Face's crumb/nano-mistral model

**Alternative: Environment Variable**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

> **Note:** The `.env` file is automatically loaded by the examples using `python-dotenv`. Make sure not to commit your `.env` file to version control!

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
- `langchain-core`: For LCEL and core functionality
- `langchain-community`: For document loaders and Hugging Face support
- `langchain-openai`: For OpenAI models and embeddings
- `langchain-chroma`: For Chroma vector database integration
- `chromadb`: The Chroma vector database
- `langchain-huggingface`: For Hugging Face models (optional)
- `sentence-transformers`: For Hugging Face embeddings (optional)
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

# Or run directly
make all
```

> **Note:** The first time you run any command, it will automatically set up the virtual environment and install dependencies if needed.

### Manual Execution

If you set up the environment manually, activate it first:

```bash
# Activate virtual environment
source venv/bin/activate  # On macOS/Linux

# Run example
python retrieval_chain_example.py
```

## Understanding Retrieval Chain Structure

Let's break down how a retrieval chain works:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Create prompt template
message = """Answer using context: {context}\nQuestion: {question}\nAnswer:"""
prompt_template = ChatPromptTemplate.from_messages([("human", message)])

# Build retrieval chain
retrieval_chain = (
    {
        "context": retriever,  # Retrieve documents
        "question": RunnablePassthrough()  # Pass question through
    }
    | prompt_template  # Format prompt
    | llm  # Generate answer
)

# Use the chain
response = retrieval_chain.invoke("What is machine learning?")
```

### Key Components:

1. **Retriever**: Searches the vector database
   - Takes a question as input
   - Returns relevant documents
   - Configured with `search_type` and `search_kwargs`

2. **Prompt Template**: Formats the prompt
   - Uses `{context}` for retrieved documents
   - Uses `{question}` for user query
   - Combines them into a formatted prompt

3. **LCEL Chain**: Connects components
   - Uses dictionary syntax `{}` for multiple inputs
   - Uses pipe operator `|` to chain components
   - `RunnablePassthrough()` passes values through unchanged

4. **LLM**: Generates the answer
   - Receives formatted prompt with context
   - Generates answer based on retrieved context
   - Returns response

### The Flow:

```
Question: "What is machine learning?"
  ↓
Retriever searches vector database
  ↓
Retrieved Documents: ["Machine learning enables...", "ML uses algorithms..."]
  ↓
Prompt Template formats: "Context: [documents]\nQuestion: What is machine learning?\nAnswer:"
  ↓
LLM generates: "Machine learning is a subset of AI that enables computers to learn..."
```

## Code Examples

### Retrieval Chain Example (`retrieval_chain_example.py`)

This example demonstrates:
- Loading or creating a vector store
- Creating a retriever from the vector store
- Building a prompt template with context and question
- Creating a retrieval chain using LCEL
- Using dictionary syntax and RunnablePassthrough
- Invoking the chain to answer questions

**Key Features:**
- Complete RAG workflow
- Uses LCEL for chaining
- Supports both OpenAI and Hugging Face models
- Shows how to combine retrieval with generation

## Key Concepts Explained

### LCEL (LangChain Expression Language)

LCEL allows you to chain components together using the pipe operator (`|`):

```python
chain = component1 | component2 | component3
```

Each component processes the output of the previous component.

### Dictionary Syntax

When you need multiple inputs, use dictionary syntax:

```python
chain = (
    {
        "input1": component1,
        "input2": component2
    }
    | component3
)
```

This allows `component3` to receive both `input1` and `input2`.

### RunnablePassthrough

`RunnablePassthrough()` passes values through unchanged:

```python
{
    "context": retriever,  # Processes the input
    "question": RunnablePassthrough()  # Passes input through unchanged
}
```

This is useful when you want to pass the original input to a later component.

### Retrieval Chain Pattern

The standard retrieval chain pattern:

```python
retrieval_chain = (
    {
        "context": retriever,  # Retrieve documents based on question
        "question": RunnablePassthrough()  # Keep original question
    }
    | prompt_template  # Format with context and question
    | llm  # Generate answer
)
```

## Quiz

Test your understanding of retrieval chains! Run:

```bash
make quiz
```

The quiz covers:
- What LCEL stands for
- Purpose of RunnablePassthrough
- What retrievers do in retrieval chains

## Challenge

Put your skills to the test! Complete the coding challenge:

```bash
make challenge
```

The challenge will ask you to:
- Create a prompt template
- Import RunnablePassthrough
- Build a retrieval chain
- Invoke the chain

## Next Steps

After completing this module, you'll be ready for:
- **012-RAG-python-markdown**: Advanced RAG techniques
- Building custom RAG applications
- Integrating RAG into production systems

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you've run `make install` to install all dependencies
2. **Vector Store Not Found**: Complete module 010 first to create a vector store, or the example will create sample documents
3. **API Key Errors**: Check your `.env` file if using OpenAI
4. **Chain Errors**: Make sure all components are properly connected with `|`
5. **Response Format**: OpenAI returns `.content`, Hugging Face returns strings

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed: `make install`
2. Verify your `.env` file has the OpenAI API key if using OpenAI
3. Try running the example directly: `python retrieval_chain_example.py`
4. Check the error messages for specific guidance
5. Ensure you've completed module 010 to have a vector store available

## Summary

Retrieval chains enable you to:
- ✅ Combine document retrieval with LLM generation
- ✅ Build complete RAG applications
- ✅ Use LCEL to chain components elegantly
- ✅ Answer questions using retrieved context
- ✅ Create production-ready RAG systems

This completes the RAG pipeline! You now have all the tools to build RAG applications that can answer questions using your own documents!

