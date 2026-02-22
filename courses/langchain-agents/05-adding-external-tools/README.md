# Adding External Tools

This module covers **adding external tools** to your LangGraph chatbot using Wikipedia as an example. You will learn how to bind tools to the LLM, use `ToolNode` to execute tool calls, and route between the chatbot and tools using `tools_condition`.

<!-- lesson:page Why Add External Tools? -->
## Why Add External Tools?

In the previous module, we saw that LLMs can **hallucinate** -- generating confident but incorrect information. Our chatbot responded to every question, but it had no way to verify its answers against real-world data.

**External tools** solve this by giving the chatbot access to verified information sources. Instead of guessing, the chatbot can query an API, search a database, or look up facts from authoritative sources.

### How It Works

When a user asks a factual question, the chatbot can:
1. **Recognise** that it needs external data to answer accurately
2. **Call a tool** (like Wikipedia) to retrieve verified information
3. **Use the tool's response** to formulate an accurate answer

### The Graph Flow with Tools

Adding tools changes the graph structure. Instead of a simple START --> chatbot --> END flow, we now have a **conditional loop**:

```
    START
      |
      v
  chatbot <-------+
    |              |
 tools_condition   |
    |       |      |
    v       v      |
  tools    END     |
    |              |
    +--------------+
```

If the chatbot decides it needs a tool, the graph routes to the `tools` node. After the tool runs, the result goes back to the chatbot so it can formulate a response. If no tool is needed, the graph goes straight to END.

<!-- lesson:page Setting Up the Wikipedia Tool -->
## Setting Up the Wikipedia Tool

LangChain provides a ready-made Wikipedia tool that queries the Wikipedia API and returns article summaries. It requires two components:

### WikipediaAPIWrapper

The **API wrapper** handles the connection to Wikipedia. The `top_k_results` parameter controls how many articles are returned per query:

```python
from langchain_community.utilities import WikipediaAPIWrapper

api_wrapper = WikipediaAPIWrapper(top_k_results=1)
```

Setting `top_k_results=1` means only the most relevant article is returned, keeping responses focused.

### WikipediaQueryRun

The **query runner** wraps the API wrapper into a LangChain tool that agents can use:

```python
from langchain_community.tools import WikipediaQueryRun

wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
```

### Creating the Tools List

Tools are provided to the graph as a list. Even with a single tool, it must be in a list:

```python
tools = [wikipedia_tool]
```

The `wikipedia_tool` object has a `.name` and `.description` that the LLM reads to decide when to use it. You can inspect these to understand what the LLM sees.

<!-- lesson:page Binding Tools to the LLM -->
## Binding Tools to the LLM

Once you have your tools list, you need to tell the LLM about them. This is done with **`.bind_tools()`**.

### What `.bind_tools()` Does

Calling `.bind_tools(tools)` creates a new LLM instance that knows about the available tools. It does **not** modify the original LLM -- it returns a wrapped version:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)
```

### The Modified Chatbot Function

With tools bound, the chatbot function uses `llm_with_tools` instead of `llm`:

```python
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}
```

When the LLM receives a question, it now has two options:
- **Answer directly** if it is confident in its knowledge
- **Request a tool call** if it needs external data

The LLM's response will contain either regular text content or a **tool call request** with the query to send to the tool.

<!-- lesson:page Adding Tool Nodes to the Graph -->
## Adding Tool Nodes to the Graph

With tools bound to the LLM, we need to add two things to the graph: a **ToolNode** to execute tool calls, and **conditional routing** to direct the flow.

### ToolNode

`ToolNode` is a prebuilt LangGraph node that executes tool calls. It takes the tools list and handles running the correct tool when requested:

```python
from langgraph.prebuilt import ToolNode

tool_node = ToolNode(tools=[wikipedia_tool])
```

Add it to the graph as a node named `"tools"`:

```python
graph_builder.add_node("tools", tool_node)
```

### tools_condition

`tools_condition` is a prebuilt function that checks whether the chatbot's last message contains a tool call. It returns either `"tools"` (to route to the tool node) or `END` (to finish):

```python
from langgraph.prebuilt import tools_condition

graph_builder.add_conditional_edges("chatbot", tools_condition)
```

### The Tool Loop

After the tools node executes, the result must go back to the chatbot so it can read the tool's output and formulate a response:

```python
graph_builder.add_edge("tools", "chatbot")
```

This creates a loop: chatbot --> tools --> chatbot --> END.

<!-- lesson:page The Complete Graph -->
## The Complete Graph

Here is the full graph structure with tools integrated:

```
    +-------+
    | START |
    +---+---+
        |
        v
    +---------+
    | chatbot |<-----+
    +----+----+      |
    tools_condition   |
    +----+-----+     |
    v          v     |
+-------+  +-----+  |
| tools |  | END |  |
+---+---+  +-----+  |
    +----------------+
```

### Building the Complete Graph

```python
graph_builder = StateGraph(State)

# Add the chatbot node
graph_builder.add_node("chatbot", chatbot)

# Add the tool node
tool_node = ToolNode(tools=[wikipedia_tool])
graph_builder.add_node("tools", tool_node)

# Connect START to chatbot
graph_builder.add_edge(START, "chatbot")

# Add conditional routing from chatbot
graph_builder.add_conditional_edges("chatbot", tools_condition)

# Loop tools back to chatbot
graph_builder.add_edge("tools", "chatbot")

# Compile
graph = graph_builder.compile()
```

### Step-by-Step Flow

1. **User sends a message** -- enters the graph at START
2. **Chatbot node runs** -- the LLM (with tools bound) processes the message
3. **tools_condition checks** -- did the LLM request a tool call?
   - **Yes** --> route to `tools` node, which executes the Wikipedia query, then return to `chatbot` so the LLM can read the result and respond
   - **No** --> route to `END`, the LLM's response is the final answer
4. **After tools run** -- the chatbot sees the tool result and generates a natural language response, then `tools_condition` checks again (usually routing to END)

<!-- lesson:page Code Example -->
## Code Example

### Adding External Tools (`adding_external_tools_example.py`)

This example demonstrates:
- Setting up the Wikipedia tool with `WikipediaAPIWrapper` and `WikipediaQueryRun`
- Binding tools to the LLM with `.bind_tools()`
- Building a graph with `ToolNode` and `tools_condition` for conditional routing
- Testing queries that trigger tool calls (factual questions) and queries that do not (simple calculations)
- Visualising the complete graph with tools

**Key Features:**
- Shows how the chatbot decides when to use tools vs answering directly
- Demonstrates the tool loop: chatbot --> tools --> chatbot --> END
- Uses `stream_graph_updates()` from Module 04 for real-time output
- Includes graph visualisation to see the conditional routing structure

## Summary

- **WikipediaAPIWrapper** connects to the Wikipedia API; `top_k_results=1` returns the top result
- **WikipediaQueryRun** wraps the API wrapper into a tool agents can use
- **`.bind_tools(tools)`** creates an LLM instance that can recognise and request tool calls
- **ToolNode** executes tool calls and returns results as messages
- **tools_condition** checks if the last message contains a tool call, routing to `"tools"` or `END`
- **Conditional edges** enable the chatbot to decide at runtime whether to use a tool or respond directly

<!-- lesson:end -->

## Prerequisites

This module builds on **04-chatbot-responses**. You should understand how to build a graph with nodes and edges, stream responses, and compile a graph.

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
- Set up the Wikipedia tool with WikipediaAPIWrapper and WikipediaQueryRun
- Bind tools to the LLM with `.bind_tools()`
- Create a ToolNode and use tools_condition for conditional routing
- Build and compile the complete graph with tool integration

## Troubleshooting

### Common Issues

1. **Import Errors**: Run `make install` to install all dependencies
2. **API Key Errors**: Check your `.env` file has a valid OpenAI API key
3. **Wikipedia Errors**: Ensure the `wikipedia` and `langchain-community` packages are installed
4. **No Tool Calls**: The LLM decides when to use tools -- simple questions may not trigger a Wikipedia lookup
5. **Timeout Errors**: Wikipedia API calls may take a few seconds; be patient with responses
