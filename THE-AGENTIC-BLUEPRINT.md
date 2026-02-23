# The Agentic Blueprint

A reference template for building production-ready agentic systems with LangChain and LangGraph. Drop this into any project repo and use it as your checklist.

---

## 1. Do You Need an Agent?

Before writing code, decide whether an agent is the right solution.

| Question | No → Use a chain/chatbot | Yes → Use an agent |
|----------|--------------------------|-------------------|
| Does the task need tools (APIs, databases, code execution)? | | |
| Does it require multi-step reasoning with branching logic? | | |
| Must it make autonomous decisions about what to do next? | | |

If all answers are "no", a chain or chatbot is sufficient. If any answer is "yes", build an agent.

**Agent = Brain + Body.** The brain is the LLM (reasons, plans, decides). The body is the tools (acts, queries, executes). Both are required.

### Levels of Agency

| Level | What the LLM Controls | Example |
|-------|----------------------|---------|
| 0 | Nothing -- fixed pipeline | `prompt \| llm \| parser` chain |
| 1 | Which route to take | Request router |
| 2 | Which tools to call | ReAct agent with tools |
| 3 | Its own loop + replanning | LangGraph with conditional edges |
| 4 | Coordinates other agents | Multi-agent supervisor |

Start at the lowest level that solves the problem. Higher autonomy = higher unpredictability.

### The ReAct Loop

The foundational reasoning pattern for any agent:

```
Thought → Action → Observation → (repeat until done)
```

1. **Thought** -- reason about the current state and what to do next
2. **Action** -- call a tool or take a step
3. **Observation** -- see the result, decide whether to continue or answer

---

## 2. Architecture

### Four Layers

Structure every agentic application into four independent layers:

| Layer | What It Contains | Key Decisions |
|-------|-----------------|---------------|
| **Interface** | Chat UI, API endpoints, voice, CLI | Hybrid: free-text + structured UI (dropdowns, confirmation buttons, sliders) |
| **Prompt Construction** | System messages, templates, few-shot examples, context assembly | Persona, constraints, objectives defined via system messages |
| **Model** | LLM provider, temperature, routing, fallbacks | Remote (OpenAI, Anthropic, Google) vs self-hosted; model tiering per task |
| **Data & Storage** | Vector stores, SQL databases, memory, knowledge bases, ephemeral cache | What to persist, what to cache, what to throw away |

Keep these layers **decoupled**. Each can be developed, tested, swapped, and scaled independently.

### Three Design Principles

1. **Robust Infrastructure** -- scalable compute, reliable deployment pipelines with rollback capability, agent frameworks (LangChain, LangGraph)
2. **Modularity** -- decoupled UI/agent logic/data stores, one agent per domain, avoid the God Agent anti-pattern
3. **Continuous Evaluation** -- quantitative metrics (success rate, latency, cost per interaction) + qualitative feedback (thumbs up/down), deploy-measure-improve loop

### Multi-Agent Patterns

| Pattern | How It Works | Best For |
|---------|-------------|----------|
| **Manager** | Central agent delegates to specialists, synthesises results | Consistent UX, controlled output |
| **Decentralized** | Triage agent hands off, specialist owns conversation | Deep domain expertise |
| **Network/Swarm** | Peers hand off freely, no hierarchy | Flexible support escalation |
| **Supervisor** | Hierarchical delegation, workers return results | Research/writing pipelines |

### Anti-Pattern: The God Agent

One agent handling everything = confusion at scale, single point of failure, impossible to improve. Decompose into specialised agents with narrow, well-defined scopes.

---

## 3. Model & Prompting

### Model Providers

```python
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
response = llm.invoke("Hello")
print(response.content)
```

`.invoke()` is the universal method. Swap providers by changing the class.

### Techniques

| Technique | What It Is | When to Use |
|-----------|-----------|-------------|
| **ARC Framework** | Structure prompts with Ask (what), Requirements (constraints), Context (background) | Every prompt you write |
| **ChatPromptTemplate** | Template with `{variables}` for system + human messages via `.from_messages()` | Reusable prompt patterns |
| **Few-Shot Prompting** | Provide 2-3 input/output examples to guide format and behaviour (`FewShotPromptTemplate`) | Classification, extraction, structured output |
| **Chain-of-Thought** | Instruct the LLM to reason step-by-step before answering ("think step by step") | Complex reasoning, math, multi-hop questions |
| **LCEL Pipe Operator** | Compose chains with `prompt \| llm \| parser` -- each component receives the previous output | All LangChain composition |
| **StrOutputParser** | Extracts plain text from LLM response objects | End of most chains |
| **Sequential Chains** | Multi-step processing with dictionary syntax `{"key": chain}` to pass outputs between chains | Multi-stage pipelines |
| **The Flipped Prompt** | Ask the AI what information it needs from you before answering | Complex/ambiguous tasks |
| **Iterative Prompting** | Start broad, evaluate output, refine the prompt, repeat until quality converges | Prompt development workflow |
| **Neutral Prompts** | Avoid leading phrasing that biases the LLM toward a particular answer | Evaluation prompts, unbiased analysis |

---

## 4. Agent Graph (LangGraph)

### Core Setup

```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
model_with_tools = llm.bind_tools(tools)

graph = StateGraph(MessagesState)
```

`MessagesState` provides a built-in `messages` list with automatic accumulation via `add_messages`. Use it as default unless you need custom state fields.

### The Two Core Nodes

```python
def call_model(state: MessagesState):
    """Call the LLM with current messages."""
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: MessagesState):
    """Route: tools if tool_calls present, otherwise END."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END
```

### Wiring the Graph

```python
tool_node = ToolNode(tools)

graph.add_node("agent", call_model)
graph.add_node("tools", tool_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, ["tools", END])
graph.add_edge("tools", "agent")

app = graph.compile()
```

```
    START → agent ──should_continue?──→ END
               ▲          │
               │       "tools"
               │          ▼
               └─────── tools
```

This is the canonical ReAct agent graph. Every agent you build starts from this pattern.

### Graph Visualisation

```python
from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))
```

Always visualise during development. It catches wiring mistakes before they become runtime bugs.

---

## 5. Tools

### Creating Tools

```python
from langchain_core.tools import tool

@tool
def search_database(query: str) -> str:
    """Search the product database for items matching the query."""
    return results
```

The **docstring is critical** -- the LLM reads it to decide when to use the tool. Write it as if explaining the tool to a colleague.

### Two Types

| Type | How It Works | Example | When to Use |
|------|-------------|---------|-------------|
| **LLM-powered** | Calls the model internally | Summariser, classifier, translator | Task requires language understanding |
| **Pure Python** | Deterministic code, no LLM call | Calculator, API wrapper, formatter | Task has predictable logic |

**Default to pure Python.** LLM-powered tools add cost and latency.

### Connecting to the Graph

```python
from langgraph.prebuilt import ToolNode

tools = [tool_a, tool_b, tool_c]
tool_node = ToolNode(tools)
model_with_tools = llm.bind_tools(tools)
```

`bind_tools` registers tool schemas with the LLM. `ToolNode` executes whatever tool calls the LLM makes.

### Three Categories of Tools

| Category | What It Is | Examples |
|----------|-----------|----------|
| **Extensions** | External API connections | Web search, email, Slack, payment gateways, `WikipediaQueryRun` |
| **Functions** | Executable code | Calculators, formatters, validators, data transformations |
| **Data Stores** | Information retrieval | Vector databases, SQL databases, knowledge bases, file systems |

### MCP (Model Context Protocol)

Solves the M x N integration problem -- tools expose a standard interface instead of custom integrations per agent.

| Component | Role |
|-----------|------|
| **Host** | The AI application (brain) |
| **MCP Client** | Translator between host and server |
| **MCP Server** | Gateway to the data source or tool |

Three primitives: **Resources** (read-only data), **Tools** (executable actions), **Prompts** (reusable workflow templates).

Transport: **Stdio** (local, fast) or **SSE** (remote, cloud agents).

Security: The MCP **server** dictates what data/actions are available and enforces permissions. The client can only use what the server exposes.

### A2A (Agent-to-Agent Protocol)

Standardises how agents discover and communicate with each other. Workflow: Discovery → Negotiation → Execution → Delivery. Key components: Agent Card (identity), Agent Executor (task packaging), Event Queue (progress tracking), Artifact (deliverable).

MCP = agent-to-data. A2A = agent-to-agent. They are complementary.

---

## 6. Memory & Streaming

### MemorySaver -- Conversation Persistence

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
app = graph.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "user-123"}}
app.invoke({"messages": [("human", "My name is Omar")]}, config)
app.invoke({"messages": [("human", "What is my name?")]}, config)  # Remembers
```

Same `thread_id` = same conversation. Different `thread_id` = fresh session. For production, swap `MemorySaver` (in-memory) for a database-backed store.

### Streaming

```python
from langchain_core.messages import AIMessageChunk, HumanMessage

for chunk, metadata in app.stream(
    {"messages": [HumanMessage(content="Explain gradient descent")]},
    config,
    stream_mode="messages",
):
    if isinstance(chunk, AIMessageChunk) and chunk.content:
        print(chunk.content, end="", flush=True)
```

| Method | Returns | Best For |
|--------|---------|----------|
| `app.invoke()` | Complete final state | Batch processing, testing |
| `app.stream()` | Iterator of `(message, metadata)` tuples | Interactive UIs, real-time display |

Filter `HumanMessage` and `ToolMessage` from the stream -- only display final AI responses.

---

## 7. RAG (Retrieval-Augmented Generation)

RAG (Retrieval-Augmented Generation) grounds LLM responses in real data by retrieving relevant documents and injecting them into the prompt as context.

### The Pipeline

```
Load → Split → Embed → Store → Retrieve → Generate
```

| Step | What to Do | Key Tools |
|------|-----------|-----------|
| **Load** | Ingest documents — each loader returns `Document` objects with `.page_content` (text) and `.metadata` (source, page, etc.) | `PyPDFLoader`, `TextLoader`, `CSVLoader`, `PythonLoader`, `UnstructuredMarkdownLoader` |
| **Split** | Break into chunks | `RecursiveCharacterTextSplitter`, `TokenTextSplitter`, `SemanticChunker` |
| **Embed** | Convert to vectors | `OpenAIEmbeddings`, `HuggingFaceEmbeddings` |
| **Store** | Save in vector database | `Chroma.from_documents()`, `FAISS` |
| **Retrieve** | Find relevant chunks | `vectorstore.as_retriever(search_kwargs={"k": 3})` |
| **Generate** | Feed chunks + query to LLM | LCEL chain |

### The LCEL Retrieval Chain

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
answer = chain.invoke("What is the refund policy?")
```

### Chunking Strategy

| Splitter | How It Works | Best For |
|----------|-------------|----------|
| `RecursiveCharacterTextSplitter` | Tries multiple separators in order (`\n\n`, `\n`, ` `, etc.) | General text (default choice) |
| `RecursiveCharacterTextSplitter.from_language()` | Splits at function/class boundaries for code | Python, Markdown, JS, etc. |
| `TokenTextSplitter` | Splits by token count (fits model context windows) | Token-budget-sensitive pipelines |
| `SemanticChunker` | Detects semantic meaning shifts using embeddings | Topic-based documents |

Parameters: `chunk_size` (500-1000 chars typical), `chunk_overlap` (50-200 chars typical).

### Retrieval Strategies

| Strategy | How It Works | Best For |
|----------|-------------|----------|
| **Dense** (default) | Embedding similarity search (`OpenAIEmbeddings` + `Chroma`) | Semantic meaning, paraphrased queries |
| **Sparse** (BM25) | Keyword/term frequency matching (`BM25Retriever.from_documents()`) | Exact terms, names, codes, rare words |
| **Hybrid** | Combines dense + sparse results | Best overall accuracy |

### Knowledge Graphs

For structured relationships that vectors cannot capture. Use when data has entity relationships (org charts, product catalogues, compliance rules).

**Graph RAG vs Vector RAG:** Vector RAG matches semantic similarity (good for "find documents about X"). Graph RAG traverses explicit relationships (good for "how does X relate to Y?"). Use vector RAG as default; add graph RAG when your data has rich relational structure.

| Component | What It Does |
|-----------|-------------|
| `LLMGraphTransformer` | Extracts entities and relationships from text |
| `Neo4jGraph` | Connects to Neo4j database, stores graph documents |
| `GraphCypherQAChain` | Translates natural language → Cypher query → natural language answer |
| `validate_cypher=True` | Auto-corrects relationship direction errors |
| `exclude_types` | Removes node types from schema to reduce LLM search space |
| Few-shot Cypher | Example question-to-Cypher pairs via `FewShotPromptTemplate` + `cypher_prompt` param |

---

## 8. Guardrails

### Three Lines of Defence

| Layer | When It Runs | What to Implement |
|-------|-------------|------------------|
| **Input** | Before the LLM sees the prompt | Relevance classifier, safety classifier, blocklists, input length caps, PII redaction |
| **Tool** | When the agent calls a tool | Risk-level scoping, human-in-the-loop for destructive actions |
| **Output** | Before the response reaches the user | PII filters, hallucination detection, content validation, brand alignment |

### Build vs Buy

Start with built-in/third-party guardrail libraries (e.g. Guardrails AI, NeMo Guardrails) for common patterns (PII detection, content safety). Build custom only when your domain has unique requirements that off-the-shelf solutions cannot cover. Evaluate: maintenance cost, latency overhead, false-positive rate.

### Risk Levels for Tool Guardrails

| Risk | Actions | Guardrail |
|------|---------|-----------|
| **Low** | Read, search, lookup | Auto-execute |
| **Medium** | Update, notify, draft emails | Log and monitor |
| **High** | Delete, transfer funds, send external messages | Human approval required |

### Human-in-the-Loop Pattern

```python
def should_continue(state):
    last = state["messages"][-1]
    if last.tool_calls:
        if last.tool_calls[0]["name"] in HIGH_RISK_TOOLS:
            return "human_review"
        return "tools"
    return END
```

### LLM Pitfalls to Guard Against

| Pitfall | What Happens | Mitigation |
|---------|-------------|------------|
| **Hallucination** | Confidently states false information | Ground in retrieved context (RAG), require citations |
| **Sycophancy** | Agrees with the user even when wrong | Push-back instructions in system prompt, adversarial testing |
| **Bias** | Reproduces biases from training data | Diverse evaluation datasets, bias-specific red teaming |
| **Data Privacy** | Exposes PII or proprietary data | PII filters, treat the chat window like a public bulletin board, enterprise zero-retention plans, user opt-out for data collection |

---

## 9. Evaluation & Testing

### RAGAS Metrics (for RAG pipelines)

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| **Faithfulness** | Does the answer stick to the retrieved context? (detects hallucination) | > 0.8 |
| **Answer Relevancy** | Does the answer address the question? | > 0.8 |
| **Context Precision** | Are the retrieved chunks relevant? (considers ordering) | > 0.7 |
| **Context Recall** | Did we retrieve all the relevant information? | > 0.7 |

```python
from ragas import evaluate
from ragas.metrics import faithfulness, context_precision
result = evaluate(dataset, metrics=[faithfulness, context_precision])
```

Use `temperature=0` for all evaluation LLM calls to ensure deterministic, reproducible results.

### Testing Layers

| Layer | What It Tests | How |
|-------|--------------|-----|
| **Unit tests** | Prompt formatting, tool connections | Standard test frameworks |
| **Integration tests** | Full end-to-end flow | Run the compiled graph with test inputs |
| **Golden datasets** | Curated question-answer pairs (regression detection) | Run after every change, alert on metric drops |
| **LLM-as-Judge** | Second LLM grades the production model's answers | Scales beyond human review, but has its own biases |
| **Red teaming** | Adversarial attacks on your own agent | Prompt injection, jailbreaking, edge cases, emotional inputs |
| **Global simulation** | Test entire multi-agent system end-to-end with realistic scenarios | Catches integration failures, timing issues, and emergent behaviour |

### Red Teaming Checklist

- Prompt injection ("Ignore your instructions and...")
- Jailbreaking (roleplay scenarios to bypass safety)
- Messy inputs (typos, slang, code-switching, emojis)
- Multi-language queries
- Extremely long messages
- Adversarial inputs designed to trigger hallucination or bias

### Fragile Evaluation

LLM outputs are probabilistic. A test that passes 9/10 times is not flaky -- it is revealing real variance. Use **statistical thresholds** instead of exact matches. Run evaluations **multiple times**. Track **trends** rather than individual results.

---

## 10. Production & Deployment

### Five Steps to Production

| Step | What to Do |
|------|-----------|
| 1. **Red team** | Attack the agent with adversarial, emotional, and edge-case inputs |
| 2. **Test everything** | Unit tests, integration tests, golden datasets, LLM-as-Judge |
| 3. **Guardrails + observability** | Content filters, token limits, API rate caps, interaction logging |
| 4. **Shadow deploy** | Process real traffic, log responses, do NOT show to users -- compare against production |
| 5. **Deploy with strategy** | A/B testing, phased rollout (5% → 25% → 100%), human-in-the-loop for high-stakes |

### Five Failure Modes to Monitor

| Failure Mode | What Happens | Mitigation |
|-------------|-------------|------------|
| **Fragile evaluation** | Tests pass inconsistently | Stress-test with chaotic/multilingual/adversarial inputs |
| **Intent drift** | Agent gradually drifts from intended behaviour | Strict guardrails in system prompt, scope detection classifier, regular golden dataset checks |
| **Sycophancy trap** | Agent tells users what they want to hear | Weighted metrics (truth > charm), hybrid review (human + automated) |
| **Latency explosion** | Multi-step reasoning takes too long | Aggressive caching, model tiering (lightweight for simple tasks), parallel tool calls |
| **Cost explosion** | Uncontrolled LLM calls | Cost-aware architecture ("Does this need an LLM?"), token budgets per interaction/session, usage limits |

### Event-Driven Architecture

At scale, agents should communicate through an **event bus** (publish/subscribe) rather than direct calls. This decouples agents, enables parallel execution, and makes the system easier to scale and debug.

### Graceful Degradation

Every failure needs a fallback:

| Failure Type | Strategy |
|-------------|----------|
| Tool call failure | Retry with exponential backoff, queue management |
| Auth/security risk | Unique agent IDs for traceability, least privilege, sandboxed environments |
| Model unavailable | Fallback chain: primary model → backup model → static response |
| General | Cached data fallback → simplified prompt retry → human escalation |

### Zero-Downtime Deployments

Use **blue-green** or **canary** deployment strategies so updates never interrupt running conversations. Route a small percentage of traffic to the new version, monitor metrics, and gradually shift 100% only after confidence thresholds are met. Always maintain a rollback path.

### LangSmith -- Observability

Use LangSmith for tracing, monitoring, and debugging LangChain/LangGraph applications. It logs every chain step, tool call, and LLM invocation, making it easy to pinpoint failures, latency bottlenecks, and unexpected behaviour. Integrate early — debugging agent issues without traces is guesswork.

### LangGraph Platform

For deploying LangGraph agents at scale, LangGraph Platform provides managed infrastructure with built-in persistence, streaming, and human-in-the-loop workflows. Consider it when moving from local prototypes to production services.

### Production Principles

1. Modular architecture (one agent per domain)
2. Standard protocols (MCP for data, A2A for agent collaboration)
3. Rigorous testing (red team, golden datasets, shadow deployments)
4. Graceful failure (retry, queue, escalate -- never leave the user staring at an error)
5. Continuous measurement (metrics, feedback, iterate)

---

## Quick Reference: All Techniques

### Prompting & Chains
`ChatPromptTemplate` | `FewShotPromptTemplate` | `PromptTemplate` | ARC framework | `.from_messages()` | pipe operator `|` | `StrOutputParser` | sequential chains | dictionary syntax | the flipped prompt | chain-of-thought | iterative prompting | neutral prompts

### Models
`ChatOpenAI` | `HuggingFaceEndpoint` | `.invoke()` | `.content` | temperature | model tiering

### Agent Graph
`StateGraph` | `MessagesState` | `START` / `END` | `.add_node()` | `.add_edge()` | `.add_conditional_edges()` | `.compile()` | `should_continue` | `call_model` | `Annotated[list, add_messages]`

### Tools
`@tool` decorator | `ToolNode` | `.bind_tools()` | `tools_condition` | `create_react_agent` | `load_tools` | docstring-based selection | LLM-powered vs pure Python

### Memory & Streaming
`MemorySaver` | `checkpointer` | `thread_id` | `app.stream()` | `stream_mode="messages"` | `AIMessageChunk` | `HumanMessage` filtering

### RAG Pipeline
`PyPDFLoader` | `TextLoader` | `CSVLoader` | `PythonLoader` | `UnstructuredMarkdownLoader` | `RecursiveCharacterTextSplitter` | `TokenTextSplitter` | `SemanticChunker` | `Language.PYTHON` | `OpenAIEmbeddings` | `HuggingFaceEmbeddings` | `Chroma` | `FAISS` | `RunnablePassthrough` | `BM25Retriever` | hybrid retrieval

### Knowledge Graphs
`LLMGraphTransformer` | `GraphDocument` | `Neo4jGraph` | `GraphCypherQAChain` | Cypher queries | `validate_cypher` | `exclude_types` | `include_source` | `baseEntityLabel` | few-shot Cypher

### Evaluation
RAGAS | `faithfulness` | `context_precision` | `EvaluatorChain` | golden datasets | LLM-as-Judge | red teaming | global simulation | `temperature=0` for eval

### Guardrails
Input/tool/output layers | risk levels | relevance classifier | safety classifier | PII filters | human-in-the-loop | content validation | build vs buy

### Production
Shadow deployment | canary rollout | zero-downtime deployment | event-driven architecture | graceful degradation | exponential backoff | least privilege | LangSmith | LangGraph Platform | MCP | A2A | agent cards
