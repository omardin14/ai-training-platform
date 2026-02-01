# Custom Tools

This module introduces **Custom Tools** - how to create your own tools for ReAct agents to extend their capabilities with domain-specific functions.

## What are Custom Tools?

Custom tools are functions that you create and make available to ReAct agents. They allow you to:
- **Extend agent capabilities** with domain-specific functions
- **Integrate with your own systems** (databases, APIs, etc.)
- **Create specialized tools** for specific use cases
- **Control tool behavior** with custom logic

Unlike pre-built tools (like the calculator), custom tools are functions you define and decorate with `@tool`.

## Concepts Covered

- **Custom Tools**: Creating your own tools with the `@tool` decorator
- **Tool Attributes**: Understanding `.name`, `.description`, and `.args`
- **Tool Description**: How the LLM uses descriptions to decide when to call tools
- **Agent Integration**: Using custom tools with ReAct agents

## How Custom Tools Work

Creating a custom tool involves:

1. **Define a Function**: Write a function that performs your desired action
2. **Add a Docstring**: The function's docstring becomes the tool's description
3. **Apply @tool Decorator**: Convert the function to a tool
4. **Use with Agent**: Pass the tool to a ReAct agent

### Example Flow:
```
Define Function → Add @tool Decorator → Tool Created
  ↓
Tool has: name, description, args
  ↓
Pass tool to agent → Agent can use tool
  ↓
Agent reasons: "This question needs the tool"
  ↓
Agent calls tool → Gets result → Answers question
```

## Prerequisites

This module builds on the concepts from **06-ReAct-agents**. Make sure you've completed that module first.

**Important**: ReAct agents with custom tools require OpenAI models. They do not work with Hugging Face models because Hugging Face models don't support the `bind_tools` method required by ReAct agents.

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
   > **Note:** ReAct agents with custom tools require an OpenAI API key. Hugging Face models do not support the `bind_tools` method required by ReAct agents.

3. **Set up virtual environment and install dependencies:**
   ```bash
   make install
   ```
   This creates a Python virtual environment and installs all required packages.

**Model Selection:**
- **ReAct agents require OpenAI**: Uses OpenAI's GPT-3.5-turbo model
- **Hugging Face models are not supported** for ReAct agents with custom tools (they don't support `bind_tools`)

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
- `langchain-community`: For additional tool utilities
- `langgraph`: For creating ReAct agents (`create_react_agent`)
- `python-dotenv`: For loading environment variables from `.env` file

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
python custom_tool_example.py
```

## Understanding Custom Tool Structure

Let's break down how a custom tool works:

```python
# Step 1: Import the @tool decorator
from langchain_core.tools import tool

# Step 2: Define a function with a docstring
@tool
def get_product_info(product_id: str) -> str:
    """Retrieve product information from inventory based on product ID."""
    # Your function logic here
    return result

# Step 3: Use the tool with an agent
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(llm, [get_product_info])

# Step 4: Invoke the agent
response = agent.invoke({"messages": [("human", "What is the price of laptop-pro-15?")]})
```

### Key Components:

1. **Function Definition**: A regular Python function with type hints
   - The function's docstring becomes the tool's description
   - The LLM uses this description to decide when to call the tool

2. **@tool Decorator**: Converts the function to a tool
   - Automatically extracts name, description, and args
   - Makes the function usable by agents

3. **Tool Attributes**: Tools have important attributes
   - `.name`: The tool's name (from function name)
   - `.description`: The tool's description (from docstring)
   - `.args`: The tool's input arguments schema

4. **Agent Integration**: Pass tools to the agent
   - Agent uses tool descriptions to decide when to call them
   - Agent automatically formats tool calls and processes results

### The Flow:

```
User Question: "What is the price of laptop-pro-15?"
  ↓
Agent receives question
  ↓
Agent reasons: "I need product information"
  ↓
Agent sees get_product_info tool description matches
  ↓
Agent calls get_product_info("laptop-pro-15")
  ↓
Tool returns: "Product: Laptop Pro 15\nPrice: $1299.99..."
  ↓
Agent formulates answer: "The price is $1299.99"
```

## Code Examples

### Custom Tool Example (`custom_tool_example.py`)

This example demonstrates:
- Creating a custom tool using the `@tool` decorator
- Understanding tool attributes (name, description, args)
- Using custom tools with ReAct agents
- How agents decide when to use custom tools

**Key Features:**
- Defines a product inventory lookup function
- Converts it to a tool with `@tool` decorator
- Shows tool attributes (name, description, args)
- Uses the tool with a ReAct agent
- Demonstrates how the agent uses the tool automatically

## Key Concepts Explained

### The @tool Decorator

The `@tool` decorator is imported from `langchain_core.tools`:
```python
from langchain_core.tools import tool

@tool
def my_function(param: str) -> str:
    """This docstring becomes the tool's description."""
    return result
```

The decorator:
- Converts the function to a tool
- Extracts the name from the function name
- Uses the docstring as the tool's description
- Infers the arguments schema from type hints

### Tool Description

The tool's description (from the docstring) is crucial:
- **The LLM uses it to decide when to call the tool**
- Should clearly describe what the tool does
- Should mention when it's useful
- Example: "Retrieve product information from inventory based on product ID"

### Tool Attributes

Custom tools have three key attributes:

1. **`.name`**: The tool's name (from function name)
   ```python
   tool.name  # "get_product_info"
   ```

2. **`.description`**: The tool's description (from docstring)
   ```python
   tool.description  # "Retrieve product information..."
   ```

3. **`.args`**: The tool's input arguments schema
   ```python
   tool.args  # Shows parameter types and requirements
   ```

### Using Tools with Agents

To use custom tools with ReAct agents:

```python
from langgraph.prebuilt import create_react_agent

# Pass tools as a list
agent = create_react_agent(llm, [tool1, tool2, tool3])

# The agent will use tool descriptions to decide when to call them
response = agent.invoke({"messages": [("human", "question")]})
```

The agent automatically:
- Analyzes the question
- Matches it against tool descriptions
- Calls appropriate tools
- Uses tool outputs to answer

## Quiz

Test your understanding of custom tools! Run:

```bash
make quiz
```

The quiz covers:
- The `@tool` decorator
- How tool descriptions are used
- Tool attributes
- Creating and using custom tools

## Challenge

Put your skills to the test! Complete the coding challenge:

```bash
make challenge
```

The challenge will ask you to:
- Import the `@tool` decorator
- Create a custom tool
- Use the tool with a ReAct agent
- Invoke the agent correctly

## Next Steps

After completing this module, you'll be ready for:
- **08-RAG-document-loader**: Loading documents for RAG applications
- **09-RAG-document-splitter**: Splitting documents for processing
- **010-RAG-document-storage**: Storing documents for retrieval

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you've run `make install` to install all dependencies
2. **API Key Errors**: ReAct agents with custom tools require an OpenAI API key - check your `.env` file
3. **Tool Not Being Called**: Check that your tool's description clearly describes when it should be used
4. **Type Errors**: Make sure your function has proper type hints for parameters and return type
5. **bind_tools Error**: If you see `AttributeError: 'HuggingFacePipeline' object has no attribute 'bind_tools'`, this means you're trying to use a Hugging Face model. ReAct agents require OpenAI models.

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed: `make install`
2. Verify your `.env` file has the OpenAI API key: `make setup`
3. Try running the example directly: `python custom_tool_example.py`
4. Check the error messages for specific guidance
5. Ensure your tool's docstring is clear and descriptive

## Summary

Custom tools enable you to:
- ✅ Create domain-specific functions for agents
- ✅ Extend agent capabilities beyond pre-built tools
- ✅ Integrate with your own systems and data
- ✅ Control tool behavior with custom logic
- ✅ Build specialized agents for specific use cases

This is a powerful pattern for building intelligent systems tailored to your specific needs!

