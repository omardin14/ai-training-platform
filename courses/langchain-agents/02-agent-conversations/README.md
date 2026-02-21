# Agent Conversations

This module covers how to maintain **conversation history** with agents -- enabling follow-up questions, context-aware answers, and full conversation inspection.

<!-- lesson:page Why Conversation History Matters -->
## Why Conversation History Matters

When you invoke an agent, it processes a single query and returns a response. But real conversations involve **follow-up questions** that reference earlier context:

- "What is the area of a circle with radius 7?" → Agent answers
- "What about one with radius 3?" → Agent needs to remember we were talking about circles

Without conversation history, the agent has no idea what "one" refers to. By passing the full message history with each new query, the agent can answer context-dependent questions naturally.

## Key Concepts

- **Message History**: The list of all messages exchanged so far
- **HumanMessage**: Represents a user's query
- **AIMessage**: Represents the agent's response
- **Follow-Up Questions**: New queries that rely on earlier context
- **Input/Output Logging**: Printing both user_input and agent_output for debugging

<!-- lesson:page Logging Agent Input and Output -->
## Logging Agent Input and Output

It's useful to print both the user's query and the agent's response to verify things are working correctly. We label them `user_input` and `agent_output`:

```python
from langchain_core.tools import tool
from langchain.agents import create_agent

@tool
def circle_area(radius: float) -> float:
    """Calculates the area of a circle given its radius."""
    import math
    return round(math.pi * radius ** 2, 2)

app = create_agent(model, [circle_area])

query = "What is the area of a circle with radius 7?"
response = app.invoke({"messages": [("human", query)]})

# Print both input and output for verification
print({"user_input": query,
       "agent_output": response['messages'][-1].content})
```

This pattern is helpful for debugging -- you can see exactly what went in and what came back.

<!-- lesson:page Follow-Up Questions -->
## Follow-Up Questions with Message History

To ask follow-up questions, we:

1. **Save the message history** from the previous response
2. **Append the new query** to the history
3. **Invoke the agent** with the combined messages

```python
# Save the message history from the first response
message_history = response["messages"]

# Ask a follow-up without repeating context
new_query = "What about one with radius 3?"

# Pass the full history + new query
response = app.invoke({
    "messages": message_history + [("human", new_query)]
})
```

While answering, LangChain updates the entire conversation. The response contains all messages exchanged so far -- both old and new queries with their respective answers.

### The Flow:

```
First query → Agent answers → Save message_history
  ↓
Follow-up query (no extra context needed)
  ↓
Pass: message_history + [("human", new_query)]
  ↓
Agent sees full conversation → Understands context → Answers
```

<!-- lesson:page Inspecting the Conversation -->
## Inspecting the Conversation

To inspect the conversation, we import `HumanMessage` and `AIMessage` from `langchain_core.messages`:

```python
from langchain_core.messages import HumanMessage, AIMessage
```

- **HumanMessage** -- represents our queries
- **AIMessage** -- represents the agent's answers

### Filtering Messages

The response contains all message types (including internal tool calls). To get a clean conversation log, filter for only `HumanMessage` and `AIMessage` instances with actual content:

```python
filtered_messages = [
    msg for msg in response["messages"]
    if isinstance(msg, (HumanMessage, AIMessage))
    and msg.content.strip()
]
```

The `.strip()` method removes any trailing whitespace, ensuring we skip empty messages.

### Formatting the Output

Label each message with its class name for a readable log:

```python
print({
    "user_input": new_query,
    "agent_output": [
        f"{msg.__class__.__name__}: {msg.content}"
        for msg in filtered_messages
    ]
})
```

This prints the full conversation with `HumanMessage` and `AIMessage` labels. The last entry is always the most recent answer, which is useful for verification.

<!-- lesson:page Code Example -->
## Code Example

### Agent Conversations (`agent_conversations_example.py`)

This example demonstrates:
- Sending a query and logging both input and output
- Saving message history from the response
- Asking follow-up questions using conversation history
- Filtering `HumanMessage` and `AIMessage` from the response
- Building a multi-turn conversation with a custom tool

**Key Features:**
- Circle area calculator tool used across multiple turns
- Shows how the agent maintains context between queries
- Demonstrates clean conversation logging with class name labels
- Continues the conversation across three turns

## Summary

- Print `user_input` and `agent_output` to verify agent behaviour
- Save `response["messages"]` as the conversation history
- Pass `message_history + [("human", new_query)]` for follow-ups
- Import `HumanMessage` and `AIMessage` to inspect the conversation
- Filter with `isinstance()` and `.strip()` for a clean message log
- Each response carries the full history, so you can keep the conversation going

<!-- lesson:end -->

## Prerequisites

This module builds on **01-react-agents-tools**. Make sure you understand how to create agents and custom tools before starting.

**Important**: Agents require an OpenAI API key. Hugging Face models do not support tool calling.

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
- Create an agent with a distance conversion tool
- Send a query and capture the response
- Save message history and ask a follow-up question
- Filter and display the conversation log

## Troubleshooting

### Common Issues

1. **Import Errors**: Run `make install` to install all dependencies
2. **API Key Errors**: Check your `.env` file has a valid OpenAI API key
3. **Empty Responses**: Make sure you're passing `response["messages"]` (not `response`) as the history
4. **Missing Context**: Ensure you include the full `message_history` when asking follow-up questions
5. **Filter Returns Empty**: Check that you're filtering for both `HumanMessage` and `AIMessage`
