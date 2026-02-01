# Document Splitters

This module introduces **Document Splitters** - tools that break large documents into smaller chunks for processing in RAG (Retrieval-Augmented Generation) applications.

## What are Document Splitters?

Document splitters are essential tools that:
- **Break large documents** into smaller, manageable chunks
- **Preserve context** through chunk overlap
- **Handle different formats** with intelligent splitting strategies
- **Enable efficient retrieval** by creating appropriately-sized chunks

Document splitters are the second step in building RAG applications - after loading documents, you need to split them into chunks that fit within model context limits and can be efficiently retrieved.

## Concepts Covered

- **Character Splitting**: Simple splitting by a single separator
- **Recursive Character Splitting**: Intelligent splitting with multiple separators
- **Chunk Size and Overlap**: Controlling chunk dimensions
- **split_text() vs split_documents()**: Working with strings vs Document objects

## How Document Splitters Work

Document splitters follow this process:

1. **Create Splitter**: Instantiate a splitter with parameters
2. **Set Parameters**: Define chunk_size, chunk_overlap, and separators
3. **Split Content**: Call `split_text()` or `split_documents()`
4. **Get Chunks**: Receive a list of text chunks or Document objects

### Example Flow:
```
Large Document
  ↓
Document Splitter
  ↓
Multiple Chunks (with overlap)
  ↓
RAG Application / Vector Store / Retrieval
```

## Prerequisites

This module builds on the concepts from **08-RAG-document-loader**. Make sure you've completed that module first, as we'll use document loaders to load files before splitting them.

### Setting Up Your Environment

**Complete Setup Steps:**

1. **Create the `.env` file** using the Makefile (optional):
   ```bash
   make setup
   ```
   This creates a `.env` file from `.env.example` (or creates a template if it doesn't exist).
   
   > **Note:** Document splitters don't require API keys! They work with local files.

2. **Set up virtual environment and install dependencies:**
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
- `langchain-core`: For text splitters
- `langchain-community`: For document loaders (used in examples)
- `pypdf`: For PDF file loading (optional, for examples)
- `unstructured`: For HTML and other unstructured formats (optional, for examples)
- `python-dotenv`: For environment variable management (optional)

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
python document_splitter_example.py
```

## Understanding Document Splitter Structure

Let's break down how document splitters work:

```python
# Step 1: Import the splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Step 2: Create a splitter instance
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=100,
    separators=["\n", " ", ""]
)

# Step 3: Split text or documents
chunks = splitter.split_text(text)  # For strings
# or
split_docs = splitter.split_documents(documents)  # For Document objects
```

### Key Components:

1. **CharacterTextSplitter**: Simple splitting by a single separator
   - Uses one separator character
   - Fast and straightforward
   - May break words or sentences

2. **RecursiveCharacterTextSplitter**: Intelligent splitting with multiple separators
   - Tries separators in order of preference
   - Tries to keep sentences/words together
   - More intelligent but slightly slower

3. **Chunk Parameters**:
   - `chunk_size`: Maximum size of each chunk (in characters)
   - `chunk_overlap`: Number of characters to overlap between chunks
   - `separators`: List of separators to try (in order)

4. **Splitting Methods**:
   - `split_text()`: For plain strings, returns list of strings
   - `split_documents()`: For Document objects, returns list of Documents (preserves metadata)

### The Flow:

```
Large Document (1000 characters)
  ↓
RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)
  ↓
[Chunk 1: chars 0-300,
 Chunk 2: chars 200-500 (overlaps 100),
 Chunk 3: chars 400-700 (overlaps 100),
 ...]
```

## Code Examples

### Document Splitter Example (`document_splitter_example.py`)

This example demonstrates:
- Character splitting with `CharacterTextSplitter`
- Recursive character splitting with `RecursiveCharacterTextSplitter`
- Splitting HTML documents loaded from files
- Understanding chunk size and overlap
- Using `split_text()` and `split_documents()`

**Key Features:**
- Shows both simple and recursive splitting
- Demonstrates chunk parameters
- Explains overlap concept
- Shows splitting of loaded documents

## Key Concepts Explained

### CharacterTextSplitter

Simple splitting by a single separator:
```python
from langchain_text_splitters import CharacterTextSplitter

splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=100,
    chunk_overlap=20
)
chunks = splitter.split_text(text)
```

### RecursiveCharacterTextSplitter

Intelligent splitting with multiple separators:
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_text(text)
```

The splitter tries separators in order:
1. First tries `"\n\n"` (paragraph breaks)
2. Then tries `"\n"` (line breaks)
3. Then tries `" "` (spaces)
4. Finally tries `""` (character-by-character)

### Chunk Size and Overlap

- **chunk_size**: Maximum characters per chunk
  - Too large: May exceed model context limits
  - Too small: May lose important context
  - Typical: 500-2000 characters

- **chunk_overlap**: Characters shared between adjacent chunks
  - Prevents losing context at boundaries
  - Helps maintain continuity
  - Typically 10-20% of chunk_size

### split_text() vs split_documents()

- **split_text()**: For plain strings
  ```python
  chunks = splitter.split_text("Your text here")
  # Returns: ["chunk 1", "chunk 2", ...]
  ```

- **split_documents()**: For Document objects
  ```python
  split_docs = splitter.split_documents(documents)
  # Returns: [Document(...), Document(...), ...]
  # Preserves metadata from original documents
  ```

## Quiz

Test your understanding of document splitters! Run:

```bash
make quiz
```

The quiz covers:
- Differences between CharacterTextSplitter and RecursiveCharacterTextSplitter
- Purpose of chunk_overlap
- split_text() vs split_documents()

## Challenge

Put your skills to the test! Complete the coding challenge:

```bash
make challenge
```

The challenge will ask you to:
- Import a document splitter
- Create a splitter instance
- Split documents
- Understand chunk parameters

## Next Steps

After completing this module, you'll be ready for:
- **010-RAG-document-storage**: Storing documents for retrieval
- **011-lcel-retrival-chain**: Building retrieval chains
- **012-RAG-python-markdown**: Advanced RAG techniques

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you've run `make install` to install all dependencies
2. **Chunks Too Large**: Reduce `chunk_size` parameter
3. **Chunks Too Small**: Increase `chunk_size` parameter
4. **Lost Context**: Increase `chunk_overlap` parameter
5. **Metadata Lost**: Use `split_documents()` instead of `split_text()` when working with Document objects

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed: `make install`
2. Verify the file paths are correct if loading documents
3. Try running the example directly: `python document_splitter_example.py`
4. Check the error messages for specific guidance
5. Adjust chunk_size and chunk_overlap parameters based on your needs

## Summary

Document splitters enable you to:
- ✅ Break large documents into manageable chunks
- ✅ Preserve context through chunk overlap
- ✅ Use intelligent splitting strategies
- ✅ Handle different document formats
- ✅ Prepare documents for vector storage and retrieval

This is an essential step for building effective RAG applications that can handle large documents!

