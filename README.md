# AI Training Platform

A hands-on, interactive training platform for learning AI and LangChain -- with structured courses covering theory through practical implementation.

## Quick Start

```bash
# 1. Set up your API keys
make setup
# Edit .env and add your OpenAI API key

# 2. Launch the interactive learning tool
make learn
```

That's it. `make learn` handles virtual environment creation, dependency installation, and launches the interactive terminal-based learning experience with a course picker.

## Courses

### Getting Started with LangChain (Available)

19 modules progressing from fundamentals to advanced RAG and knowledge graphs:

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
| 16 | Knowledge Graphs | Graph documents, LLM-powered entity extraction |
| 17 | Neo4j Graph Store | Neo4j database, Cypher queries, graph storage |
| 18 | Graph RAG Chain | GraphCypherQAChain, natural language to Cypher |
| 19 | Improving Graph RAG | Few-shot Cypher, fulltext search, advanced prompting |

### LangChain Agents & LangGraph (Available)

7 modules covering agent architectures, custom tools, and LangGraph workflows:

| # | Module | Topics |
|---|--------|--------|
| 01 | ReAct Agents & Custom Tools | ReAct loop, `@tool` decorator, `create_agent`, multi-tool agents |
| 02 | Agent Conversations | Message history, follow-up questions, `HumanMessage`, `AIMessage` |
| 03 | Building Graphs | `StateGraph`, nodes, edges, `START`/`END`, `add_messages`, `.compile()` |
| 04 | Chatbot Responses | `.stream()`, `stream_graph_updates()`, graph visualisation, hallucination awareness |
| 05 | Adding External Tools | Wikipedia tool, `.bind_tools()`, `ToolNode`, `tools_condition`, conditional edges |
| 06 | Memory & Conversation | `MemorySaver`, `checkpointer`, `thread_id`, conversation context, follow-up questions |
| 07 | Multi-Tool Chatbot | `@tool` custom tools, LLM-powered vs pure Python tools, `ToolNode`, `bind_tools`, `MessagesState`, `should_continue`, `call_model`, `app.stream()` |

### AI Theory & Foundations (Available)

Machine learning, LLMs, alignment, prompt engineering, AI safety, and AI agents.

Based on: [The AI Sketchbook](https://medium.com/@omarnour_5895/the-ai-sketchbook-visual-notes-on-the-fundamentals-5f8bd3234bde) | [Inside the Brain of an Agent](https://medium.com/@omarnour_5895/inside-the-brain-of-an-agent-orchestration-tools-and-guardrails-39e67dc3ca76) | [Agentic Applications](https://medium.com/@omarnour_5895/agentic-applications-scaling-protocols-and-production-6da32c75a7f0)

| # | Module | Topics |
|---|--------|--------|
| 01 | Machine Learning Fundamentals | Explicit programming vs ML, three-step learning loop, weights and biases, training data |
| 02 | Large Language Models | Trinity of modern AI, next-word prediction, training at scale, generative vs analytical AI |
| 03 | AI Alignment & Safety | RLHF, human evaluators, preference ranking, fine-tuning, safety boundaries |
| 04 | From Tool to Teammate | Mindset shift, execution partner, thought partner, editor, infinite tutor |
| 05 | Prompt Engineering | ARC framework (Ask, Requirements, Context), iteration, the flipped prompt |
| 06 | AI Pitfalls & Risks | Sycophancy, hallucinations, bias, data privacy |
| 07 | Introduction to AI Agents | Agent anatomy (brain & body), spectrum of agency (levels 0-4), agent vs chatbot |
| 08 | Orchestration & Reasoning | Orchestration layer, Thought-Action-Observation cycle, ReAct framework, chain-of-thought |
| 09 | Agent Tools & Multi-Agent Systems | APIs/extensions, functions, data stores, MCP, Manager and Decentralized patterns |
| 10 | Guardrails & Best Practices | Input/tool/output guardrails, build vs buy, best practices for using and building agents |
| 11 | Agentic Application Architecture | Four layers (interface, prompt, model, storage), three design principles, modularity |
| 12 | Scaling & Failure Modes | Fragile evaluation, intent drift, sycophancy trap, latency, cost explosion, multi-agent patterns |
| 13 | Agent Protocols: MCP & A2A | M x N problem, MCP architecture, three primitives, A2A workflow, agent cards |
| 14 | Production & Operations | Red teaming, shadow deployments, event-driven architecture, graceful failure, least privilege |

## Interactive Learning Tool

`make learn` provides a terminal-based learning experience with:

- **Course Picker** -- Select from available courses (or see what's coming soon)
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
│   └── content/             # Course and module configs
│       ├── courses.py       # Course registry
│       ├── langchain_fundamentals/  # LangChain Fundamentals content
│       │   └── module_XX.py # Per-module quiz, challenge, example configs
│       └── langchain_agents/        # LangChain Agents content
│           └── module_XX.py
├── courses/
│   ├── langchain-fundamentals/      # 19 modules (01–19)
│   │   ├── Makefile.common
│   │   ├── 01-langchain-models/
│   │   │   ├── README.md            # Lesson content (source of truth)
│   │   │   ├── Makefile             # Module-level make targets
│   │   │   ├── *_example.py         # Working code examples
│   │   │   ├── challenge.py         # Coding challenge (fill in XXXX___)
│   │   │   └── challenge_solution.py
│   │   └── ...
│   └── langchain-agents/            # Agent modules
│       ├── Makefile.common
│       ├── 01-react-agents-tools/
│       └── ...
└── utils/
    └── docs/                 # Sample documents for RAG modules
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
