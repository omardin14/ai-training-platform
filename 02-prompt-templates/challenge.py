"""
Challenge: Complete the Prompt Template

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Creating prompt templates with ChatPromptTemplate
- Formatting templates with variables
- Using formatted prompts with models
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for API key
openai_api_key = os.getenv("OPENAI_API_KEY")
use_openai = openai_api_key and openai_api_key != "your-openai-api-key-here"

if use_openai:
    from langchain_openai import ChatOpenAI
    model = ChatOpenAI(model="gpt-3.5-turbo")
else:
    from langchain_huggingface import HuggingFacePipeline
    model = HuggingFacePipeline.from_model_id(
        model_id="crumb/nano-mistral",
        task="text-generation",
        pipeline_kwargs={"max_new_tokens": 50}
    )

# ============================================================================
# CHALLENGE: Complete the code below
# ============================================================================

# Step 1: Import the prompt template class
# Replace XXXX___ with the correct import (ChatPromptTemplate)
from langchain_core.prompts import XXXX___

# Step 2: Create a prompt template
# Replace XXXX___ with the correct method to create a template from messages
prompt_template = XXXX___.XXXX___([
    ("system", "You are a helpful assistant."),
    ("human", "Explain {concept} in simple terms.")
])

# Step 3: Format the template with a value
# Replace XXXX___ with the correct method to fill in the variable
concept = "machine learning"
formatted_messages = prompt_template.XXXX___(concept=concept)

# Step 4: Convert format if needed and invoke the model
if use_openai:
    formatted_prompt = formatted_messages
else:
    prompt_parts = [msg.content for msg in formatted_messages]
    formatted_prompt = " ".join(prompt_parts)

response = model.invoke(formatted_prompt)

# Extract and print the response
if use_openai:
    result = response.content if hasattr(response, 'content') else str(response)
else:
    result = str(response).strip()

print(f"\nQuestion: Explain {concept} in simple terms.")
print(f"Answer: {result}\n")

