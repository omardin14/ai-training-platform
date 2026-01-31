# LangChain Models

This module introduces the fundamental concept of using different language models with LangChain. LangChain provides a unified interface to work with various LLM providers, making it easy to switch between different models.

## Why LangChain?

Consider a real-world scenario: building a **customer support chatbot** that uses LLMs to converse with customers. The chatbot needs to:

- Provide product information and recommendations
- Respond to customers experiencing issues with placing orders
- Ensure responses are based on existing support articles that can be easily tweaked and maintained

### Components to Manage

To build such a system, you need to manage several components:

- **An LLM** - which may be from a whole host of different providers, both proprietary and open-source
- **A mechanism** to help the model decide whether to provide product information or advise on troubleshooting issues
- **A database** of customer support articles for the model to use
- **A mechanism** for finding and integrating them into the chatbot

**LangChain can be used to manage all these components**, providing a unified framework that simplifies working with different LLM providers and building complex AI applications.

### Working with LangChain Models

LangChain abstracts away the differences between model providers, making it easy to switch between them:

- **To pass a model a prompt**, we use the `.invoke()` method - this works consistently across all model types
- **You can use completely different models** from different providers (OpenAI, Hugging Face, Anthropic, etc.)
- **You can use models like Hugging Face** that are downloaded locally, or **models that require API requests** like OpenAI
- **For LangChain, switching between providers** often only requires changing one class and its arguments

> **Note:** For working with open-source models downloaded into a local directory, **Hugging Face** is an excellent choice for finding an appropriate model.

## Concepts Covered

- **OpenAI Models**: Using GPT models via OpenAI's API
- **Hugging Face Models**: Using open-source models from Hugging Face
- **Model Abstraction**: How LangChain provides a consistent interface across different providers

## Prerequisites

### Getting an OpenAI API Key

1. Go to [OpenAI's website](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to the [API Keys section](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key and store it securely

### Setting Up Your Environment

**Complete Setup Steps:**

1. **Create the `.env` file** using the Makefile:
   ```bash
   make setup
   ```

2. **Edit the `.env` file** and add your API keys:
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   HUGGINGFACEHUB_API_TOKEN=your-token-here  # Optional
   ```

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
# Run OpenAI example (creates venv and installs deps if needed)
make openai

# Run Hugging Face example (creates venv and installs deps if needed)
make huggingface

# Run both examples
make all
```

> **Note:** The first time you run any command, it will automatically set up the virtual environment and install dependencies if needed.

### Manual Execution

If you set up the environment manually, activate it first:

```bash
# Activate virtual environment
source venv/bin/activate  # On macOS/Linux

# Run examples
python openai_example.py
python huggingface_example.py
```

## Code Examples

Both examples follow the same pattern, demonstrating LangChain's unified interface:

1. **Load the model** - Initialize the model with appropriate parameters
2. **Invoke with a prompt** - Use the `.invoke()` method (works the same for all providers)
3. **Get the response** - Receive and use the model's output

### OpenAI Example (`openai_example.py`)

Simple example demonstrating:
- Loading an OpenAI model using `ChatOpenAI`
- Invoking the model with a prompt using `.invoke()`
- Getting the response

### Hugging Face Example (`huggingface_example.py`)

Simple example demonstrating:
- Loading a Hugging Face model using `HuggingFacePipeline` (runs locally)
- Invoking the model with a prompt using `.invoke()` (same method!)
- Getting the response

> **Note:** The model will be downloaded on first run. This may take a few minutes depending on your internet connection.

Notice how both examples use the same `.invoke()` method, even though they're using completely different model providers. This is the power of LangChain's abstraction!

## Key Differences

| Feature | OpenAI | Hugging Face |
|---------|--------|--------------|
| **Access** | API-based (requires internet) | Can run locally |
| **Cost** | Pay per token | Free (but requires compute) |
| **Speed** | Fast (cloud infrastructure) | Depends on local hardware |
| **Privacy** | Data sent to OpenAI | Data stays local |
| **Setup** | API key required | Model download required |

## Next Steps

After understanding models, proceed to:
- **02-prompt-templates**: Learn how to create and use prompt templates
- **03-prompt-chains**: Discover how to chain multiple prompts together

