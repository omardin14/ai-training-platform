"""
Challenge: Complete the Model Invocation

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Loading a model with LangChain
- Invoking a model with a prompt
- Getting the response from the model
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for API key
openai_api_key = os.getenv("OPENAI_API_KEY")
use_openai = openai_api_key and openai_api_key != "your-openai-api-key-here"

# ============================================================================
# CHALLENGE: Complete the code below
# ============================================================================

if use_openai:
    # Step 1: Import the OpenAI model class
    # Replace XXXX___ with the correct import (ChatOpenAI)
    from langchain_openai import XXXX___
    
    # Step 2: Create an instance of the model
    # Replace XXXX___ with the correct class name
    model = XXXX___(model="gpt-3.5-turbo")
else:
    from langchain_huggingface import HuggingFacePipeline
    model = HuggingFacePipeline.from_model_id(
        model_id="crumb/nano-mistral",
        task="text-generation",
        pipeline_kwargs={"max_new_tokens": 50}
    )

# Step 3: Invoke the model with a prompt
# Replace XXXX___ with the correct method to send a prompt to the model
prompt = "What is Python in one sentence?"
response = model.XXXX___(prompt)

# Step 4: Extract the response content
# Replace XXXX___ with the correct attribute to get the response text
if use_openai:
    result = response.XXXX___
else:
    result = str(response).strip()

print(f"\nPrompt: {prompt}")
print(f"Response: {result}\n")

