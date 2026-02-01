# Few-Shot Prompts

This module introduces **Few-Shot Prompts** - providing examples to the model to help it understand the desired format and behavior.

## What are Few-Shot Prompts?

Few-shot prompting is a technique where you provide the model with a few examples of the task you want it to perform. This helps the model:

- **Understand the format** - See how inputs and outputs should be structured
- **Learn the pattern** - Recognize the relationship between examples
- **Improve accuracy** - Better results by following the provided examples
- **Maintain consistency** - Produce outputs in the same style as the examples

## Concepts Covered

- **Few-Shot Prompting**: Providing examples to guide model behavior
- **Example Templates**: Structuring examples for the model
- **FewShotPromptTemplate**: LangChain's class for creating few-shot prompts

## How Few-Shot Prompts Work

A few-shot prompt includes:

1. **Examples** - A list of input/output pairs showing the desired behavior
2. **Example Prompt** - A template that formats each example
3. **Suffix** - The actual question/task you want the model to complete
4. **Input Variables** - Variables that will be filled in when invoking

### Example Structure:
```
Example 1: Input → Output
Example 2: Input → Output
Example 3: Input → Output
---
Your Question: {input}
```

The model learns from the examples and applies the same pattern to your question.

## Prerequisites

This module builds on the concepts from **03-prompt-chains**. Make sure you've completed that module first.

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
- **If `OPENAI_API_KEY` is set**: Uses OpenAI's GPT-3.5-turbo model (highly recommended for few-shot prompts)
- **If `OPENAI_API_KEY` is not set**: Uses Hugging Face's local model (crumb/nano-mistral)
  - ⚠️ **Important**: Few-shot prompts work much better with OpenAI models. Smaller Hugging Face models often struggle to follow the example format correctly. For best results with few-shot prompting, strongly consider using an OpenAI API key.

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
python few_shot_example.py
```

## Understanding Few-Shot Prompt Structure

Let's break down how a few-shot prompt works:

```python
# Step 1: Define examples
examples = [
    {"input": "happy", "output": "joyful"},
    {"input": "sad", "output": "melancholy"},
    {"input": "angry", "output": "furious"}
]

# Step 2: Create a template for formatting each example
example_prompt = PromptTemplate.from_template("Word: {input}\nSynonym: {output}")

# Step 3: Create the few-shot prompt template
prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Word: {input}",
    input_variables=["input"]
)
```

### Key Components:

1. **Examples List** - A list of dictionaries showing input/output pairs
2. **Example Prompt** - A template that formats each example consistently
3. **FewShotPromptTemplate** - Combines examples with your actual question
4. **Suffix** - The format for your actual input question

### The Flow:

```
Examples:
  Word: happy → Synonym: joyful
  Word: sad → Synonym: melancholy
  Word: angry → Synonym: furious
---
Your Question:
  Word: excited
```

The model sees the pattern and generates: "Synonym: thrilled"

## Code Examples

### Few-Shot Example (`few_shot_example.py`)

The example demonstrates:
- **Creating examples** as a list of dictionaries
- **Formatting examples** with an example prompt template
- **Building a few-shot prompt** with `FewShotPromptTemplate`
- **Using the prompt** with a model to get responses following the example pattern

## Key Benefits

| Feature | Zero-Shot | Few-Shot |
|---------|-----------|----------|
| **Examples Provided** | None | 2-5 examples |
| **Accuracy** | Good | Better (learns from examples) |
| **Format Consistency** | May vary | Follows example format |
| **Pattern Recognition** | Limited | Learns the pattern |
| **Use Case** | Simple tasks | Complex or specific formats |

## Test Your Knowledge

After running the examples, test your understanding with the interactive quiz:

```bash
make quiz
```

The quiz includes:
- **3 questions** covering key concepts about few-shot prompts
- **Multiple choice format** with 3 options per question
- **Immediate feedback** on each answer
- **Score calculation** at the end
- **Personalized messages** based on your performance

### Quiz Topics

The quiz tests your knowledge of:
1. What few-shot prompting is and why it's useful
2. The `FewShotPromptTemplate` class
3. How examples help the model understand patterns

### Scoring

- **3/3**: 🎉 Perfect! You've mastered few-shot prompts!
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

1. **Create examples** - Define example input/output pairs
2. **Create example prompt** - Format examples with a template
3. **Build few-shot template** - Use `FewShotPromptTemplate` to combine everything

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
- **Reference**: Look at `few_shot_example.py` for working examples
- **Solution**: Check `challenge_solution.py` if you're completely stuck (but try first!)

### What You'll Learn

By completing the challenge, you'll reinforce:
- How to structure examples for few-shot prompting
- How to create example prompt templates
- How to use `FewShotPromptTemplate` to combine examples
- How to invoke few-shot prompts with models

## Next Steps

After understanding few-shot prompts, proceed to:
- **05-sequential-chain**: Discover more advanced chaining patterns with multiple steps

