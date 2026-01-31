"""
Hugging Face Models with LangChain

This example demonstrates how to use Hugging Face models through LangChain.
Hugging Face models can run locally, providing privacy and no API costs.
"""

import warnings
from dotenv import load_dotenv
from langchain_huggingface import HuggingFacePipeline

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)

# Load environment variables from .env file
load_dotenv()


def main():
    """Simple example: Load Hugging Face model and invoke it with a prompt."""
    
    print("\n" + "="*70)
    print("🤗 Hugging Face Model Example")
    print("="*70)
    
    # Load the model from Hugging Face
    # Note: This will download the model on first run (may take a few minutes)
    print("\n📦 Loading model (crumb/nano-mistral)...")
    print("   (This will download the model on first run - may take a few minutes)")
    model = HuggingFacePipeline.from_model_id(
        model_id="crumb/nano-mistral",
        task="text-generation",
        pipeline_kwargs={"max_new_tokens": 50}
    )
    print("✓ Model loaded successfully!\n")
    
    # Invoke with a prompt
    prompt = "Hugging Face is"
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
    print(f"\n{response}\n")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
