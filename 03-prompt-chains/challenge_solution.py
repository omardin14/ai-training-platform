"""
Challenge Solution - For Reference Only

This file shows the complete solution to the challenge.
Only look at this if you're stuck!
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
# SOLUTION
# ============================================================================

# Step 1: Create a prompt template
template = "Explain {topic} in one sentence."
prompt = PromptTemplate.from_template(template=template)  # Answer: from_template

# Step 2: Create a chain using the pipe operator
chain = prompt | llm  # Answer: |

# Step 3: Invoke the chain
topic = "artificial intelligence"
response = chain.invoke({"topic": topic})  # Answer: invoke

# Extract and print the response
if use_openai:
    result = response.content if hasattr(response, 'content') else str(response)
else:
    result = str(response).strip()

print(f"\nQuestion: Explain {topic} in one sentence.")
print(f"Answer: {result}\n")

