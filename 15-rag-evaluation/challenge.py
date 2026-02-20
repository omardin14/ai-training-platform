"""
Challenge: RAG Evaluation

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Output evaluation using LLMs
- RAGAS faithfulness metric using the evaluate() API
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key or openai_api_key == "your-openai-api-key-here":
    print("Error: OPENAI_API_KEY not found. Please set it in .env file.")
    exit(1)

from langchain_openai import ChatOpenAI

# Create evaluation LLM
eval_llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# ============================================================================
# CHALLENGE: Complete the code below
# ============================================================================

# Step 1: Create prompt template for evaluation
# Replace XXXX___ with the correct import (PromptTemplate)
from langchain_core.prompts import XXXX___

prompt_template = """You are an evaluator comparing two answers.

Question: {query}
Expected answer: {answer}
Answer to evaluate: {result}

Respond with only CORRECT or INCORRECT:"""

# Replace XXXX___ with the correct class name (PromptTemplate)
prompt = XXXX___(
    input_variables=["query", "answer", "result"],
    template=prompt_template
)

# Step 2: Create faithfulness evaluator using RAGAS v0.4 API
# Replace XXXX___ with the correct function name (evaluate)
from ragas import XXXX___, EvaluationDataset, SingleTurnSample
from ragas.metrics._faithfulness import Faithfulness
from ragas.llms import LangchainLLMWrapper

from langchain_openai import OpenAIEmbeddings

llm = ChatOpenAI(model="gpt-4o-mini")

# Replace XXXX___ with the correct wrapper (LangchainLLMWrapper)
ragas_llm = XXXX___(llm)

# Replace XXXX___ with the correct metric class (Faithfulness)
faithfulness_metric = XXXX___(llm=ragas_llm)

# Test evaluation
query = "What are the main stages in document processing?"
predicted_answer = "Retrieval and generation"
ref_answer = "Retrieval and generation"

eval_chain = prompt | eval_llm
result = eval_chain.invoke({
    "query": query,
    "answer": ref_answer,
    "result": predicted_answer
})

print(f"Evaluation: {result.content.strip()}")

# Test faithfulness using RAGAS evaluate() API
# Replace XXXX___ with the correct class (SingleTurnSample)
sample = XXXX___(
    user_input="What are the main stages in document processing?",
    response="Document processing combines retrieval with generation.",
    retrieved_contexts=["Document processing systems combine document retrieval with text generation to provide accurate responses."]
)

# Replace XXXX___ with the correct class (EvaluationDataset)
dataset = XXXX___(samples=[sample])

# Replace XXXX___ with the correct function (evaluate)
eval_result = XXXX___(
    dataset=dataset,
    metrics=[faithfulness_metric],
)

faithfulness_score = eval_result.scores[0].get("faithfulness", 0.0)
print(f"Faithfulness Score: {faithfulness_score}")
print("\nChallenge completed!")
