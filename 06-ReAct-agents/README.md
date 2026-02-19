# ReAct Agents

This module introduces **ReAct Agents** - agents that combine Reasoning and Acting to use tools and answer complex questions.

<!-- lesson:page What are ReAct Agents? -->
## What are ReAct Agents?

ReAct (Reasoning + Acting) agents are intelligent systems that can:
- **Reason** about what actions to take
- **Act** by using tools to perform actions
- **Answer questions** by combining reasoning with tool use
- **Decide automatically** when to use tools based on the question

Unlike simple LLMs, ReAct agents can interact with external tools to gather information or perform calculations.

## Concepts Covered

- **ReAct Agents**: Agents that reason and act
- **Tools**: Functions the agent can use (e.g., calculator, search)
- **Agent Creation**: Building agents with tools
- **Tool Selection**: How agents decide which tools to use

<!-- lesson:page How ReAct Agents Work -->
## How ReAct Agents Work

A ReAct agent follows this process:

1. **Receive Question**: The agent gets a question from the user
2. **Reason**: The agent thinks about what it needs to do
3. **Decide**: The agent decides if it needs to use a tool
4. **Act**: If needed, the agent calls a tool with appropriate inputs
5. **Process**: The agent uses the tool's output
6. **Answer**: The agent formulates and returns the final answer

### Example Flow:
```
Question: "What is 15 * 23 + 100?"
  ↓
Agent reasons: "I need to calculate this"
  ↓
Agent uses calculator tool: 15 * 23 = 345
  ↓
Agent uses calculator tool: 345 + 100 = 445
  ↓
Agent answers: "The result is 445"
```

## Understanding ReAct Agent Structure

Let's break down how a ReAct agent works:

```python
# Step 1: Load tools
from langchain_community.agent_toolkits.load_tools import load_tools
tools = load_tools(["llm-math"], llm=llm)

# Step 2: Create the agent
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(llm, tools)

# Step 3: Invoke the agent
response = agent.invoke({"messages": [("human", "What is 15 * 23 + 100?")]})
final_answer = response['messages'][-1].content
```

> **Note:** The `load_tools` function is from `langchain_community.agent_toolkits.load_tools`. This is the official way to load pre-built tools like the calculator. See the [LangChain documentation](https://reference.langchain.com/v0.3/python/community/agent_toolkits/langchain_community.agent_toolkits.load_tools.load_tools.html) for more information.

### Key Components:

1. **Tools**: Functions the agent can use
   - Example: Calculator tool for math operations
   - Tools extend the agent's capabilities

2. **Agent**: The reasoning and acting system
   - Created with `create_react_agent()`
   - Combines the LLM with available tools
   - Uses a ReAct prompt template

3. **Invocation**: How to use the agent
   - Pass messages in the format: `[("human", "question")]`
   - The agent processes and responds

### The Flow:

```
User Question: "What is 15 * 23 + 100?"
  ↓
Agent receives question
  ↓
Agent reasons: "I need to calculate this"
  ↓
Agent calls calculator tool: 15 * 23
  ↓
Tool returns: 345
  ↓
Agent calls calculator tool: 345 + 100
  ↓
Tool returns: 445
  ↓
Agent formulates answer: "The result is 445"
```

<!-- lesson:page Tools and Agent Reasoning -->
## Code Examples

### ReAct Agent Example (`react_agent_example.py`)

This example demonstrates:
- Loading tools using `load_tools()` from `langchain_community.agent_toolkits.load_tools`
- Creating a ReAct agent with `create_react_agent()` from `langgraph.prebuilt`
- Invoking the agent with a question
- How the agent uses tools automatically
- Extracting the final answer from the agent's response

**Key Features:**
- Uses the `llm-math` tool for mathematical calculations
- Agent automatically decides when to use the calculator tool
- Shows how tools extend agent capabilities beyond text generation
- Demonstrates the ReAct pattern: reasoning + acting

## Key Concepts Explained

### Tools

Tools are functions that agents can call to perform actions:
- **Calculator Tool** (`llm-math`): Performs mathematical calculations using the `numexpr` library
- **Search Tools**: Search the web or databases (available via `load_tools`)
- **Custom Tools**: You can create your own tools (covered in module 07)

Tools are loaded using `load_tools()` from `langchain_community.agent_toolkits.load_tools`. This function takes a list of tool names and an optional LLM (required for some tools like `llm-math`).

### Agent Reasoning

The agent automatically:
- Analyzes the question
- Decides if tools are needed
- Selects the appropriate tool
- Uses tool output to answer

### ReAct Prompt

The ReAct prompt template (handled internally by `create_react_agent`) guides the agent to:
- Think step by step (reasoning)
- Decide when to use tools (acting)
- Format tool calls correctly
- Combine tool results with reasoning
- Provide final answers based on tool outputs

The prompt is automatically managed by `langgraph.prebuilt.create_react_agent`, so you don't need to create it manually.

<!-- lesson:end -->

## Prerequisites

This module builds on the concepts from **05-sequential-chain**. Make sure you've completed that module first.

**Important**: ReAct agents require OpenAI models. They do not work with Hugging Face models.

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
   > **Note:** ReAct agents require an OpenAI API key. They will not work without it.

3. **Set up virtual environment and install dependencies:**
   ```bash
   make install
   ```
   This creates a Python virtual environment and installs all required packages.

**Model Selection:**
- **ReAct agents require OpenAI**: Uses OpenAI's GPT-3.5-turbo model
- **Hugging Face models are not supported** for ReAct agents

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
- `langchain-community`: For loading tools (`load_tools`)
- `langgraph`: For creating ReAct agents (`create_react_agent`)
- `numexpr`: Required by the `llm-math` tool for mathematical calculations
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
python react_agent_example.py
```

## Quiz

Test your understanding of ReAct agents! Run:

```bash
make quiz
```

The quiz covers:
- What ReAct agents are
- How agents use tools
- When agents decide to use tools
- The ReAct pattern

## Challenge

Put your skills to the test! Complete the coding challenge:

```bash
make challenge
```

The challenge will ask you to:
- Load tools
- Create a ReAct agent
- Invoke the agent correctly
- Extract the response

## Next Steps

After completing this module, you'll be ready for:
- **07-custom-tools**: Creating your own custom tools
- **08-RAG-document-loader**: Loading documents for RAG applications
- **09-RAG-document-splitter**: Splitting documents for processing

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you've run `make install` to install all dependencies
2. **API Key Errors**: ReAct agents require an OpenAI API key - check your `.env` file
3. **Tool Loading Errors**: Make sure `langchain-community` is installed
4. **Agent Not Using Tools**: Check that tools are loaded correctly and the question requires tool use
5. **Python 3.14 Compatibility**: If you encounter `TypeError: 'function' object is not subscriptable`, this is a known issue with `langchain_classic` and Python 3.14. The Makefile automatically applies a compatibility fix during installation.

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed: `make install`
2. Verify your `.env` file has the OpenAI API key: `make setup`
3. Try running the example directly: `python react_agent_example.py`
4. Check the error messages for specific guidance
5. For Python 3.14 users: The compatibility fix is automatically applied. If you reinstall packages, you may need to run `make install` again to reapply the fix.
