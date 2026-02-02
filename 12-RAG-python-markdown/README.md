# Markdown and Python Document Loaders

This module introduces **specialized document loaders** for Markdown and Python files, along with **language-aware text splitters** that understand code structure. These tools are essential for building RAG applications that work with documentation and codebases.

## Overview

In previous modules, we've covered loading documents from PDF, HTML, and CSV files. This module extends that knowledge to:

- **Markdown files**: Lightweight markup language commonly used for documentation
- **Python files**: Source code files that can be loaded to create code-aware RAG applications

## Improving the Architecture for RAG with Markdown and Python

### Markdown Documents

We discussed above extracting from PDF, HTML, and CSV. But now we will look into other types like **Markdown**.

- **Markdown is a lightweight markup language** for creating formatted documents
- It's often the tool of choice for writing code documentation
- LangChain offers a **Markdown loader** (`UnstructuredMarkdownLoader`) to load Markdown files

### Python Files

Imagine we have a codebase and would like to have a way to talk with it and ask it questions about it. We could achieve this by integrating Python files into a RAG application.

- The **PythonLoader class** and the `.load()` method can be used to load these files into memory
- **Can be tricky during splitting** - regular text splitters may break code structure
- Instead of splitting per text or document, it's **best to use the recursive text splitter with from_language method**
- This ensures code is split at appropriate boundaries (functions, classes, etc.) rather than arbitrary text positions

## Concepts Covered

- **UnstructuredMarkdownLoader**: Loading Markdown documentation files
- **PythonLoader**: Loading Python source code files
- **Language-Aware Splitting**: Using `RecursiveCharacterTextSplitter.from_language()` for code
- **Code Structure Preservation**: Maintaining code structure during splitting

## About Markdown Loaders

### What is Markdown?

Markdown is a lightweight markup language that uses plain text formatting syntax. It's widely used for:

- Documentation (README files, API docs)
- Blog posts and articles
- Technical writing
- Code comments and docstrings

### UnstructuredMarkdownLoader

The `UnstructuredMarkdownLoader` from `langchain_community.document_loaders` loads Markdown files and preserves their structure:

```python
from langchain_community.document_loaders import UnstructuredMarkdownLoader

loader = UnstructuredMarkdownLoader('README.md')
markdown_data = loader.load()
```

**Key Features:**
- Preserves Markdown structure (headers, lists, code blocks)
- Extracts metadata from the document
- Handles various Markdown formats

## About Python Loaders

### PythonLoader

The `PythonLoader` loads Python source files into LangChain documents:

```python
from langchain_community.document_loaders import PythonLoader

loader = PythonLoader('rag.py')
python_data = loader.load()
```

**Key Features:**
- Loads Python source code files
- Preserves code structure
- Useful for creating code-aware RAG applications

### Why Python Files Need Special Handling

Python files have a specific structure:
- Functions and classes define logical boundaries
- Code blocks should be kept together
- Comments and docstrings are important context

Regular text splitters may:
- Break code in the middle of functions
- Split across logical boundaries
- Lose important code structure

## Language-Aware Text Splitting

### RecursiveCharacterTextSplitter.from_language()

For code files, use language-aware splitters that understand the code structure:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import Language

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=300,
    chunk_overlap=100
)

chunks = python_splitter.split_documents(python_data)
```

**Key Benefits:**
- Splits at appropriate code boundaries (functions, classes)
- Preserves code structure
- Maintains context within logical units
- Better for code understanding and retrieval

**Supported Languages:**
- Python (`Language.PYTHON`)
- JavaScript (`Language.JS`)
- TypeScript (`Language.TS`)
- And more...

### When to Use Language-Aware Splitting

**Use language-aware splitters for:**
- Source code files (Python, JavaScript, etc.)
- Code documentation
- Technical documentation with code examples

**Use regular splitters for:**
- Plain text documents
- Markdown documentation (can use regular or language-aware)
- General text content

## Prerequisites

This module builds on concepts from:
- **08-RAG-document-loader**: Understanding document loaders
- **09-RAG-document-splitter**: Understanding text splitting

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
   > **Note:** This module requires an OpenAI API key. Get your key from: https://platform.openai.com/api-keys

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
- `langchain-community`: For document loaders (Markdown and Python)
- `unstructured`: For Markdown loading support
- `markdown`: Required dependency for unstructured markdown support
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
python python_markdown_example.py
```

## Code Examples

### Markdown and Python Loader Example (`python_markdown_example.py`)

This example demonstrates:
- Loading Markdown files with `UnstructuredMarkdownLoader`
- Loading Python files with `PythonLoader`
- Splitting Python code with language-aware splitters
- Splitting Markdown with regular splitters

### Key Components:

1. **UnstructuredMarkdownLoader**: Loads Markdown documentation
   ```python
   from langchain_community.document_loaders import UnstructuredMarkdownLoader
   
   loader = UnstructuredMarkdownLoader('README.md')
   markdown_data = loader.load()
   ```

2. **PythonLoader**: Loads Python source files
   ```python
   from langchain_community.document_loaders import PythonLoader
   
   loader = PythonLoader('rag.py')
   python_data = loader.load()
   ```

3. **Language-Aware Splitter**: Splits code while preserving structure
   ```python
   from langchain_text_splitters import RecursiveCharacterTextSplitter
   from langchain_text_splitters import Language
   
   python_splitter = RecursiveCharacterTextSplitter.from_language(
       language=Language.PYTHON,
       chunk_size=300,
       chunk_overlap=100
   )
   chunks = python_splitter.split_documents(python_data)
   ```

## Use Cases

### Markdown Loaders

- **Documentation RAG**: Create RAG applications from technical documentation
- **Knowledge Bases**: Load README files and documentation into vector stores
- **Content Management**: Process Markdown-based content systems

### Python Loaders

- **Code Q&A**: Answer questions about codebases
- **Code Documentation**: Generate documentation from code
- **Code Analysis**: Analyze and understand codebases
- **Developer Assistants**: Build assistants that understand your code

## Best Practices

1. **Use Language-Aware Splitters for Code**
   - Always use `RecursiveCharacterTextSplitter.from_language()` for code files
   - This preserves code structure and improves retrieval quality

2. **Choose Appropriate Chunk Sizes**
   - For code: Smaller chunks (200-500 characters) work well
   - For documentation: Larger chunks (500-1000 characters) may be better
   - Adjust based on your use case

3. **Maintain Context with Overlap**
   - Use chunk overlap (50-100 characters) to maintain context
   - Especially important for code where functions may span multiple chunks

4. **Preserve Metadata**
   - Keep source file information in metadata
   - This helps with attribution and debugging

## Common Issues and Solutions

### Issue: Code Splitting Breaks Functions

**Problem:** Regular splitters break code in the middle of functions.

**Solution:** Use `RecursiveCharacterTextSplitter.from_language(Language.PYTHON)` to split at appropriate boundaries.

### Issue: Markdown Structure Lost

**Problem:** Markdown formatting is lost during loading.

**Solution:** `UnstructuredMarkdownLoader` preserves Markdown structure. Ensure you're using the correct loader.

### Issue: Import Errors

**Problem:** `UnstructuredMarkdownLoader` not found.

**Solution:** Install `unstructured` package: `pip install unstructured[markdown]`

## Next Steps

After completing this module, you can:
- Combine Markdown and Python loaders with vector stores (from module 010)
- Build complete RAG applications for codebases
- Create documentation Q&A systems
- Explore other language-aware splitters (JavaScript, TypeScript, etc.)

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
- Load Markdown files
- Load Python files
- Use language-aware splitters

## Summary

This module introduced:
- **Markdown loaders** for documentation
- **Python loaders** for source code
- **Language-aware splitters** that preserve code structure
- Best practices for handling code and documentation in RAG applications

These tools enable you to build sophisticated RAG applications that can understand and answer questions about both documentation and codebases.
