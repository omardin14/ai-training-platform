# Advanced Document Splitting

This module introduces **advanced splitting methods** that go beyond simple character-based splitting. These methods address limitations of basic splitters and significantly improve the quality of RAG (Retrieval-Augmented Generation) applications.

<!-- lesson:page Limitations of Character-Based Splitting -->
## Overview

While character-based text splitters are simple and effective for many use cases, they have limitations:
- They don't consider the context of surrounding text
- Related information may be stored and processed separately
- This can lower the quality of RAG applications
- Risk of exceeding model context windows

This module covers two advanced splitting approaches:
1. **Token-based splitting**: Split by tokens instead of characters
2. **Semantic splitting**: Split based on semantic meaning shifts

## Limitations of Character-Based Splitting

Splitting documents with character text splitters has a few limitations:

### Context Ignorance
- Character splitters are executed **without considering the context** of the surrounding text
- Related information will potentially be stored and processed separately
- This will **lower the quality of our RAG application**

### Context Window Risk
- If we split documents using characters rather than tokens, we risk:
  - Retrieving chunks that exceed the model's context window
  - Creating retrieval prompts that exceed the maximum amount of text the model can process
- The **model context window** is the maximum number of tokens a model can process at once

### Example Problem
With a character text splitter with `chunk_size=500` and `chunk_overlap=50`:
- We get chunks containing groups of characters that satisfy the chunking parameters
- But we don't know how many tokens these chunks contain
- A 500-character chunk might be 100 tokens or 200 tokens depending on the content
- This makes it difficult to ensure chunks fit within model limits

<!-- lesson:page Token-Based Splitting -->
## Token-Based Splitting

### What is Token-Based Splitting?

Token-based splitting addresses the context window issue by splitting based on **token count** rather than character count.

**Key Differences:**
- **Character splitting**: `chunk_size=500` means 500 characters
- **Token splitting**: `chunk_size=100` means 100 tokens

### How It Works

When using token-based splitting:
- The `chunk_size` and `chunk_overlap` refer to the **number of tokens** in the chunk
- A `chunk_size` of 100 means we can have a maximum of 100 tokens in the chunk
- This ensures chunks fit within model context windows

### TokenTextSplitter

The `TokenTextSplitter` can be used to perform token splitting:

```python
import tiktoken
from langchain_text_splitters import TokenTextSplitter

# Get the encoding for the target model
encoding = tiktoken.encoding_for_model('gpt-4o-mini')

# Create a token text splitter
token_splitter = TokenTextSplitter(
    encoding_name=encoding.name,
    chunk_size=100,  # 100 tokens
    chunk_overlap=10  # 10 tokens overlap
)

# Split the document
chunks = token_splitter.split_documents([document])
```

### Benefits

- **Respects model context windows**: Chunks are guaranteed to fit within token limits
- **More accurate size control**: Token count is what matters for LLMs
- **Model-specific**: Can use the exact encoding for your target model

<!-- lesson:page Semantic Splitting -->
## Semantic Splitting

### What is Semantic Splitting?

A semantic splitter will **detect shifts in semantic meaning** and perform the splits at those locations.

**Key Concept:**
- Uses an embedding model to generate text embeddings
- Analyzes embeddings to determine where topic shifts occur
- Splits at natural semantic boundaries rather than arbitrary positions

### How It Works

Semantic splitting requires:
1. An **embedding model** to generate text embeddings
2. Analysis of embedding similarities to detect topic shifts
3. Splitting at points where semantic meaning changes

### SemanticChunker

The `SemanticChunker` performs semantic splitting:

```python
from langchain_openai import OpenAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker

# Instantiate an OpenAI embeddings model
embedding_model = OpenAIEmbeddings(
    model='text-embedding-3-small'
)

# Create the semantic text splitter
semantic_splitter = SemanticChunker(
    embeddings=embedding_model,
    breakpoint_threshold_type="gradient",
    breakpoint_threshold_amount=0.8
)

# Split the document
chunks = semantic_splitter.split_documents([document])
```

### Parameters

- **`breakpoint_threshold_type`**: Method for detecting breaks
  - `"gradient"`: Uses gradient-based detection
  - `"percentile"`: Uses percentile-based detection
- **`breakpoint_threshold_amount`**: Threshold value (0.0 to 1.0)
  - Higher values = fewer splits (more conservative)
  - Lower values = more splits (more aggressive)

### Benefits

- **Preserves semantic coherence**: Keeps related information together
- **Natural boundaries**: Splits at topic transitions
- **Better retrieval**: Related information stays in the same chunk
- **Improved RAG quality**: Context is maintained within chunks

## Concepts Covered

- **Token-based splitting**: Splitting by token count instead of character count
- **Tiktoken**: Library for token encoding
- **Semantic splitting**: Splitting based on semantic meaning shifts
- **Embeddings for splitting**: Using embeddings to detect topic boundaries
- **Context window management**: Ensuring chunks fit within model limits

<!-- lesson:page When to Use Each Method -->
## When to Use Each Method

### Character-Based Splitting
- **Use when**: Simple documents, no strict token limits
- **Pros**: Fast, simple, no API calls needed
- **Cons**: May break context, risk of exceeding context windows

### Token-Based Splitting
- **Use when**: Need to ensure chunks fit within model context windows
- **Pros**: Accurate size control, respects token limits
- **Cons**: Requires tiktoken, model-specific encoding

### Semantic Splitting
- **Use when**: Need to preserve semantic coherence, complex documents
- **Pros**: Natural boundaries, better context preservation
- **Cons**: Requires embeddings API, slower, more expensive

## Best Practices

1. **Choose the Right Method**
   - Use token-based splitting when working with specific models
   - Use semantic splitting for complex documents with multiple topics
   - Combine methods when appropriate

2. **Tune Parameters**
   - For token splitting: Match chunk_size to your model's context window
   - For semantic splitting: Adjust threshold based on document complexity

3. **Consider Costs**
   - Semantic splitting requires API calls (embeddings)
   - Token splitting is free but requires tiktoken
   - Character splitting is the fastest and cheapest

4. **Test and Iterate**
   - Try different methods on your documents
   - Measure retrieval quality
   - Adjust based on results

## Summary

This module introduced:
- **Token-based splitting** for accurate size control
- **Semantic splitting** for preserving context
- **Trade-offs** between different splitting methods
- **Best practices** for choosing and tuning splitters

These advanced methods significantly improve RAG application quality by ensuring chunks are appropriately sized and semantically coherent.

<!-- lesson:end -->

## Prerequisites

This module builds on concepts from:
- **09-RAG-document-splitter**: Understanding basic text splitting
- **010-RAG-document-storage**: Understanding embeddings (for semantic splitting)

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
   > **Note:** This module requires an OpenAI API key for semantic splitting. Get your key from: https://platform.openai.com/api-keys

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
- `langchain-community`: For document loaders
- `langchain-openai`: For OpenAI embeddings (semantic splitting)
- `langchain-experimental`: For SemanticChunker
- `tiktoken`: For token encoding
- `pypdf`: For PDF loading
- `unstructured`: For Markdown loading
- `markdown`: For Markdown support
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
python advanced_splitting_example.py
```

## Code Examples

### Advanced Splitting Example (`advanced_splitting_example.py`)

This example demonstrates:
- Loading multiple document types from `utils/docs`
- Token-based splitting with `TokenTextSplitter`
- Semantic splitting with `SemanticChunker`
- Comparison of different splitting methods

### Key Components:

1. **Token-Based Splitting**:
   ```python
   import tiktoken
   from langchain_text_splitters import TokenTextSplitter

   encoding = tiktoken.encoding_for_model('gpt-4o-mini')
   token_splitter = TokenTextSplitter(
       encoding_name=encoding.name,
       chunk_size=100,
       chunk_overlap=10
   )
   chunks = token_splitter.split_documents([document])
   ```

2. **Semantic Splitting**:
   ```python
   from langchain_openai import OpenAIEmbeddings
   from langchain_experimental.text_splitter import SemanticChunker

   embedding_model = OpenAIEmbeddings(model='text-embedding-3-small')
   semantic_splitter = SemanticChunker(
       embeddings=embedding_model,
       breakpoint_threshold_type="gradient",
       breakpoint_threshold_amount=0.8
   )
   chunks = semantic_splitter.split_documents([document])
   ```

## Common Issues and Solutions

### Issue: Tiktoken Encoding Not Found

**Problem:** `KeyError` when using `encoding_for_model()`.

**Solution:** Use fallback encoding:
```python
try:
    encoding = tiktoken.encoding_for_model('gpt-4o-mini')
except KeyError:
    encoding = tiktoken.get_encoding('cl100k_base')
```

### Issue: Semantic Splitting Too Slow

**Problem:** Semantic splitting takes too long.

**Solution:**
- Reduce document size before splitting
- Use a faster embedding model
- Consider token-based splitting for large documents

### Issue: Too Many/Few Semantic Chunks

**Problem:** Semantic splitter creates too many or too few chunks.

**Solution:** Adjust `breakpoint_threshold_amount`:
- Increase (closer to 1.0) for fewer chunks
- Decrease (closer to 0.0) for more chunks

## Next Steps

After completing this module, you can:
- Combine advanced splitting with vector stores
- Build RAG applications with better chunk quality
- Experiment with different splitting strategies
- Optimize splitting for your specific use case

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
- Set up token-based splitting
- Configure semantic splitting
- Use embeddings for splitting
