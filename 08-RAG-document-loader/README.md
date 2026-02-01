# Document Loaders

This module introduces **Document Loaders** - tools that extract text content from various file formats for use in RAG (Retrieval-Augmented Generation) applications.

## What are Document Loaders?

Document loaders are specialized tools that:
- **Extract text** from various file formats (PDF, CSV, HTML, etc.)
- **Convert files** into Document objects that LangChain can process
- **Preserve metadata** about the source file (page numbers, file paths, etc.)
- **Enable RAG** by making document content searchable and retrievable

Document loaders are the first step in building RAG applications - they convert your files into a format that can be processed, searched, and used for generation.

## Concepts Covered

- **Document Loaders**: Loading documents from various sources
- **Document Objects**: Understanding the structure of loaded documents
- **Metadata**: Accessing file information alongside content
- **Different Formats**: PDF, CSV, HTML, and text file loaders

## How Document Loaders Work

Document loaders follow a simple pattern:

1. **Create Loader**: Instantiate a loader for your file type
2. **Load Document**: Call `load()` to extract content
3. **Get Documents**: Receive Document objects with content and metadata
4. **Process**: Use documents for RAG, search, or other applications

### Example Flow:
```
File (PDF/CSV/HTML/etc.)
  ↓
Document Loader
  ↓
Document Objects (with page_content and metadata)
  ↓
RAG Application / Search / Generation
```

## Prerequisites

This module is foundational for RAG applications. It doesn't require previous modules, but understanding LangChain basics from earlier modules will be helpful.

### Setting Up Your Environment

**Complete Setup Steps:**

1. **Create the `.env` file** using the Makefile (optional):
   ```bash
   make setup
   ```
   This creates a `.env` file from `.env.example` (or creates a template if it doesn't exist).
   
   > **Note:** Document loaders don't require API keys! They work with local files.

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
- `langchain-community`: For document loaders
- `pypdf`: For PDF file loading
- `unstructured`: For HTML and other unstructured formats
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
python document_loader_example.py
```

## Understanding Document Loader Structure

Let's break down how document loaders work:

```python
# Step 1: Import the loader for your file type
from langchain_community.document_loaders import PyPDFLoader

# Step 2: Create a loader instance
loader = PyPDFLoader("path/to/file.pdf")

# Step 3: Load the document
documents = loader.load()

# Step 4: Access content and metadata
first_doc = documents[0]
print(first_doc.page_content)  # The text content
print(first_doc.metadata)       # File information
```

### Key Components:

1. **Loader Classes**: Different loaders for different file types
   - `PyPDFLoader`: For PDF files
   - `CSVLoader`: For CSV files
   - `UnstructuredHTMLLoader`: For HTML files
   - `TextLoader`: For plain text files

2. **Document Objects**: What loaders return
   - `page_content`: The extracted text content
   - `metadata`: Dictionary with file information
     - `source`: File path or URL
     - `page`: Page number (for PDFs)
     - `row`: Row number (for CSVs)
     - Other format-specific fields

3. **Load Method**: Extracts content from files
   - Returns a list of Document objects
   - Each document represents a page, row, or section

### The Flow:

```
PDF File (3 pages)
  ↓
PyPDFLoader.load()
  ↓
[Document(page_content="...", metadata={page: 1}),
 Document(page_content="...", metadata={page: 2}),
 Document(page_content="...", metadata={page: 3})]
```

## Code Examples

### Document Loader Example (`document_loader_example.py`)

This example demonstrates:
- Loading PDF documents with `PyPDFLoader`
- Loading CSV files with `CSVLoader`
- Loading HTML files with `UnstructuredHTMLLoader`
- Loading text files with `TextLoader`
- Understanding Document object structure
- Accessing content and metadata

**Key Features:**
- Shows multiple loader types
- Demonstrates Document object structure
- Explains metadata fields
- Provides structure examples even without actual files

## Key Concepts Explained

### PDF Loader

`PyPDFLoader` extracts text from PDF files:
```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("document.pdf")
documents = loader.load()
# Each page becomes a separate Document object
```

### CSV Loader

`CSVLoader` converts CSV rows into documents:
```python
from langchain_community.document_loaders.csv_loader import CSVLoader

loader = CSVLoader("data.csv")
documents = loader.load()
# Each row becomes a separate Document object
```

### HTML Loader

`UnstructuredHTMLLoader` extracts text from HTML:
```python
from langchain_community.document_loaders import UnstructuredHTMLLoader

loader = UnstructuredHTMLLoader("page.html")
documents = loader.load()
# HTML content is extracted as text
```

### Text Loader

`TextLoader` loads plain text files:
```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader("document.txt")
documents = loader.load()
# File content becomes a Document object
```

### Document Structure

All loaders return Document objects with:
- **`page_content`**: The extracted text (string)
- **`metadata`**: Dictionary with file information
  - Always includes `source` (file path)
  - Format-specific fields (page, row, etc.)

## Quiz

Test your understanding of document loaders! Run:

```bash
make quiz
```

The quiz covers:
- What document loaders return
- Which loader to use for different file types
- The purpose of document loaders in RAG applications

## Challenge

Put your skills to the test! Complete the coding challenge:

```bash
make challenge
```

The challenge will ask you to:
- Import a document loader
- Create a loader instance
- Load documents
- Access content and metadata

## Next Steps

After completing this module, you'll be ready for:
- **09-RAG-document-splitter**: Splitting documents into smaller chunks
- **010-RAG-document-storage**: Storing documents for retrieval
- **011-lcel-retrival-chain**: Building retrieval chains

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you've run `make install` to install all dependencies
2. **File Not Found**: Ensure the file path is correct and the file exists
3. **PDF Loading Errors**: Make sure `pypdf` is installed: `pip install pypdf`
4. **HTML Loading Errors**: Make sure `unstructured` is installed: `pip install unstructured`
5. **Empty Documents**: Check that the file contains readable content

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed: `make install`
2. Verify the file path is correct and the file exists
3. Try running the example directly: `python document_loader_example.py`
4. Check the error messages for specific guidance
5. Ensure the file format is supported by the loader

## Summary

Document loaders enable you to:
- ✅ Extract text from various file formats
- ✅ Convert files into Document objects
- ✅ Preserve metadata about source files
- ✅ Prepare documents for RAG applications
- ✅ Load documents from PDF, CSV, HTML, and text files

This is the foundation for building RAG applications that can work with your own documents!

