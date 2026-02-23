# Multi-Tool Chatbot

This module covers how to build a chatbot that **automatically selects the right tool** for each query and routes messages through a structured workflow. You will learn how to:

- Create **LLM-powered tools** that invoke the language model internally
- Create **pure Python tools** that use standard code logic
- Combine multiple tools using **ToolNode** and **bind_tools**
- Use **MessagesState** for cleaner state management
- Write a **should_continue** stopping function and a **call_model** dynamic dispatcher
- Wire the full workflow with **conditional edges** and **MemorySaver**
- **Stream responses** in real time with `app.stream()` and `stream_mode="messages"`

<!-- lesson:page Why Build a Multi-Tool Chatbot? -->

## Why Build a Multi-Tool Chatbot?

In previous modules we built chatbots with a single external tool — the Wikipedia lookup. That works well for factual queries, but real-world assistants need **multiple capabilities**.

### The Problem

A single-tool chatbot can only do one thing. Ask it to explain a concept and it searches Wikipedia. Ask it to analyse some text and it still searches Wikipedia — even though no search is needed.

### The Solution

A **multi-tool chatbot** registers several tools, each with a clear name and description. The LLM reads this metadata and **routes each query to the best tool automatically**.

```
User: "What does gradient descent mean?"
  → LLM picks: concept_lookup  (needs language understanding)

User: "How many words are in this sentence?"
  → LLM picks: char_counter  (needs Python logic, no LLM)

User: "Tell me about the Apollo programme"
  → LLM picks: wikipedia_tool  (needs factual lookup)
```

### Two Types of Custom Tool

| Type | How It Works | Best For |
|------|-------------|----------|
| **LLM-powered** | Calls the language model inside the tool | Explanations, summaries, creative tasks |
| **Pure Python** | Uses standard code logic, no LLM call | Counting, calculations, string operations |

Both types look the same to the LLM — it picks based on the tool's **name** and **docstring**, not its implementation.

<!-- lesson:page Creating Custom Tools with @tool -->

## Creating Custom Tools with @tool

LangChain provides the `@tool` decorator to turn any Python function into a tool the LLM can call. The decorator reads three things:

1. **Function name** — becomes the tool name the LLM sees
2. **Type hints** — tells the LLM what input to provide
3. **Docstring** — describes when and how to use the tool

### An LLM-Powered Tool: concept_lookup

This tool takes a technical term and asks the LLM to explain it simply:

```python
from langchain_core.tools import tool

@tool
def concept_lookup(topic: str) -> str:
    """Look up and explain a technical concept in simple terms."""
    try:
        answer = llm.invoke(
            f"Explain the concept of {topic} in 2-3 simple sentences."
        )
        return answer.content
    except Exception as e:
        return f"Error looking up concept: {str(e)}"
```

The `@tool` decorator exposes `concept_lookup` to the LLM. When a user asks "what is backpropagation?", the LLM sees the docstring and knows this tool handles concept explanations.

Notice the **try-except block** — if the inner LLM call fails, the tool returns an error message instead of crashing the entire chatbot.

### A Pure Python Tool: char_counter

This tool counts characters, words, and unique words using only Python — no LLM needed:

```python
@tool
def char_counter(text: str) -> str:
    """Count the number of characters, words, and unique words in a text."""
    chars = len(text)
    words = text.split()
    word_count = len(words)
    unique_count = len(set(w.lower() for w in words))
    return (
        f"'{text}' has {chars} characters, "
        f"{word_count} words, and {unique_count} unique words."
    )
```

The LLM never runs inside this tool. It uses `len()`, `split()`, and `set()` — standard Python. This makes it **fast**, **deterministic**, and **free** (no API tokens consumed).

<!-- lesson:page Combining Tools with ToolNode -->

## Combining Tools with ToolNode

Now we combine all three tools — the Wikipedia tool from the previous module, our LLM-powered tool, and our Python tool — into a single chatbot.

### Step 1: Create the Tools List

```python
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

wikipedia_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper()
)

tools = [wikipedia_tool, concept_lookup, char_counter]
```

### Step 2: Create the ToolNode

The `ToolNode` wraps our tools list into a graph node that LangGraph can execute:

```python
from langgraph.prebuilt import ToolNode

tool_node = ToolNode(tools)
```

### Step 3: Bind Tools to the LLM

The `bind_tools()` method attaches the tool definitions to the LLM so it knows what is available:

```python
model_with_tools = llm.bind_tools(tools)
```

After binding, every time the LLM receives a message it also receives the **tool schemas** — the names, input types, and docstrings of all three tools. It uses this information to decide whether to respond directly or call a tool.

### How It Looks Together

```
┌─────────────────────────────────────┐
│            model_with_tools         │
│  (LLM + awareness of 3 tools)      │
├─────────────────────────────────────┤
│                                     │
│  Tools available:                   │
│    • wikipedia_tool  (factual)      │
│    • concept_lookup  (LLM-powered)  │
│    • char_counter    (Python-only)  │
│                                     │
└─────────────────────────────────────┘
```

<!-- lesson:page Building the Workflow -->

## Building the Workflow

With the tools ready, we need two workflow functions before wiring the graph: a **stopping function** that decides whether to call tools or end, and a **dynamic dispatcher** that handles different message types.

### MessagesState

Instead of writing a custom `State(TypedDict)` with `messages: Annotated[list, add_messages]`, LangGraph provides **MessagesState** — a pre-built class that handles message accumulation automatically:

```python
from langgraph.graph import MessagesState, START, END
```

### The Stopping Function: should_continue

This function inspects the last message and routes accordingly:

```python
def should_continue(state: MessagesState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END
```

If `tool_calls` is non-empty, the LLM wants to use a tool — route to `"tools"`. Otherwise, the conversation is done — return `END`.

### The Dynamic Dispatcher: call_model

The `call_model` function checks what kind of message it received before acting:

```python
from langchain_core.messages import AIMessage

def call_model(state: MessagesState):
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return {
            "messages": [
                AIMessage(content=last_message.tool_calls[0]["response"])
            ]
        }
    return {"messages": [model_with_tools.invoke(state["messages"])]}
```

| Condition | Action |
|-----------|--------|
| AIMessage **with** tool_calls | Return the tool response directly — no extra LLM call |
| Otherwise | Invoke the LLM with the full message history |

This avoids redundant LLM calls when a tool has already produced a response.

### Wiring the Graph

```python
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver

workflow = StateGraph(MessagesState)
workflow.add_node("chatbot", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "chatbot")
workflow.add_conditional_edges("chatbot", should_continue, ["tools", END])
workflow.add_edge("tools", "chatbot")

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
```

### The Graph Structure

```
        ┌──────────┐
        │  START    │
        └────┬─────┘
             │
             ▼
        ┌──────────┐       should_continue
   ┌───►│ chatbot   │──────────────────┐
   │    │(call_model)│                  │
   │    └────┬─────┘              no tool calls
   │         │                         │
   │    tool_calls?                    ▼
   │         │                    ┌────────┐
   │         ▼                    │  END   │
   │    ┌──────────┐              └────────┘
   │    │  tools    │
   │    │(ToolNode) │
   │    └────┬─────┘
   │         │
   └─────────┘
```

The **tools** node executes whichever tool the LLM selected, then loops back to **chatbot** so `call_model` can process the result.

<!-- lesson:page Testing the Multi-Tool Chatbot -->

## Testing the Multi-Tool Chatbot

With the graph compiled, we can test different query types and watch the LLM route to the correct tool.

### Query 1: Concept Explanation

```python
config = {"configurable": {"thread_id": "demo"}}
response = app.invoke(
    {"messages": [("user", "What is transfer learning?")]},
    config=config,
)
```

The LLM sees "What is transfer learning?" and matches it to `concept_lookup`. The message flow:

```
user → chatbot (LLM picks concept_lookup) → tools → chatbot → END
```

### Query 2: Text Analysis

```python
response = app.invoke(
    {"messages": [("user", "Count the words in: the quick brown fox jumps")]},
    config={"configurable": {"thread_id": "demo-2"}},
)
```

The LLM routes to `char_counter` — no LLM call inside the tool, pure Python.

### Query 3: Factual Lookup

```python
response = app.invoke(
    {"messages": [("user", "Tell me about the Hubble Space Telescope")]},
    config={"configurable": {"thread_id": "demo-3"}},
)
```

The LLM picks `wikipedia_tool` for a factual lookup.

### Query 4: Memory Follow-Up

```python
# Same thread_id as Query 1
response = app.invoke(
    {"messages": [("user", "Can you explain that in more detail?")]},
    config=config,
)
```

Because we compiled with `MemorySaver`, the chatbot remembers the earlier conversation about transfer learning and provides a detailed follow-up.

### Key Takeaway

The LLM makes the routing decision **per query** based on tool metadata. The `should_continue` function handles routing, `call_model` handles dispatch — separating concerns cleanly. Add more tools to the list and the chatbot gains new capabilities without changing the graph.

<!-- lesson:page Streaming Responses -->

## Streaming Responses

So far we have used `app.invoke()`, which waits for the entire response before returning. For a more interactive experience, `app.stream()` delivers messages in real time as they are generated.

### Single-Query Streaming

```python
from langchain_core.messages import HumanMessage

config = {"configurable": {"thread_id": "stream-1"}}

def stream_query(query):
    inputs = {"messages": [HumanMessage(content=query)]}
    for msg, metadata in app.stream(
        inputs, config, stream_mode="messages"
    ):
        if msg.content and not isinstance(msg, HumanMessage):
            print(msg.content, end="", flush=True)
    print("\n")
```

Setting `stream_mode="messages"` tells LangGraph to yield individual messages as they flow through the graph. The `flush=True` parameter ensures each piece of output is printed immediately without buffering.

### invoke vs stream

| | `app.invoke()` | `app.stream()` |
|---|---|---|
| **Returns** | Complete response dict | Iterator of `(message, metadata)` tuples |
| **Output timing** | All at once after completion | Real-time as tokens arrive |
| **Best for** | Batch processing, testing | Interactive chatbots, live UIs |

### Why Filter HumanMessage?

The stream includes **all** messages flowing through the graph — including the user's own input echoed back. Filtering with `not isinstance(msg, HumanMessage)` ensures we only display the chatbot's responses.

### Multi-Turn Streaming

We can extend streaming to handle a list of queries in sequence, simulating a full conversation:

```python
def stream_conversation(queries):
    for query in queries:
        print(f"User: {query}")
        response = ""
        for msg, metadata in app.stream(
            {"messages": [HumanMessage(content=query)]},
            config,
            stream_mode="messages",
        ):
            if msg.content and not isinstance(msg, HumanMessage):
                response += msg.content
        print(f"Agent: {response}\n")
```

Because all queries share the same `config` (same `thread_id`), the chatbot remembers earlier exchanges. A follow-up question like "Can you explain that in more detail?" will reference the prior conversation — combining **streaming** with **memory** in a single loop.

<!-- lesson:page What's Next? -->

## What's Next?

Congratulations — you have built a multi-tool chatbot that routes queries, manages state, remembers conversations, and streams responses in real time. These are the core building blocks of production-ready AI agents.

LangChain offers a suite of packages designed to test these systems in real-world settings before putting them into production:

- **LangSmith** helps debug your workflows by evaluating agent responses
- **LangGraph** allows customisation of agentic workflows
- **LangGraph Platform** supports agent deployment

Be sure to explore all of their documentation to build robust agents capable of impressive workloads.

<!-- lesson:end -->

## Prerequisites

- Completed **Module 05** (Adding External Tools) and **Module 06** (Memory & Conversation)
- OpenAI API key configured in `.env`

**Important**: This module requires an OpenAI API key. The example and challenge make real API calls.

### Running the Examples

```bash
# From the project root
python courses/langchain-agents/07-multi-tool-chatbot/multi_tool_chatbot.py
```

## Challenge

Complete the coding challenge to build your own multi-tool chatbot:

- Import the `@tool` decorator and `MessagesState`
- Define an LLM-powered tool and a pure Python tool
- Write the `call_model` dynamic dispatcher
- Combine tools with `ToolNode` and `bind_tools`
- Build and test the workflow
- Stream responses with `app.stream()` and filter `HumanMessage`
