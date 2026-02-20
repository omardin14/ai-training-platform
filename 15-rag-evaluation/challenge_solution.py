"""
Challenge Solution: RAG Evaluation

This is the complete solution for the RAG evaluation challenge.
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
# SOLUTION: Complete code
# ============================================================================

# Step 1: Create prompt template for evaluation
from langchain_core.prompts import PromptTemplate

prompt_template = """You are an evaluator comparing two answers.

Question: {query}
Expected answer: {answer}
Answer to evaluate: {result}

Respond with only CORRECT or INCORRECT:"""

prompt = PromptTemplate(
    input_variables=["query", "answer", "result"],
    template=prompt_template
)

# Step 2: Create faithfulness evaluator using RAGAS v0.4 API
from ragas import evaluate, EvaluationDataset, SingleTurnSample
from ragas.metrics._faithfulness import Faithfulness
from ragas.llms import LangchainLLMWrapper

from langchain_openai import OpenAIEmbeddings

llm = ChatOpenAI(model="gpt-4o-mini")

ragas_llm = LangchainLLMWrapper(llm)

faithfulness_metric = Faithfulness(llm=ragas_llm)

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
sample = SingleTurnSample(
    user_input="What are the main stages in document processing?",
    response="Document processing combines retrieval with generation.",
    retrieved_contexts=["Document processing systems combine document retrieval with text generation to provide accurate responses."]
)

dataset = EvaluationDataset(samples=[sample])

eval_result = evaluate(
    dataset=dataset,
    metrics=[faithfulness_metric],
)

faithfulness_score = eval_result.scores[0].get("faithfulness", 0.0)
print(f"Faithfulness Score: {faithfulness_score}")
print("\nChallenge completed!")
