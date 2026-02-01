"""
Prompt Chains with LangChain

This example demonstrates how to chain a prompt template with a model using the pipe operator (|).
The pipe operator connects the prompt template to the LLM, creating a chain that can be invoked.
"""

import os
import warnings
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)

# Load environment variables from .env file
load_dotenv()


def main():
    """Simple example: Chain a prompt template with a model."""
    
    print("\n" + "="*70)
    print("🔗 Prompt Chain Example")
    print("="*70)
    
    # Check for API key - use OpenAI if available, otherwise use Hugging Face
    openai_api_key = os.getenv("OPENAI_API_KEY")
    use_openai = openai_api_key and openai_api_key != "your-openai-api-key-here"
    
    if use_openai:
        # Use OpenAI model
        from langchain_openai import ChatOpenAI
        print("\n📦 Loading OpenAI model (gpt-3.5-turbo)...")
        llm = ChatOpenAI(model="gpt-3.5-turbo")
        print("✓ OpenAI model loaded successfully!\n")
    else:
        # Use Hugging Face model
        from langchain_huggingface import HuggingFacePipeline
        print("\n📦 Loading Hugging Face model (crumb/nano-mistral)...")
        print("   (This will download the model on first run - may take a few minutes)")
        llm = HuggingFacePipeline.from_model_id(
            model_id="crumb/nano-mistral",
            task="text-generation",
            pipeline_kwargs={"max_new_tokens": 80}
        )
        print("✓ Hugging Face model loaded successfully!\n")
    
    # ============================================================================
    # PROMPT TEMPLATE - Create a template with a variable placeholder
    # ============================================================================
    #
    # PromptTemplate.from_template() creates a template from a string
    # The string can contain variables in {curly_braces}
    #
    template = "You are a helpful AI assistant. Answer the question: {question}"
    prompt = PromptTemplate.from_template(template=template)
    
    print("-"*70)
    print("📋 Prompt Template")
    print("-"*70)
    print(f"  Template: '{template}'")
    print("    → INSTRUCTION: Sets the assistant's role")
    print("    → VARIABLE: {question} will be filled in")
    print("    → TASK: Answer a question\n")
    
    # ============================================================================
    # CREATING THE CHAIN - Using the pipe operator (|)
    # ============================================================================
    #
    # The pipe operator (|) chains the prompt template with the LLM
    # This creates a chain: prompt | llm
    # When invoked, it will: format the prompt → send to LLM → return response
    #
    llm_chain = prompt | llm
    
    print("-"*70)
    print("🔗 Creating Chain with Pipe Operator")
    print("-"*70)
    print("  Code: llm_chain = prompt | llm")
    print("    → This chains the prompt template with the model")
    print("    → The pipe operator (|) connects them together")
    print("    → The chain can now be invoked with .invoke()\n")
    
    # ============================================================================
    # INVOKING THE CHAIN - Call the chain with a question
    # ============================================================================
    #
    # The invoke() method takes a dictionary with the variable values
    # The chain will: format the template → send to LLM → return response
    #
    print("="*70)
    print("🔄 Invoking the Chain")
    print("="*70)
    
    question = "How does LangChain make LLM application development easier?"
    print(f"\n📥 Input: question = '{question}'\n")
    
    print("🔄 Invoking chain...")
    response = llm_chain.invoke({"question": question})
    
    # Extract the response content
    if use_openai:
        response_text = response.content if hasattr(response, 'content') else str(response)
    else:
        response_text = str(response).strip()
    
    # Print the result
    print("\n" + "="*70)
    print("✨ Response:")
    print("="*70)
    print(f"\n{response_text}\n")
    print("="*70 + "\n")
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("\n" + "="*70)
    print("📊 Summary")
    print("="*70)
    print("\nKey Concepts:")
    print("  1. Create a prompt template with PromptTemplate.from_template()")
    print("  2. Chain it with a model using the pipe operator: prompt | llm")
    print("  3. Invoke the chain with .invoke() and a dictionary of variables")
    print("\nThe pipe operator (|) is a clean way to connect LangChain components!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
