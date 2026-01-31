"""
Prompt Templates with LangChain

This example demonstrates how to use prompt templates in LangChain.
Prompt templates allow you to create reusable prompt structures.
"""

import os
import warnings
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)

# Load environment variables from .env file
load_dotenv()


def main():
    """Simple example: Create a prompt template and use it with a model."""
    
    print("\n" + "="*70)
    print("📝 Prompt Template Example")
    print("="*70)
    
    # Check for API key - use OpenAI if available, otherwise use Hugging Face
    openai_api_key = os.getenv("OPENAI_API_KEY")
    use_openai = openai_api_key and openai_api_key != "your-openai-api-key-here"
    
    if use_openai:
        # Use OpenAI model
        from langchain_openai import ChatOpenAI
        print("\n📦 Loading OpenAI model (gpt-3.5-turbo)...")
        model = ChatOpenAI(model="gpt-3.5-turbo")
        print("✓ OpenAI model loaded successfully!\n")
    else:
        # Use Hugging Face model
        from langchain_huggingface import HuggingFacePipeline
        print("\n📦 Loading Hugging Face model (crumb/nano-mistral)...")
        print("   (This will download the model on first run - may take a few minutes)")
        model = HuggingFacePipeline.from_model_id(
            model_id="crumb/nano-mistral",
            task="text-generation",
            pipeline_kwargs={"max_new_tokens": 50}
        )
        print("✓ Hugging Face model loaded successfully!\n")
    
    # ============================================================================
    # PROMPT TEMPLATE - Creating a reusable template with variable placeholders
    # ============================================================================
    # 
    # ChatPromptTemplate.from_messages() creates a template from a list of messages
    # Each message is a tuple with two parts:
    #   1. Role: "system", "human", or "ai" - defines who is speaking
    #   2. Content: The actual message text (can include variables in {curly_braces})
    #
    prompt_template = ChatPromptTemplate.from_messages([
        # SYSTEM MESSAGE: Instructions for the model's behavior
        # - This sets the context and tells the model how to act
        # - Usually contains instructions, guidelines, or role definitions
        ("system", "You are a helpful assistant."),
        
        # HUMAN MESSAGE: The user's input/question
        # - This is what the user wants to ask or request
        # - {topic} is a VARIABLE PLACEHOLDER that will be filled in later
        # - Variables are defined using {variable_name} syntax
        ("human", "Explain {topic} in one sentence.")
    ])
    
    print("-"*70)
    print("📋 Prompt Template Created:")
    print("-"*70)
    print("  System Message: 'You are a helpful assistant.'")
    print("    → This is an INSTRUCTION that sets the model's behavior")
    print("  Human Message: 'Explain {topic} in one sentence.'")
    print("    → This is a QUESTION with a variable placeholder")
    print("    → {topic} will be replaced with an actual value\n")
    
    # ============================================================================
    # FORMATTING THE TEMPLATE - Filling in the variable with an actual value
    # ============================================================================
    # 
    # format_messages() takes keyword arguments matching the variable names
    # It replaces {topic} with the actual value provided
    #
    print("-"*70)
    print("💬 Formatting Template with Value...")
    print("-"*70)
    
    topic = "quantum computing"  # The actual value to fill in
    formatted_messages = prompt_template.format_messages(topic=topic)
    # Result: The {topic} placeholder is replaced with "quantum computing"
    # Final prompt: "Explain quantum computing in one sentence."
    
    print(f"  Variable: topic = '{topic}'")
    print(f"  → Replaces {{topic}} in the template\n")
    
    # ============================================================================
    # MODEL FORMAT CONVERSION - Different models need different input formats
    # ============================================================================
    #
    # OpenAI models accept the message format directly (list of message objects)
    # Hugging Face models need a simple string, so we combine the messages
    #
    if use_openai:
        # OpenAI: Use the formatted messages directly (list of message objects)
        formatted_prompt = formatted_messages
    else:
        # Hugging Face: Convert messages to a single string
        # Extract the content from each message and join them
        prompt_parts = [msg.content for msg in formatted_messages]
        formatted_prompt = " ".join(prompt_parts)
    
    # ============================================================================
    # INVOKING THE MODEL - Send the formatted prompt to the model
    # ============================================================================
    #
    # The invoke() method sends the prompt to the model and returns a response
    # This is the same method used in module 01, showing LangChain's consistency
    #
    print("🔄 Invoking model...")
    response = model.invoke(formatted_prompt)
    
    # Print the result
    print("\n" + "="*70)
    print("✨ Response:")
    print("="*70)
    # Handle different response types (OpenAI returns .content, Hugging Face returns string)
    response_text = response.content if hasattr(response, 'content') else str(response)
    print(f"\n{response_text}\n")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
