"""
Challenge Solution - For Reference Only

This file shows the complete solution to the challenge.
Only look at this if you're stuck!
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for API key
openai_api_key = os.getenv("OPENAI_API_KEY")
use_openai = openai_api_key and openai_api_key != "your-openai-api-key-here"

# ============================================================================
# SOLUTION
# ============================================================================

if use_openai:
    from langchain_openai import ChatOpenAI  # Answer: ChatOpenAI
    model = ChatOpenAI(model="gpt-3.5-turbo")  # Answer: ChatOpenAI
else:
    from langchain_huggingface import HuggingFacePipeline
    model = HuggingFacePipeline.from_model_id(
        model_id="crumb/nano-mistral",
        task="text-generation",
        pipeline_kwargs={"max_new_tokens": 50}
    )

prompt = "What is Python in one sentence?"
response = model.invoke(prompt)  # Answer: invoke

if use_openai:
    result = response.content  # Answer: content
else:
    result = str(response).strip()

print(f"\nPrompt: {prompt}")
print(f"Response: {result}\n")

