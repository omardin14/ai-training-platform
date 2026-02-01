"""
Challenge: Complete the Prompt Chain

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Creating prompt templates
- Using the pipe operator to chain components
- Invoking chains with input variables
"""

import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Check for API key
openai_api_key = os.getenv("OPENAI_API_KEY")
use_openai = openai_api_key and openai_api_key != "your-openai-api-key-here"

if use_openai:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-3.5-turbo")
else:
    from langchain_huggingface import HuggingFacePipeline
    llm = HuggingFacePipeline.from_model_id(
        model_id="crumb/nano-mistral",
        task="text-generation",
        pipeline_kwargs={"max_new_tokens": 50}
    )

# ============================================================================
# CHALLENGE: Complete the code below
# ============================================================================

# Step 1: Create a prompt template
# Replace XXXX___ with the correct method to create a template from a string
template = "Explain {topic} in one sentence."
prompt = PromptTemplate.XXXX___(template=template)

# Step 2: Create a chain using the pipe operator
# Replace XXXX___ with the correct operator to chain the prompt with the model
chain = prompt XXXX___ llm

# Step 3: Invoke the chain
# Replace XXXX___ with the correct method to run the chain
topic = "artificial intelligence"
response = chain.XXXX___({"topic": topic})

# Extract and print the response
if use_openai:
    result = response.content if hasattr(response, 'content') else str(response)
else:
    result = str(response).strip()

print(f"\nQuestion: Explain {topic} in one sentence.")
print(f"Answer: {result}\n")

