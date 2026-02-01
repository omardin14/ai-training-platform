# Prompt Templates

This module introduces **Prompt Templates** - LangChain components that act as reusable recipes for defining prompts for LLMs.

## What are Prompt Templates?

Prompt templates are structured ways to create prompts for language models. Instead of writing prompts as plain strings every time, prompt templates allow you to:

- **Define reusable prompt structures** that can be filled in with different values
- **Maintain consistency** across your application
- **Separate prompt logic** from your application code
- **Make prompts easier to maintain and update**

## Concepts Covered

- **Basic Prompt Templates**: Creating simple templates with variables
- **Template Formatting**: Using different template formats (f-string style, Jinja2)
- **Reusability**: How templates make prompts reusable across different contexts

## Prompt Template Components

Prompt templates can include different types of content:

- **Instructions** - Directives for the model on how to behave (usually in system messages)
- **Questions** - Queries you want the model to answer (usually in human messages)
- **Examples** - Sample inputs/outputs for the model to draw on (few-shot learning)
- **Additional context** - Any extra information that might help the model complete the task

### Message Roles

In `ChatPromptTemplate`, messages have different roles:

| Role | Purpose | Example |
|------|---------|---------|
| **`system`** | Sets instructions, context, or behavior guidelines | `"You are a helpful assistant."` |
| **`human`** | Represents the user's input, questions, or requests | `"Explain {topic} in one sentence."` |
| **`ai`** | Represents the assistant's previous responses (for conversations) | `"I'd be happy to help!"` |

> **Note**: In our simple example, we use `system` for instructions and `human` for the user's question. The `ai` role is used when building conversational chains with multiple turns.

## Prerequisites

This module builds on the concepts from **01-langchain-models**. Make sure you've completed that module first.

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
- **If `OPENAI_API_KEY` is set**: Uses OpenAI's GPT-3.5-turbo model
- **If `OPENAI_API_KEY` is not set**: Uses Hugging Face's local model (crumb/nano-mistral)

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
python prompt_template_example.py
```

## Understanding Prompt Template Structure

Let's break down the components of a prompt template using our example:

```python
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "Explain {topic} in one sentence.")
])
```

### 1. **ChatPromptTemplate.from_messages()**
   - This method creates a template from a list of messages
   - Each message defines a role and content

### 2. **System Message** - `("system", "You are a helpful assistant.")`
   - **Role**: `"system"` - Instructions for the model's behavior
   - **Content**: `"You are a helpful assistant."` - Sets the context/instructions
   - **Purpose**: Tells the model how to behave, what role to play, or what guidelines to follow
   - This is an **INSTRUCTION** component

### 3. **Human Message** - `("human", "Explain {topic} in one sentence.")`
   - **Role**: `"human"` - Represents the user's input
   - **Content**: `"Explain {topic} in one sentence."` - The actual question/request
   - **Purpose**: Contains the user's query or request
   - This is a **QUESTION** component

### 4. **Variable Placeholder** - `{topic}`
   - **Syntax**: `{variable_name}` - Curly braces define a variable
   - **Purpose**: A placeholder that will be filled in with an actual value later
   - **Example**: When formatted with `topic="quantum computing"`, becomes:
     `"Explain quantum computing in one sentence."`

### 5. **Formatting the Template**
   ```python
   formatted_messages = prompt_template.format_messages(topic="quantum computing")
   ```
   - Replaces `{topic}` with the actual value
   - Returns formatted messages ready to send to the model

### Complete Flow:
1. **Create Template** → Define structure with variables
2. **Format Template** → Fill in variables with actual values
3. **Invoke Model** → Send formatted prompt to the model
4. **Get Response** → Receive the model's output

## Code Examples

### Prompt Template Example (`prompt_template_example.py`)

The example demonstrates:
- **Creating a prompt template** with system instructions and a human question
- **Using variables** (`{topic}`) as placeholders
- **Formatting the template** by filling in the variable with an actual value
- **Using the formatted prompt** with a model (OpenAI or Hugging Face)

## Test Your Knowledge

After running the examples, test your understanding with the interactive quiz:

```bash
make quiz
```

The quiz includes:
- **3 questions** covering key concepts about prompt templates
- **Multiple choice format** with 3 options per question
- **Immediate feedback** on each answer
- **Score calculation** at the end
- **Personalized messages** based on your performance

### Quiz Topics

The quiz tests your knowledge of:
1. The `ChatPromptTemplate` class for creating templates
2. The `.format_messages()` method for filling in variables
3. Variable placeholder syntax (`{variable_name}`)

### Scoring

- **3/3**: 🎉 Perfect! You've mastered prompt templates!
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

1. **Import the template class** - Use the correct import for `ChatPromptTemplate`
2. **Create a template** - Use the correct method to create a template from messages
3. **Format the template** - Use the correct method to fill in variables

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
- **Reference**: Look at `prompt_template_example.py` for working examples
- **Solution**: Check `challenge_solution.py` if you're completely stuck (but try first!)

### What You'll Learn

By completing the challenge, you'll reinforce:
- How to import and use `ChatPromptTemplate`
- How to create templates with system and human messages
- How to format templates with actual values
- How to use formatted templates with models

## Key Benefits

| Feature | Without Templates | With Templates |
|---------|-------------------|----------------|
| **Reusability** | Rewrite prompts each time | Define once, reuse many times |
| **Maintainability** | Update prompts in multiple places | Update in one place |
| **Consistency** | Easy to have inconsistencies | Ensures consistent structure |
| **Flexibility** | Hard to parameterize | Easy to fill in variables |

## Next Steps

After understanding prompt templates, proceed to:
- **03-prompt-chains**: Discover how to chain multiple prompts together
- **04-few-shot-prompts**: Learn about providing examples to improve model responses

