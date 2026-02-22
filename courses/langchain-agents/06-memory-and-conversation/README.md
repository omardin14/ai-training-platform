# Memory & Conversation

This module covers **adding memory** to your LangGraph chatbot so it can maintain conversation context across multiple turns. You will learn how to use `MemorySaver` as a checkpoint, configure sessions with `thread_id`, and stream responses that remember previous interactions.

<!-- lesson:page Why Add Memory? -->
## Why Add Memory?

In the previous module, we added the Wikipedia tool so the chatbot can look up verified facts. However, each query is still treated **independently** -- the chatbot has no memory of what was discussed before.

### The Problem

In Module 02, we handled follow-up questions by **manually** passing the full `message_history` list to each new `.invoke()` call. This works, but it means your code is responsible for tracking and passing the conversation state every time.

Without that manual effort, follow-up questions lose context:

```
User:  "What is the Panama Canal?"
Agent: "The Panama Canal is a waterway in Panama..."

User:  "When was it completed?"
Agent: (has no context -- doesn't know "it" refers to the Panama Canal)
```

### The Solution

**MemorySaver** handles conversation history **automatically**. Instead of manually passing message history, the graph saves its state as checkpoints. Each message is stored, so the chatbot can reference earlier turns without any manual tracking:

```
User:  "What is the Panama Canal?"
Agent: "The Panama Canal is a waterway in Panama..."

User:  "When was it completed?"
Agent: "The Panama Canal was completed in 1914..."
```

By adding memory, the graph manages conversation context for you -- no need to manually collect and pass message history.

<!-- lesson:page Verifying Tool Responses -->
## Verifying Tool Responses

Before adding memory, let's verify the Wikipedia tool integration from Module 05 is working. We define a streaming function called `stream_tool_responses` that prints the full message objects, so we can see tool call metadata.

### The stream_tool_responses Function

```python
def stream_tool_responses(user_input: str):
    for event in graph.stream({"messages": [("human", user_input)]}):
        for value in event.values():
            print("Agent:", value["messages"])
```

Unlike `stream_graph_updates()` from Module 04 (which printed just the content), this function prints the **full message objects**. This reveals the tool call metadata, including the tool name and the query sent to Wikipedia.

### What the Output Shows

When you run a factual query, the output shows three stages:
1. **Tool call request** -- the chatbot recognises it needs Wikipedia and sends a query
2. **Tool response** -- Wikipedia returns the article summary
3. **Final answer** -- the chatbot uses the Wikipedia content to formulate its response

### Visualising the Graph

The graph diagram confirms the tools node is connected with conditional routing:

```python
display(Image(graph.get_graph().draw_mermaid_png()))
```

This shows the same structure from Module 05: START --> chatbot --> tools_condition --> tools/END, with the tools --> chatbot loop.

<!-- lesson:page Setting Up MemorySaver -->
## Setting Up MemorySaver

To add memory to the chatbot, we use `MemorySaver` from LangGraph's checkpoint module.

### Import and Create

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
```

`MemorySaver` stores conversation state **in memory** (not to disk). It acts as a checkpoint that saves the graph's state after each node runs.

### Compile with Checkpointing

Pass the `memory` instance to `graph_builder.compile()` using the `checkpointer` parameter:

```python
graph = graph_builder.compile(checkpointer=memory)
```

This tells the graph to save its state after each step. The chatbot can now look back at previous messages when generating a response.

### What Changes

| Without Memory | With Memory |
|----------------|-------------|
| Each query is independent | Queries share conversation history |
| You must manually pass message history | The graph tracks conversation automatically |
| `graph_builder.compile()` | `graph_builder.compile(checkpointer=memory)` |

<!-- lesson:page Streaming with Memory -->
## Streaming with Memory

With memory enabled, we need a **config dictionary** to identify the conversation session. This is how the chatbot knows which conversation history to use.

### The Config Dictionary

```python
config = {"configurable": {"thread_id": "single_session_memory"}}
```

The `thread_id` is a unique identifier for the conversation. All messages sent with the same `thread_id` share the same memory. Different `thread_id` values create separate conversations.

### The stream_memory_responses Function

```python
def stream_memory_responses(user_input: str):
    config = {"configurable": {"thread_id": "single_session_memory"}}
    for event in graph.stream({"messages": [("human", user_input)]}, config):
        for value in event.values():
            if "messages" in value and value["messages"]:
                print("Agent:", value["messages"][-1].content)
```

### Key Differences from Previous Streaming

| Feature | stream_graph_updates (Module 04) | stream_memory_responses |
|---------|----------------------------------|------------------------|
| Config parameter | Not used | `config` passed to `.stream()` |
| Thread ID | None | Identifies the conversation session |
| Memory | No persistence | Messages saved between calls |
| Guard check | Not needed | `if "messages" in value` ensures safe access |

The guard check `if "messages" in value and value["messages"]:` is important because with checkpointing enabled, some events may not contain messages.

<!-- lesson:page Conversation in Action -->
## Conversation in Action

With memory enabled, the chatbot can handle follow-up questions that reference earlier parts of the conversation.

### Example Conversation

```python
stream_memory_responses("What is the Panama Canal?")
# Agent: The Panama Canal is a waterway in Panama connecting
#        the Atlantic and Pacific oceans...

stream_memory_responses("When was it completed?")
# Agent: The Panama Canal was completed in 1914...
```

### How It Works

1. **First query** -- "What is the Panama Canal?" is sent to the chatbot. The LLM calls Wikipedia, retrieves the article, and generates a response. The entire exchange is saved to memory.

2. **Follow-up query** -- "When was it completed?" is sent with the same `thread_id`. The chatbot loads the previous conversation from memory, sees that "it" refers to the Panama Canal, and answers using context from the earlier turn.

### Thread ID as Session Identifier

The `thread_id` acts like a session ID. You can have multiple independent conversations by using different thread IDs:

```python
# Conversation A
config_a = {"configurable": {"thread_id": "session_a"}}
graph.stream({"messages": [("human", "What is the Sahara?")]}, config_a)

# Conversation B (separate memory)
config_b = {"configurable": {"thread_id": "session_b"}}
graph.stream({"messages": [("human", "What is the Amazon?")]}, config_b)
```

Each thread maintains its own independent conversation history.

<!-- lesson:page Code Example -->
## Code Example

### Memory & Conversation (`memory_and_conversation_example.py`)

This example demonstrates:
- Rebuilding the chatbot with Wikipedia tools (recap from Module 05)
- Verifying tool responses with `stream_tool_responses()` to see tool call metadata
- Setting up `MemorySaver` and compiling the graph with `checkpointer=memory`
- Streaming with memory using `stream_memory_responses()` and a `thread_id` config
- Testing follow-up questions that rely on conversation context
- Visualising the complete graph

**Key Features:**
- Shows the difference between stateless and memory-enabled chatbots
- Demonstrates how `thread_id` identifies conversation sessions
- Uses the guard check pattern for safe message access with checkpointing
- Includes graph visualisation showing the tool routing structure

## Summary

- **MemorySaver** stores conversation state as in-memory checkpoints
- **`checkpointer=memory`** in `.compile()` enables memory for the graph
- **`thread_id`** in the config dictionary identifies a unique conversation session
- **`config`** must be passed to `.stream()` as the second argument
- The guard check `if "messages" in value` ensures safe access with checkpointing
- Different `thread_id` values create separate, independent conversations

<!-- lesson:end -->

## Prerequisites

This module builds on **05-adding-external-tools**. You should understand how to set up the Wikipedia tool, bind tools to the LLM, and build a graph with `ToolNode` and `tools_condition`.

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
- Import and create a `MemorySaver` instance
- Compile the graph with `checkpointer=memory`
- Set up a config dictionary with a `thread_id`
- Pass the config to `.stream()` for memory-enabled streaming
- Use the guard check pattern for safe message access

## Troubleshooting

### Common Issues

1. **Import Errors**: Run `make install` to install all dependencies
2. **API Key Errors**: Check your `.env` file has a valid OpenAI API key
3. **Memory Not Working**: Ensure you pass `checkpointer=memory` to `.compile()`
4. **Follow-ups Fail**: Check that both queries use the same `thread_id` in the config
5. **Missing Config**: The `config` dictionary must be passed as the second argument to `.stream()`
