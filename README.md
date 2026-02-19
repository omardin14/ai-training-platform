# LangChain Training Course

A hands-on, interactive training course for learning LangChain -- from basic model usage through RAG (Retrieval-Augmented Generation) and evaluation.

## Quick Start

```bash
# 1. Set up your API keys
make setup
# Edit .env and add your OpenAI API key

# 2. Launch the interactive learning tool
make learn
```

That's it. `make learn` handles virtual environment creation, dependency installation, and launches the interactive terminal-based learning experience.

## What's Inside

The course covers 15 modules, progressing from fundamentals to advanced RAG techniques:

| # | Module | Topics |
|---|--------|--------|
| 01 | LangChain Models | OpenAI and Hugging Face model providers, `.invoke()` |
| 02 | Prompt Templates | `ChatPromptTemplate`, message roles, template variables |
| 03 | Prompt Chains | Pipe operator (`\|`), chaining prompts with models |
| 04 | Few-Shot Prompts | `FewShotPromptTemplate`, example-based prompting |
| 05 | Sequential Chains | Multi-step chains, `StrOutputParser`, dictionary syntax |
| 06 | ReAct Agents | Reasoning + Acting, `create_react_agent`, tool use |
| 07 | Custom Agent Tools | `@tool` decorator, building custom tools for agents |
| 08 | RAG: Document Loaders | `PyPDFLoader`, `TextLoader`, `CSVLoader` |
| 09 | RAG: Document Splitters | `RecursiveCharacterTextSplitter`, chunk size and overlap |
| 10 | RAG: Document Storage | Embeddings, Chroma vector database |
| 11 | LCEL Retrieval Chain | `RunnablePassthrough`, retrieval chain composition |
| 12 | RAG: Python & Markdown | `PythonLoader`, `UnstructuredMarkdownLoader`, language-aware splitting |
| 13 | Advanced Splitting | Token-based splitting, semantic chunking |
| 14 | Advanced Retrieval | Dense vs sparse retrieval, BM25, TF-IDF |
| 15 | RAG Evaluation | Faithfulness, context precision, RAGAS framework |

## Interactive Learning Tool

`make learn` provides a terminal-based learning experience with:

- **Lessons** -- Theory content rendered as styled markdown pages
- **Quizzes** -- Multiple-choice questions with arrow-key selection and instant feedback
- **Coding Challenges** -- Fill-in-the-blank exercises with inline validation
- **Run Examples** -- Execute module example scripts directly

Navigate with arrow keys, no need to leave the tool.

## Project Structure

```
.
├── Makefile                 # Root Makefile (make learn, make run, etc.)
├── Makefile.common          # Shared Makefile targets for modules
├── requirements.txt         # Consolidated Python dependencies
├── .env.example             # API key template
├── learn.py                 # Entry point for make learn
├── learn/                   # Interactive learning tool package
│   ├── app.py               # Main application loop
│   ├── ui.py                # Rich + InquirerPy rendering
│   ├── parser.py            # README.md lesson page parser
│   └── content/             # Module configs (quiz questions, challenge hints)
├── 01-langchain-models/     # Module directories
│   ├── README.md            # Lesson content (source of truth)
│   ├── Makefile             # Module-level make targets
│   ├── openai_example.py    # Working code examples
│   ├── challenge.py         # Coding challenge (fill in XXXX___)
│   └── challenge_solution.py
├── 02-prompt-templates/
│   └── ...
├── ...
└── utils/
    └── docs/                # Sample documents for RAG modules
```

## Prerequisites

- **Python 3.10+**
- **OpenAI API key** -- Required for most modules. Get one at [platform.openai.com](https://platform.openai.com/api-keys)
- **Hugging Face token** (optional) -- For module 01's Hugging Face example. Get one at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

## Setup

```bash
# Create .env file from template
make setup

# Edit .env and add your API keys
# OPENAI_API_KEY=sk-...
```

## Other Commands

```bash
make learn            # Interactive learning tool
make run M=01         # Run module 01 examples directly
make install M=01     # Install dependencies for a module
make clean M=01       # Clean a module's venv and cache
make list             # Show all available modules
```

## How Lessons Work

Each module's `README.md` is the single source of truth for lesson content. HTML comment markers (`<!-- lesson:page Title -->`) delineate lesson pages, and `<!-- lesson:end -->` separates theory from setup instructions. The `learn/parser.py` module parses these at runtime -- edit a README and the changes appear immediately in `make learn`.
