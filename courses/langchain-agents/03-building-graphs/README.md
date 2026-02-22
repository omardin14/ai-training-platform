# Building Graphs

This module introduces **LangGraph's StateGraph** -- how to build custom chatbot workflows by defining nodes, edges, and an agent state.

<!-- lesson:page What is a Graph in LangGraph? -->
## What is a Graph in LangGraph?

In LangGraph, a **graph** organises the agent's order of tasks -- such as tool usage and LLM calls -- into a structured workflow. The graph uses an **agent state** to track the agent's progress as text, helping determine when a task is complete.

### Core Concepts

- **Nodes**: Functions that perform work (e.g. generating a response, calling a tool)
- **Edges**: Connections between nodes that define the flow
- **State**: A data structure that tracks messages and progress through the workflow

### A Simple Chatbot Graph

```
    ┌───────┐      ┌─────────┐      ┌─────┐
    │ START │ ───▶ │ chatbot │ ───▶ │ END │
    └───────┘      └─────────┘      └─────┘
```

- An edge connects **START** to the **chatbot** node
- The chatbot node generates a response using the LLM
- Another edge connects **chatbot** to **END**

The `START` and `END` nodes are imported directly from LangGraph to mark the beginning and end of the workflow.

### Use Case

Imagine a travel assistant chatbot that uses an LLM to answer questions about destinations. The graph state ensures each question flows through the LLM and produces a response in the correct order.

<!-- lesson:page Setting Up the Graph -->
## Setting Up the Graph

Building a graph requires several imports:

**Modules for structuring text** -- `Annotated` and `TypedDict` help organise the chatbot's text data with type hints.

```python
from typing import Annotated
from typing_extensions import TypedDict
```

**LangGraph modules for defining graphs** -- `StateGraph` builds the graph that organises nodes and edges. `START` and `END` mark the beginning and end of the workflow. `add_messages` ensures new messages are appended to the list rather than replacing it.

```python
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
```

**LLM provider** -- `ChatOpenAI` is the model that generates responses.

```python
from langchain_openai import ChatOpenAI
```

<!-- lesson:page Defining the State -->
## Defining the State

The **State** class defines what data the graph tracks. For a chatbot, we need a list of messages:

```python
llm = ChatOpenAI(model="gpt-4o-mini")

class State(TypedDict):
    messages: Annotated[list, add_messages]
```

### Key Details

- **`TypedDict`** gives the state a structured shape -- LangGraph knows it has a `messages` field
- **`Annotated[list, add_messages]`** does two things:
  - Declares `messages` as a list
  - The `add_messages` annotation tells LangGraph to **append** new messages rather than overwrite the list
- Every interaction with the chatbot is stored in this messages list

<!-- lesson:page Building and Compiling -->
## Building and Compiling the Graph

With the state defined, we build the graph in five steps:

**Step 1: Initialise the graph builder** -- Create a `StateGraph` and pass in our `State` structure. The graph builder will organise the nodes and edges in the chatbot's workflow.

```python
graph_builder = StateGraph(State)
```

**Step 2: Define the chatbot function node** -- This function accepts the `State` class and uses `llm.invoke()` with the messages content to generate a response based on the conversation so far.

```python
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}
```

**Step 3: Add the node to the graph** -- Register the chatbot function as a node using `.add_node()`, giving it the label `"chatbot"`.

```python
graph_builder.add_node("chatbot", chatbot)
```

**Step 4: Connect the edges** -- Connect the `START` node to the chatbot node to begin the conversation, then connect the chatbot node to the `END` node to finish it.

```python
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
```

**Step 5: Compile the graph** -- Now that the graph builder is ready, compile it into a runnable application using `.compile()`.

```python
graph = graph_builder.compile()
```

### The Result

```
    ┌───────┐      ┌─────────┐      ┌─────┐
    │ START │ ───▶ │ chatbot │ ───▶ │ END │
    └───────┘      └─────────┘      └─────┘
```

The compiled graph can be invoked just like any LangChain agent:

```python
response = graph.invoke({"messages": [("human", "What is 2 + 2?")]})
print(response["messages"][-1].content)
```

<!-- lesson:page Code Example -->
## Code Example

### Building Graphs (`building_graphs_example.py`)

This example demonstrates:
- Understanding graph concepts (nodes, edges, state)
- Importing and setting up the required modules
- Defining a `State` class with `TypedDict` and `Annotated`
- Building a chatbot node function with `llm.invoke()`
- Connecting `START → chatbot → END` with edges
- Compiling and invoking the graph
- Multi-turn conversation with the compiled graph

**Key Features:**
- Walks through each build step with explanations
- Shows the graph structure as ASCII art
- Demonstrates both single-query and follow-up usage
- The compiled graph works just like a LangChain agent

## Summary

- **StateGraph** organises the agent's workflow as nodes and edges
- **Nodes** are functions that process state (e.g. call the LLM)
- **Edges** connect nodes: `START → chatbot → END`
- **State** uses `TypedDict` with `Annotated[list, add_messages]` to track messages
- **`.compile()`** turns the graph into a runnable application
- The compiled graph supports conversation history like any agent

<!-- lesson:end -->

## Prerequisites

This module builds on **02-agent-conversations**. Understanding conversation history and message types will help with the state and message concepts here.

**Important**: This module requires an OpenAI API key.

### Setting Up Your Environment

1. **Create the `.env` file**:
   ```bash
   make setup
   ```

2. **Edit the `.env` file** and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   ```

3. **Install dependencies:**
   ```bash
   make install
   ```

## Running the Examples

```bash
# Run the example
make run

# Or run directly
make all
```

## Quiz

Test your understanding:

```bash
make quiz
```

## Challenge

Complete the coding challenge:

```bash
make challenge
```

The challenge asks you to:
- Import `StateGraph`, `START`, and `END`
- Define a `State` class with `TypedDict` and `add_messages`
- Initialise a `StateGraph` and define a chatbot node
- Compile and invoke the graph

## Troubleshooting

### Common Issues

1. **Import Errors**: Run `make install` to install all dependencies
2. **API Key Errors**: Check your `.env` file has a valid OpenAI API key
3. **State Errors**: Make sure `messages` uses `Annotated[list, add_messages]`, not just `list`
4. **Graph Won't Compile**: Ensure both edges are added (START → chatbot and chatbot → END)
5. **No Response**: Verify the chatbot function returns `{"messages": [llm.invoke(...)]}` (wrapped in a list)
