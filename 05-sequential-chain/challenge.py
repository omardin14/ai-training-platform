"""
Challenge: Complete the Sequential Chain

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Creating prompt templates
- Building sequential chains
- Using StrOutputParser to extract text
- Passing data between chains
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
# CHALLENGE: Complete the code below
# ============================================================================

# Step 1: Import the required classes
# Replace XXXX___ with the correct imports (PromptTemplate, StrOutputParser)
from langchain_core.prompts import XXXX___
from langchain_core.output_parsers import XXXX___

# Step 2: Create the first prompt template
# Replace XXXX___ with the correct class and method
first_prompt = XXXX___.XXXX___(
    template="Explain {topic} in simple terms."
)

# Step 3: Create the second prompt template
# Replace XXXX___ with the correct class and method
second_prompt = XXXX___.XXXX___(
    template="Summarize this explanation in one sentence: {explanation}"
)

# Step 4: Create the sequential chain
# Replace XXXX___ with the correct class name (StrOutputParser)
seq_chain = (
    {"explanation": first_prompt | llm | XXXX___()}
    | second_prompt
    | llm
    | XXXX___()
)

# Invoke the chain
response = seq_chain.invoke({"topic": "machine learning"})

# Print the result
print(f"\nTopic: machine learning")
print(f"Summary: {response}\n")

