# ReAct Agents & Custom Tools

This module introduces **ReAct agents** and **custom tools** -- how agents reason about questions, choose the right tool, and act to produce answers.

<!-- lesson:page What are ReAct Agents? -->
## What are ReAct Agents?

ReAct stands for **Reasoning** and **Action**. ReAct agents are intelligent, autonomous systems that:

- **Reason** about what information or action is needed to answer a question
- **Act** by calling tools -- functions that perform tasks like data lookup, calculations, or API calls
- **Observe** the tool's result and use it to formulate a final answer

This reasoning-action loop is the core of the agentic framework in LangChain.

## Key Concepts

- **Agents**: Autonomous systems that make decisions and take actions, much like a human would
- **Tools**: Functions that agents can call to perform specific tasks (data queries, calculations, lookups, etc.)
- **ReAct Loop**: The agent reasons about the question, picks a tool, calls it, and uses the result

## How a ReAct Agent Works

```
User Question: "What is (3 + 7) multiplied by 6?"
  ↓
Agent reasons: "I need to do arithmetic"
  ↓
Agent selects a math tool
  ↓
Agent calls tool → Gets result: 60
  ↓
Agent responds: "The answer is 60"
```

The agent decides **which tool to use** and **what inputs to provide** based purely on the question and the tool descriptions available to it.

<!-- lesson:page Creating a ReAct Agent -->
## Creating a ReAct Agent

LangChain provides `create_agent` from `langgraph.prebuilt` to build ReAct agents quickly:

```python
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
import math

# Set up the LLM
model = ChatOpenAI(model="gpt-4o-mini")

# Define a tool
@tool
def square_root(value: str) -> float:
    """Calculate the square root of a number."""
    return math.sqrt(float(value))

# Create the agent with the tool
agent = create_agent(model, [square_root])

# Ask a question in natural language
query = "What is the square root of 256?"
response = agent.invoke({"messages": [("human", query)]})

# Print the agent's answer
print(response['messages'][-1].content)
```

### Key Steps:
1. **Import** `tool`, `ChatOpenAI`, and `create_agent`
2. **Define tools** using the `@tool` decorator
3. **Create the agent** by passing the model and a list of tools
4. **Invoke** the agent with a `messages` list containing the user's question
5. **Read the response** from the last message's `.content`

<!-- lesson:page Building Custom Tools -->
## Building Custom Tools

By default, LangChain can handle many tasks, but custom tools let you give agents access to **your own data and logic**.

### The @tool Decorator

The `@tool` decorator from `langchain_core.tools` converts a regular Python function into a tool that agents can call:

```python
from langchain_core.tools import tool

@tool
def triangle_area(base: float, height: float) -> float:
    """Calculates the area of a triangle given the base and height."""
    return 0.5 * base * height
```

### How It Works Step by Step

1. **`@tool` decorator** -- Tells LangChain this function is available as a tool
2. **Typed parameters** -- Use Python type hints (`float`, `str`, etc.) so the LLM knows what to extract from the query
3. **Docstring** -- Describes what the tool does. The LLM reads this to decide when to call it
4. **Return the result** -- The agent receives this and uses it in its answer

### Registering and Using the Tool

Make the tool available by passing it in a list to `create_agent`:

```python
# Register tools in a list (you can include multiple tools)
tools = [triangle_area]

# Create the agent with the tools
app = create_agent(model, tools)

# Ask a question in natural language
query = "What is the area of a triangle with base 12 and height 8?"
response = app.invoke({"messages": [("human", query)]})
print(response['messages'][-1].content)
```

The agent:
1. Reads the question
2. Matches it against tool descriptions
3. Calls `triangle_area(base=12, height=8)`
4. Receives `48.0` and answers the user

<!-- lesson:page Tool Attributes & Multiple Tools -->
## Tool Attributes

Every tool created with `@tool` has three key attributes:

1. **`.name`** -- The tool's name (derived from the function name)
2. **`.description`** -- The tool's description (from the docstring)
3. **`.args`** -- The input argument schema

```python
print(triangle_area.name)        # "triangle_area"
print(triangle_area.description) # "Calculates the area of a triangle..."
print(triangle_area.args)        # {'input': {'type': 'string', ...}}
```

The **description** is especially important -- it's what the LLM reads to decide whether this tool is relevant to the current question.

## Using Multiple Tools

Agents can work with any number of tools. Pass them all in a list and the agent picks the right one based on the question:

```python
@tool
def get_recipe(recipe_id: str) -> str:
    """Look up a recipe from the catalog by its ID."""
    # ... lookup logic ...

agent = create_agent(model, [triangle_area, get_recipe])
```

When a question is about geometry, the agent calls `triangle_area`. When it's about recipes, it calls `get_recipe`. The agent makes this decision automatically based on tool descriptions.

**Note:** LangChain also has an extensive library of pre-built tools for database querying, web scraping, image generation, and more. See the LangChain documentation for the full list.

<!-- lesson:page Code Example -->
## Code Example

### ReAct Agents & Custom Tools (`react_agent_tools_example.py`)

This example demonstrates:
- Creating a basic ReAct agent with a math tool
- Building a custom tool with `@tool` and a string input
- Inspecting tool attributes (name, description, args)
- Using multiple custom tools with a single agent

**Key Features:**
- Shows the full ReAct reasoning-action loop
- Builds a triangle area calculator as a custom tool
- Builds a recipe lookup tool from a sample catalog
- Demonstrates how the agent picks the right tool automatically

## Summary

- ReAct agents **reason** about questions and **act** by calling tools
- The `@tool` decorator converts any Python function into an agent tool
- The tool's **docstring** is how the LLM decides when to call it
- Use **typed parameters** so the LLM extracts values from the query automatically
- Agents can use **multiple tools** and pick the right one per question
- Pass tools as a **list** to `create_agent`

<!-- lesson:end -->

## Prerequisites

This module builds on the ReAct agent and custom tool concepts from the **LangChain Fundamentals** course (modules 06 and 07). Familiarity with those modules is recommended.

**Important**: ReAct agents require OpenAI models. They do not work with Hugging Face models because Hugging Face models don't support the `bind_tools` method required by ReAct agents.

### Setting Up Your Environment

**Complete Setup Steps:**

1. **Create the `.env` file** using the Makefile:
   ```bash
   make setup
   ```
   This creates a `.env` file from `.env.example` (or creates a template if it doesn't exist).

2. **Edit the `.env` file** and add your OpenAI API key (required):
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   ```
   > **Note:** ReAct agents require an OpenAI API key. Hugging Face models do not support the `bind_tools` method required by ReAct agents.

3. **Set up virtual environment and install dependencies:**
   ```bash
   make install
   ```
   This creates a Python virtual environment and installs all required packages.

**Alternative: Environment Variable**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

> **Note:** The `.env` file is automatically loaded by the examples using `python-dotenv`. Make sure not to commit your `.env` file to version control!

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
- `langchain-openai`: For OpenAI model integration
- `langchain-core`: For the `@tool` decorator
- `langchain`: For creating agents (`create_agent`)
- `python-dotenv`: For loading environment variables from `.env` file

All dependencies are listed in `requirements.txt` and installed automatically with `make install`.

## Running the Examples

### Using Makefile (Recommended)

```bash
# Run the example (creates venv and installs deps if needed)
make run

# Or run directly
make all
```

### Manual Execution

```bash
source venv/bin/activate
python react_agent_tools_example.py
```

## Quiz

Test your understanding! Run:

```bash
make quiz
```

## Challenge

Complete the coding challenge:

```bash
make challenge
```

The challenge asks you to:
- Import the `@tool` decorator
- Create a custom tool for looking up planet data
- Create a ReAct agent with the tool
- Invoke the agent with a question

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you've run `make install` to install all dependencies
2. **API Key Errors**: ReAct agents require an OpenAI API key -- check your `.env` file
3. **Tool Not Being Called**: Check that your tool's docstring clearly describes when it should be used
4. **Type Errors**: Make sure your function has proper type hints for parameters and return type
5. **bind_tools Error**: If you see `AttributeError: ... has no attribute 'bind_tools'`, you're trying to use a model that doesn't support tool calling. Switch to an OpenAI model.
