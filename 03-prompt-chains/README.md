# Prompt Chains

This module introduces **Prompt Chains** - connecting prompt templates with models using the pipe operator (`|`) in LangChain.

## What are Prompt Chains?

Prompt chains allow you to connect LangChain components together in a clean, readable way. The pipe operator (`|`) lets you:

- **Chain components** - Connect prompt templates directly with models
- **Simplify code** - Write `prompt | llm` instead of manual formatting and invocation
- **Build workflows** - Create reusable chains that can be invoked with different inputs
- **Maintain consistency** - Use the same pattern across different LangChain components

## Concepts Covered

- **Pipe Operator (`|`)**: The syntax for chaining LangChain components
- **Prompt Template Chaining**: Connecting prompt templates with LLMs
- **Chain Invocation**: How to invoke chains with input variables

## How Prompt Chains Work

A prompt chain connects a prompt template with a model using the pipe operator:

```python
# Create a prompt template
template = "You are a helpful AI assistant. Answer the question: {question}"
prompt = PromptTemplate.from_template(template=template)

# Create a chain using the pipe operator
llm_chain = prompt | llm

# Invoke the chain
response = llm_chain.invoke({"question": "What is LangChain?"})
```

### Flow:
```
Input: {"question": "What is LangChain?"}
    ↓
[Prompt Template formats the template]
    ↓
Formatted: "You are a helpful AI assistant. Answer the question: What is LangChain?"
    ↓
[LLM processes the prompt]
    ↓
Output: Response from the model
```

## Prerequisites

This module builds on the concepts from **02-prompt-templates**. Make sure you've completed that module first.

### Setting Up Your Environment

**Complete Setup Steps:**

1. **Create the `.env` file** using the Makefile:
   ```bash
   make setup
   ```
   This creates a `.env` file from `.env.example` (or creates a template if it doesn't exist).

2. **Optional: Edit the `.env` file** and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   ```
   > **Note:** If you don't set an API key, the example will automatically use a Hugging Face model instead!

3. **Set up virtual environment and install dependencies:**
   ```bash
   make install
   ```
   This creates a Python virtual environment and installs all required packages.

**Model Selection:**
- **If `OPENAI_API_KEY` is set**: Uses OpenAI's GPT-3.5-turbo model (recommended for best results)
- **If `OPENAI_API_KEY` is not set**: Uses Hugging Face's local model (crumb/nano-mistral)
  - ⚠️ **Note**: Smaller Hugging Face models may not follow instructions as precisely as OpenAI models. For best results, consider using an OpenAI API key.

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
python prompt_chain_example.py
```

## Test Your Knowledge

After running the examples, test your understanding with the interactive quiz:

```bash
make quiz
```

The quiz includes:
- **3 questions** covering key concepts about prompt chains
- **Multiple choice format** with 3 options per question
- **Immediate feedback** on each answer
- **Score calculation** at the end
- **Personalized messages** based on your performance

### Quiz Topics

The quiz tests your knowledge of:
1. The pipe operator (`|`) used for chaining components
2. The `.invoke()` method for running chains
3. How chains connect components together

### Scoring

- **3/3**: 🎉 Perfect! You've mastered prompt chains!
- **2/3**: 👍 Great job! You have a good understanding.
- **1/3**: 📚 Good start! Review the concepts you missed.
- **0/3**: 📖 Don't worry! Review the README and examples.

## Coding Challenge

Put your knowledge to the test with a hands-on coding challenge:

```bash
make challenge
```

### Challenge Overview

The challenge requires you to complete a Python script by filling in missing code. You'll need to:

1. **Create a prompt template** - Use the correct method to create a template from a string
2. **Chain components** - Use the pipe operator to connect the prompt with the model
3. **Invoke the chain** - Use the correct method to run the chain with input variables

### How It Works

1. **Open `challenge.py`** - This file contains code with `XXXX___` placeholders
2. **Replace the placeholders** - Fill in the missing code based on what you've learned
3. **Test your solution** - Run `make challenge` to check if your code works
4. **Get hints** - If you're stuck, the Makefile will provide helpful hints

### Challenge File Structure

The challenge file (`challenge.py`) includes:
- Complete setup code (model loading, imports)
- Three `XXXX___` placeholders that need to be filled in
- Clear comments explaining what each step should do
- Working code that will run once completed

### Getting Help

- **Hints**: The Makefile provides hints if you have placeholders remaining
- **Reference**: Look at `prompt_chain_example.py` for working examples
- **Solution**: Check `challenge_solution.py` if you're completely stuck (but try first!)

### What You'll Learn

By completing the challenge, you'll reinforce:
- How to create prompt templates
- The syntax for chaining components
- How to invoke chains with variables
- Practical application of the concepts

## Understanding Prompt Chain Structure

Let's break down how a prompt chain works using our example:

```python
# Step 1: Create a prompt template
template = "You are a helpful AI assistant. Answer the question: {question}"
prompt = PromptTemplate.from_template(template=template)

# Step 2: Create a chain using the pipe operator
llm_chain = prompt | llm

# Step 3: Invoke the chain with input variables
response = llm_chain.invoke({"question": "How does LangChain make LLM application development easier?"})
```

### Key Components:

1. **Prompt Template** - `PromptTemplate.from_template()`
   - Creates a reusable template with variable placeholders
   - Variables are defined using `{variable_name}` syntax

2. **Pipe Operator (`|`)** - Connects components
   - `prompt | llm` chains the prompt template with the model
   - The pipe operator is LangChain's way of connecting components

3. **Chain Invocation** - `.invoke()`
   - Takes a dictionary with variable values
   - Automatically formats the template → sends to LLM → returns response

### The Magic of the Pipe Operator:

The pipe operator (`|`) is a clean, Pythonic way to connect LangChain components. Instead of:
```python
# Manual approach (more verbose)
formatted = prompt.format(question="What is LangChain?")
response = llm.invoke(formatted)
```

You can write:
```python
# Chain approach (cleaner)
chain = prompt | llm
response = chain.invoke({"question": "What is LangChain?"})
```

## Code Examples

### Prompt Chain Example (`prompt_chain_example.py`)

The example demonstrates:
- **Creating a prompt template** with `PromptTemplate.from_template()`
- **Chaining the template with a model** using the pipe operator (`|`)
- **Invoking the chain** with `.invoke()` and a dictionary of variables
- **Understanding the flow** from template → model → response

## Key Benefits

| Feature | Without Chains | With Chains |
|---------|----------------|-------------|
| **Code Clarity** | Multiple steps, verbose | Single line: `prompt \| llm` |
| **Reusability** | Hard to reuse | Chain can be reused multiple times |
| **Maintainability** | Changes in multiple places | Update chain definition once |
| **Readability** | Less intuitive flow | Clear component connections |

## The Pipe Operator Pattern

The pipe operator (`|`) is a powerful pattern in LangChain that works with many components:

- `prompt | llm` - Chain prompt with model
- `prompt1 | prompt2 | llm` - Chain multiple prompts
- `chain1 | chain2` - Chain multiple chains together

This pattern makes it easy to build complex workflows from simple components!

## Next Steps

After understanding prompt chains, proceed to:
- **04-few-shot-prompts**: Learn about providing examples to improve model responses
- **05-sequential-chain**: Discover more advanced chaining patterns with multiple steps
