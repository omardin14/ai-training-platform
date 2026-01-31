"""
OpenAI Models with LangChain

This example demonstrates how to use OpenAI's GPT models through LangChain.
OpenAI models are accessed via API and require an API key.
"""

import os
import warnings
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)


def main():
    """Simple example: Load OpenAI model and invoke it with a prompt."""
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ Error: OPENAI_API_KEY not found.")
        print("Set it in a .env file or as an environment variable:")
        print("  export OPENAI_API_KEY='your-api-key-here'\n")
        return
    
    print("\n" + "="*70)
    print("🤖 OpenAI Model Example")
    print("="*70)
    
    # Load the model
    print("\n📦 Loading model (gpt-3.5-turbo)...")
    model = ChatOpenAI(model="gpt-3.5-turbo")
    print("✓ Model loaded successfully!\n")
    
    # Invoke with a prompt
    prompt = "What is LangChain in one sentence?"
    print("-"*70)
    print("💬 Prompt:")
    print(f"   {prompt}")
    print("-"*70)
    
    print("\n🔄 Invoking model...")
    response = model.invoke(prompt)
    
    # Print the result
    print("\n" + "="*70)
    print("✨ Response:")
    print("="*70)
    print(f"\n{response.content}\n")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
