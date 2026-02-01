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
# SOLUTION
# ============================================================================

from langchain_core.prompts import ChatPromptTemplate  # Answer: ChatPromptTemplate

prompt_template = ChatPromptTemplate.from_messages([  # Answer: from_messages
    ("system", "You are a helpful assistant."),
    ("human", "Explain {concept} in simple terms.")
])

concept = "machine learning"
formatted_messages = prompt_template.format_messages(concept=concept)  # Answer: format_messages

if use_openai:
    formatted_prompt = formatted_messages
else:
    prompt_parts = [msg.content for msg in formatted_messages]
    formatted_prompt = " ".join(prompt_parts)

response = model.invoke(formatted_prompt)

if use_openai:
    result = response.content if hasattr(response, 'content') else str(response)
else:
    result = str(response).strip()

print(f"\nQuestion: Explain {concept} in simple terms.")
print(f"Answer: {result}\n")

