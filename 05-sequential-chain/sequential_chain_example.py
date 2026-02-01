"""
Sequential Chains with LangChain

This example demonstrates how to create sequential chains where the output of one chain
becomes the input to the next chain. This allows for multi-step processing of information.
"""

import os
import warnings
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)

# Load environment variables from .env file
load_dotenv()


def main():
    """Example: Create a sequential chain for concept explanation and summarization."""
    
    print("\n" + "="*70)
    print("🔗 Sequential Chain Example")
    print("="*70)
    
    # Check for API key - use OpenAI if available, otherwise use Hugging Face
    openai_api_key = os.getenv("OPENAI_API_KEY")
    use_openai = openai_api_key and openai_api_key != "your-openai-api-key-here"
    
    if not use_openai:
        print("\n⚠️  Note: Sequential chains work much better with OpenAI models.")
        print("   Hugging Face models may not follow the format as precisely.")
        print("   For best results, consider using an OpenAI API key.\n")
    
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
            pipeline_kwargs={"max_new_tokens": 100}
        )
        print("✓ Hugging Face model loaded successfully!\n")
    
    # ============================================================================
    # FIRST PROMPT TEMPLATE - Explains a concept in detail
    # ============================================================================
    #
    # This prompt takes a topic and asks for a detailed explanation
    # The variable {topic} will be filled in when we invoke the chain
    #
    explanation_prompt = PromptTemplate(
        input_variables=["topic"],
        template="Explain {topic} in detail, covering its key concepts and how it works."
    )
    
    print("-"*70)
    print("📋 First Prompt Template Created:")
    print("-"*70)
    print("  Template: 'Explain {topic} in detail, covering its key concepts and how it works.'")
    print("    → INPUT VARIABLE: {topic} - the concept to explain")
    print("    → TASK: Generate a detailed explanation\n")
    
    # ============================================================================
    # SECOND PROMPT TEMPLATE - Creates a simplified summary
    # ============================================================================
    #
    # This prompt takes the detailed explanation from the first chain and creates a simple summary
    # The variable {detailed_explanation} will be filled with the output from the first chain
    #
    summary_prompt = PromptTemplate(
        input_variables=["detailed_explanation"],
        template="Based on this explanation: {detailed_explanation}\n\nCreate a simple, beginner-friendly summary in 2-3 sentences."
    )
    
    print("-"*70)
    print("📋 Second Prompt Template Created:")
    print("-"*70)
    print("  Template: 'Based on this explanation: {detailed_explanation}\\n\\nCreate a simple, beginner-friendly summary in 2-3 sentences.'")
    print("    → INPUT VARIABLE: {detailed_explanation} - output from the first chain")
    print("    → TASK: Create a simplified summary\n")
    
    # ============================================================================
    # CREATING THE SEQUENTIAL CHAIN
    # ============================================================================
    #
    # A sequential chain connects multiple steps:
    # 1. First chain: explanation_prompt -> llm -> StrOutputParser()
    #    - Takes {topic} as input
    #    - Generates a detailed explanation
    #    - StrOutputParser() extracts the text from the response
    #
    # 2. Second chain: summary_prompt -> llm -> StrOutputParser()
    #    - Takes {detailed_explanation} (from first chain) as input
    #    - Creates a simplified summary
    #    - Generates final summary
    #
    # The pipe operator (|) connects each step
    # The dictionary {"detailed_explanation": ...} passes the output of the first chain
    #   to the {detailed_explanation} variable in the second prompt
    #
    seq_chain = (
        {"detailed_explanation": explanation_prompt | llm | StrOutputParser()}
        | summary_prompt
        | llm
        | StrOutputParser()
    )
    
    print("="*70)
    print("🔗 Sequential Chain Created:")
    print("="*70)
    print("  Step 1: explanation_prompt -> llm -> StrOutputParser()")
    print("    → Input: {topic}")
    print("    → Output: detailed explanation (text)")
    print()
    print("  Step 2: summary_prompt -> llm -> StrOutputParser()")
    print("    → Input: {detailed_explanation} (from Step 1)")
    print("    → Output: simplified summary (text)")
    print()
    print("  The dictionary {'detailed_explanation': ...} passes Step 1's output to Step 2\n")
    
    # ============================================================================
    # INVOKING THE SEQUENTIAL CHAIN
    # ============================================================================
    #
    # When we invoke the chain with {"topic": "quantum computing"}:
    # 1. The first prompt is formatted with the topic
    # 2. The LLM generates a detailed explanation
    # 3. StrOutputParser() extracts the text
    # 4. That text becomes {detailed_explanation} in the second prompt
    # 5. The second LLM generates a simplified summary
    # 6. StrOutputParser() extracts the final text
    #
    print("="*70)
    print("🔄 Executing Sequential Chain")
    print("="*70)
    
    topic = "quantum computing"
    print(f"\n📥 Input topic: '{topic}'\n")
    
    print("🔄 Invoking sequential chain...")
    print("   (This will run both chains in sequence)\n")
    
    response = seq_chain.invoke({"topic": topic})
    
    print("="*70)
    print("✨ Final Output:")
    print("="*70)
    response_text = response if isinstance(response, str) else str(response)
    print(f"\n{response_text}\n")
    print("="*70 + "\n")
    
    print("💡 Note: The first chain generated a detailed explanation,")
    print("   and the second chain created a simplified summary from it.\n")
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("="*70)
    print("📊 Summary")
    print("="*70)
    print("\nKey Concepts:")
    print("  1. Sequential chains connect multiple processing steps")
    print("  2. The output of one chain becomes input to the next")
    print("  3. StrOutputParser() extracts text from LLM responses")
    print("  4. Dictionary syntax passes data between chains")
    print("  5. The pipe operator (|) connects each step")
    print("\nSequential chains enable complex multi-step workflows!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

