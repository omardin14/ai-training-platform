"""
Challenge Solution: Sequential Chain

This is the complete solution for the sequential chain challenge.
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
    llm = ChatOpenAI(model="gpt-3.5-turbo")
else:
    from langchain_huggingface import HuggingFacePipeline
    llm = HuggingFacePipeline.from_model_id(
        model_id="crumb/nano-mistral",
        task="text-generation",
        pipeline_kwargs={"max_new_tokens": 100}
    )

# ============================================================================
# SOLUTION: Complete code
# ============================================================================

# Step 1: Import the required classes
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Step 2: Create the first prompt template
first_prompt = PromptTemplate.from_template(
    template="Explain {topic} in simple terms."
)

# Step 3: Create the second prompt template
second_prompt = PromptTemplate.from_template(
    template="Summarize this explanation in one sentence: {explanation}"
)

# Step 4: Create the sequential chain
seq_chain = (
    {"explanation": first_prompt | llm | StrOutputParser()}
    | second_prompt
    | llm
    | StrOutputParser()
)

# Invoke the chain
response = seq_chain.invoke({"topic": "machine learning"})

# Print the result
print(f"\nTopic: machine learning")
print(f"Summary: {response}\n")

