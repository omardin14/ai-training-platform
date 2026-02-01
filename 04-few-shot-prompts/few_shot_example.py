"""
Few-Shot Prompts with LangChain

This example demonstrates how to use few-shot prompts in LangChain.
Few-shot prompts provide examples to help the model understand the desired format.
"""

import os
import warnings
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)

# Load environment variables from .env file
load_dotenv()


def main():
    """Simple example: Create and use a few-shot prompt."""
    
    print("\n" + "="*70)
    print("📚 Few-Shot Prompt Example")
    print("="*70)
    
    # Check for API key - use OpenAI if available, otherwise use Hugging Face
    openai_api_key = os.getenv("OPENAI_API_KEY")
    use_openai = openai_api_key and openai_api_key != "your-openai-api-key-here"
    
    if not use_openai:
        print("\n⚠️  Note: Few-shot prompts work much better with OpenAI models.")
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
            pipeline_kwargs={"max_new_tokens": 80}
        )
        print("✓ Hugging Face model loaded successfully!\n")
    
    # ============================================================================
    # EXAMPLES - Define example input/output pairs
    # ============================================================================
    #
    # Examples show the model the pattern you want it to follow
    # Each example is a dictionary with input and output keys
    #
    examples = [
        {
            "word": "happy",
            "synonym": "joyful"
        },
        {
            "word": "sad",
            "synonym": "melancholy"
        },
        {
            "word": "angry",
            "synonym": "furious"
        }
    ]
    
    print("-"*70)
    print("📋 Examples Created:")
    print("-"*70)
    print("  These examples show the model the pattern:")
    for ex in examples:
        print(f"    {ex['word']} → {ex['synonym']}")
    print()
    
    # ============================================================================
    # EXAMPLE PROMPT - Template for formatting each example
    # ============================================================================
    #
    # This template formats each example in a consistent way
    # The variables {word} and {synonym} match the keys in the examples
    #
    example_prompt = PromptTemplate.from_template(
        "Word: {word}\nSynonym: {synonym}"
    )
    
    print("-"*70)
    print("📝 Example Prompt Template:")
    print("-"*70)
    print("  Template: 'Word: {word}\\nSynonym: {synonym}'")
    print("    → This formats each example consistently")
    print("    → Variables match the keys in examples\n")
    
    # ============================================================================
    # FEW-SHOT PROMPT TEMPLATE - Combine examples with your question
    # ============================================================================
    #
    # FewShotPromptTemplate combines:
    # - examples: The list of example dictionaries
    # - example_prompt: Template to format each example
    # - suffix: The format for your actual question
    # - input_variables: Variables that will be filled when invoking
    #
    prompt_template = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        suffix="Word: {input}",
        input_variables=["input"]
    )
    
    print("-"*70)
    print("🔗 Few-Shot Prompt Template Created:")
    print("-"*70)
    print("  examples: List of example dictionaries")
    print("  example_prompt: Template to format each example")
    print("  suffix: Format for your actual question")
    print("  input_variables: ['input'] - variable to fill in\n")
    
    # ============================================================================
    # INVOKING THE PROMPT - Use it with a model
    # ============================================================================
    #
    # The few-shot prompt can be used directly or chained with a model
    #
    print("="*70)
    print("🔄 Using the Few-Shot Prompt")
    print("="*70)
    
    # First, let's see what the formatted prompt looks like
    input_word = "excited"
    formatted_prompt = prompt_template.invoke({"input": input_word})
    
    print(f"\n📥 Input word: '{input_word}'")
    print("\n📋 Formatted Prompt (showing examples + your question):")
    print("-" * 70)
    print(formatted_prompt.text)
    print("-" * 70)
    print("\n→ Notice how the examples are shown first, then your question")
    if not use_openai:
        print("→ Note: Hugging Face models may not follow the format as precisely\n")
    else:
        print()
    
    # Create a chain and invoke with the model
    print("🔄 Invoking model with few-shot prompt...")
    chain = prompt_template | llm
    response = chain.invoke({"input": input_word})
    
    # Extract the response
    if use_openai:
        result = response.content if hasattr(response, 'content') else str(response)
        # For OpenAI, extract just the synonym part if it's in the response
        if f"Word: {input_word}" in result:
            parts = result.split(f"Word: {input_word}")
            if len(parts) > 1:
                synonym_part = parts[-1].strip()
                if "Synonym:" in synonym_part:
                    result = synonym_part.split("Synonym:")[-1].strip()
    else:
        # For Hugging Face, extract only the new synonym (after the input word)
        response_text = str(response).strip()
        # Look for the last occurrence of "Word: {input_word}" (the actual question)
        search_pattern = f"Word: {input_word}"
        # Split by the pattern and take the last part (after the actual question)
        if search_pattern in response_text:
            # Find all occurrences and use the last one (the actual question, not examples)
            parts = response_text.split(search_pattern)
            if len(parts) > 1:
                # Take the last part (after the actual question)
                after_input = parts[-1].strip()
                # Look for "Synonym:" in this part
                if "Synonym:" in after_input:
                    synonym_part = after_input.split("Synonym:")[-1].strip()
                    # Get the first word/line before any new "Word:" or newline
                    result = synonym_part.split("\n")[0].split("Word:")[0].strip()
                    # Clean up any extra whitespace or punctuation
                    result = result.split()[0] if result.split() else result
                else:
                    # If no "Synonym:" found, the model didn't follow format
                    # Try to get the first word after the input
                    first_words = after_input.split()
                    if first_words:
                        result = first_words[0].strip()
                    else:
                        result = "Unable to extract - model didn't follow format"
            else:
                result = "Unable to extract - format not recognized"
        else:
            # Model completely ignored the format
            result = "Model response doesn't match expected format"
    
    # Print the result
    print("\n" + "="*70)
    print("✨ Response:")
    print("="*70)
    if use_openai:
        print(f"\nSynonym for '{input_word}': {result}\n")
    else:
        print(f"\nSynonym for '{input_word}': {result}")
        if "Unable to extract" in result or "doesn't match" in result:
            print("\n⚠️  The Hugging Face model didn't follow the few-shot format correctly.")
            print("   This demonstrates why OpenAI models are recommended for few-shot prompts.")
        else:
            print("\n(Note: Hugging Face models may not follow the format as precisely as OpenAI)")
    print("="*70 + "\n")
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("\n" + "="*70)
    print("📊 Summary")
    print("="*70)
    print("\nKey Concepts:")
    print("  1. Examples show the model the desired pattern")
    print("  2. Example prompt formats each example consistently")
    print("  3. FewShotPromptTemplate combines examples with your question")
    print("  4. The model learns from examples and follows the pattern")
    print("\nFew-shot prompting helps models understand format and improve accuracy!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

