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

examples = [
    {"concept": "loop", "explanation": "A way to repeat code"},
    {"concept": "function", "explanation": "A reusable block of code"},
    {"concept": "variable", "explanation": "A container for storing data"}
]

from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate  # Answer: PromptTemplate, FewShotPromptTemplate

example_prompt = PromptTemplate.from_template(  # Answer: PromptTemplate, from_template
    "Concept: {concept}\nExplanation: {explanation}"
)

prompt_template = FewShotPromptTemplate(  # Answer: FewShotPromptTemplate
    examples=examples,
    example_prompt=example_prompt,
    suffix="Concept: {input}",
    input_variables=["input"]
)

chain = prompt_template | llm
response = chain.invoke({"input": "array"})

if use_openai:
    result = response.content if hasattr(response, 'content') else str(response)
else:
    result = str(response).strip()

print(f"\nQuestion: Explain 'array'")
print(f"Answer: {result}\n")

