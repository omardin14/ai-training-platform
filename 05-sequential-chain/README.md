# Sequential Chains

This module introduces **Sequential Chains** - connecting multiple chains together where the output of one chain becomes the input to the next chain.

<!-- lesson:page What are Sequential Chains? -->
## What are Sequential Chains?

Sequential chains allow you to create multi-step workflows where:
- The output of the first chain feeds into the second chain
- Each step processes information and passes it forward
- Complex tasks can be broken down into simpler, sequential steps
- Data flows from one processing step to the next

## Concepts Covered

- **Sequential Chains**: Multi-step processing workflows
- **StrOutputParser**: Extracting text from LLM responses
- **Chain Composition**: Connecting multiple chains together
- **Data Flow**: Passing outputs between chains

<!-- lesson:page How Sequential Chains Work -->
## How Sequential Chains Work

A sequential chain connects multiple processing steps:

1. **First Chain**: Takes initial input and processes it
2. **Output Parser**: Extracts the text from the LLM response
3. **Second Chain**: Takes the output from the first chain as input
4. **Final Output**: The result of the last chain

### Example Flow:
```
Input: {activity}
  ↓
[Prompt 1] → [LLM] → [Output Parser] → learning_plan
  ↓
[Prompt 2] → [LLM] → [Output Parser] → final_plan
```

The output of the first chain becomes the input variable for the second chain.

## Understanding Sequential Chain Structure

Let's break down how a sequential chain works:

### Step 1: Create the First Prompt Template

The first prompt takes the initial input and asks the LLM for a detailed response:

```python
explanation_prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in detail, covering its key concepts and how it works."
)
```

### Step 2: Create the Second Prompt Template

The second prompt takes the output of the first chain as its input variable (`detailed_explanation`):

```python
summary_prompt = PromptTemplate(
    input_variables=["detailed_explanation"],
    template="Based on this explanation: {detailed_explanation}\n\nCreate a simple, beginner-friendly summary in 2-3 sentences."
)
```

### Step 3: Create the Sequential Chain

Connect both prompts using dictionary syntax. The first chain's output is passed as `"detailed_explanation"` to the second chain:

```python
seq_chain = (
    {"detailed_explanation": explanation_prompt | llm | StrOutputParser()}
    | summary_prompt
    | llm
    | StrOutputParser()
)
```

### Key Components:

1. **First Chain**: `explanation_prompt | llm | StrOutputParser()`
   - Formats the prompt with the topic
   - Sends to LLM
   - Extracts text with StrOutputParser()

2. **Dictionary Syntax**: `{"detailed_explanation": ...}`
   - Passes the output of the first chain to the second chain
   - The key `"detailed_explanation"` matches the input variable in `summary_prompt`

3. **Second Chain**: `summary_prompt | llm | StrOutputParser()`
   - Formats the prompt with the detailed explanation from step 1
   - Sends to LLM
   - Extracts final text

### The Flow:

```
Input: {"topic": "quantum computing"}
  ↓
Step 1: explanation_prompt formats → "Explain quantum computing in detail..."
  ↓
LLM generates detailed explanation
  ↓
StrOutputParser() extracts text → "Quantum computing uses quantum mechanics..."
  ↓
Step 2: summary_prompt formats → "Based on this explanation: Quantum computing uses... Create a simple summary..."
  ↓
LLM generates simplified summary
  ↓
StrOutputParser() extracts final text → "Quantum computing is a type of computing..."
```

<!-- lesson:page Key Concepts Explained -->
## Code Examples

### Sequential Chain Example (`sequential_chain_example.py`)

This example demonstrates:
- Creating two prompt templates
- Building a sequential chain that connects them
- Using `StrOutputParser()` to extract text from responses
- Passing data between chains using dictionary syntax

**Key Features:**
- First chain generates a detailed explanation of a topic
- Second chain creates a simplified summary from the detailed explanation
- Shows how outputs flow from one chain to the next

## Key Concepts Explained

### StrOutputParser()

`StrOutputParser()` extracts the text content from an LLM response. It's essential in sequential chains because:
- LLM responses are objects, not plain text
- The next chain needs text input, not response objects
- It converts `response.content` (or similar) to a simple string

### Dictionary Syntax in Chains

When you write:
```python
{"learning_plan": learning_prompt | llm | StrOutputParser()}
```

This means:
- Run the chain: `learning_prompt | llm | StrOutputParser()`
- Take its output
- Pass it as the value for the key `"learning_plan"`
- This value will be used to fill `{learning_plan}` in the next prompt

### Why Sequential Chains?

Sequential chains are useful when:
- You need to process information in multiple steps
- Each step depends on the previous step's output
- You want to break complex tasks into simpler parts
- You need to transform or refine information progressively

<!-- lesson:end -->

## Prerequisites

This module builds on the concepts from **03-prompt-chains** and **04-few-shot-prompts**. Make sure you've completed those modules first.

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
- **If `OPENAI_API_KEY` is set**: Uses OpenAI's GPT-3.5-turbo model (highly recommended for sequential chains)
- **If `OPENAI_API_KEY` is not set**: Uses Hugging Face's local model (crumb/nano-mistral)
  - ⚠️ **Important**: Sequential chains work much better with OpenAI models. Smaller Hugging Face models often struggle to follow the format correctly. For best results, strongly consider using an OpenAI API key.

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
python sequential_chain_example.py
```

## Quiz

Test your understanding of sequential chains! Run:

```bash
make quiz
```

The quiz covers:
- How sequential chains work
- The role of StrOutputParser()
- How data flows between chains
- Dictionary syntax for passing data

## Challenge

Put your skills to the test! Complete the coding challenge:

```bash
make challenge
```

The challenge will ask you to:
- Create prompt templates
- Build a sequential chain
- Use StrOutputParser() correctly
- Pass data between chains

## Next Steps

After completing this module, you'll be ready for:
- **06-langchain-agents**: Building agents that can use tools
- **07-custom-tools**: Creating custom tools for agents
- **08-RAG-document-loader**: Loading documents for RAG applications

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you've run `make install` to install all dependencies
2. **API Key Errors**: Check that your `.env` file has the correct API key format
3. **Model Loading Issues**: Hugging Face models download on first run - be patient!
4. **Output Format Issues**: Make sure you're using `StrOutputParser()` to extract text

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed: `make install`
2. Verify your `.env` file is set up correctly: `make setup`
3. Try running the example directly: `python sequential_chain_example.py`
4. Check the error messages for specific guidance
