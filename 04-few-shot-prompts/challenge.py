"""
Challenge: Complete the Few-Shot Prompt

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Creating examples for few-shot prompting
- Formatting examples with a template
- Building a few-shot prompt template
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
        pipeline_kwargs={"max_new_tokens": 50}
    )

# ============================================================================
# CHALLENGE: Complete the code below
# ============================================================================

# Step 1: Create examples list
examples = [
    {"concept": "loop", "explanation": "A way to repeat code"},
    {"concept": "function", "explanation": "A reusable block of code"},
    {"concept": "variable", "explanation": "A container for storing data"}
]

# Step 2: Import the required classes
# Replace XXXX___ with the correct imports (PromptTemplate, FewShotPromptTemplate)
from langchain_core.prompts import XXXX___, XXXX___

# Step 3: Create example prompt template
# Replace XXXX___ with the correct class and method
example_prompt = XXXX___.XXXX___(
    "Concept: {concept}\nExplanation: {explanation}"
)

# Step 4: Create few-shot prompt template
# Replace XXXX___ with the correct class name
prompt_template = XXXX___(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Concept: {input}",
    input_variables=["input"]
)

# Create chain and invoke
chain = prompt_template | llm
response = chain.invoke({"input": "array"})

# Extract and print response
if use_openai:
    result = response.content if hasattr(response, 'content') else str(response)
else:
    result = str(response).strip()

print(f"\nQuestion: Explain 'array'")
print(f"Answer: {result}\n")

