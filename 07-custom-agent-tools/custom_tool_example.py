"""
Custom Tools with LangChain

This example demonstrates how to create custom tools for ReAct agents. Custom tools
allow you to extend agent capabilities with domain-specific functions.
"""

from __future__ import annotations

import os
import warnings
from dotenv import load_dotenv

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)

# Load environment variables from .env file
load_dotenv()


def main():
    """Example: Create a custom tool and use it with a ReAct agent."""
    
    print("\n" + "="*70)
    print("🔧 Custom Tools Example")
    print("="*70)
    
    # Check for API key - ReAct agents require OpenAI
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key or openai_api_key == "your-openai-api-key-here":
        print("\n❌ Error: ReAct agents with custom tools require an OpenAI API key.")
        print("   Hugging Face models do not support the bind_tools method required by ReAct agents.")
        print("   Please set OPENAI_API_KEY in your .env file.")
        print("   Get your key from: https://platform.openai.com/api-keys\n")
        return
    
    # Use OpenAI model (required for ReAct agents)
    from langchain_openai import ChatOpenAI
    print("\n📦 Loading OpenAI model (gpt-3.5-turbo)...")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    print("✓ OpenAI model loaded successfully!\n")
    
    # ============================================================================
    # CREATING A CUSTOM TOOL
    # ============================================================================
    #
    # Custom tools are functions that agents can use to perform specific actions
    # To create a custom tool:
    # 1. Define a function with a clear docstring (description)
    # 2. Use the @tool decorator to convert it to a tool
    # 3. The tool's name and description are used by the LLM to decide when to call it
    #
    # Example: Product inventory lookup tool
    #
    print("-"*70)
    print("📦 Creating Custom Tool:")
    print("-"*70)
    
    # Sample product inventory (in a real app, this would be a database)
    product_inventory = {
        "laptop-pro-15": {
            "name": "Laptop Pro 15",
            "price": 1299.99,
            "stock": 45,
            "category": "Electronics"
        },
        "wireless-mouse": {
            "name": "Wireless Mouse",
            "price": 29.99,
            "stock": 120,
            "category": "Accessories"
        },
        "usb-keyboard": {
            "name": "USB Keyboard",
            "price": 49.99,
            "stock": 78,
            "category": "Accessories"
        },
        "monitor-27": {
            "name": "27-inch Monitor",
            "price": 349.99,
            "stock": 32,
            "category": "Electronics"
        }
    }
    
    # Step 1: Define a function to look up product information
    def get_product_info(product_id: str) -> str:
        """Retrieve product information from inventory based on product ID."""
        if product_id in product_inventory:
            product = product_inventory[product_id]
            return f"Product: {product['name']}\nPrice: ${product['price']}\nStock: {product['stock']}\nCategory: {product['category']}"
        else:
            return f"Product '{product_id}' not found in inventory."
    
    print("  Step 1: Defined function 'get_product_info'")
    print("    → Function retrieves product details from inventory\n")
    
    # Step 2: Convert the function to a tool using @tool decorator
    from langchain_core.tools import tool
    
    @tool
    def get_product_info(product_id: str) -> str:
        """Retrieve product information from inventory based on product ID."""
        if product_id in product_inventory:
            product = product_inventory[product_id]
            return f"Product: {product['name']}\nPrice: ${product['price']}\nStock: {product['stock']}\nCategory: {product['category']}"
        else:
            return f"Product '{product_id}' not found in inventory."
    
    print("  Step 2: Applied @tool decorator to convert function to tool")
    print(f"    → Tool name: {get_product_info.name}")
    print(f"    → Tool description: {get_product_info.description}\n")
    
    # ============================================================================
    # TOOL ATTRIBUTES
    # ============================================================================
    #
    # Custom tools have important attributes:
    # - .name: The tool's name (used for identification)
    # - .description: Used by the LLM to decide when to call the tool
    # - .args: The tool's input arguments schema
    #
    print("-"*70)
    print("🔍 Tool Attributes:")
    print("-"*70)
    print(f"  Name: {get_product_info.name}")
    print(f"  Description: {get_product_info.description}")
    print(f"  Arguments: {get_product_info.args}\n")
    
    # ============================================================================
    # CREATING AGENT WITH CUSTOM TOOL
    # ============================================================================
    #
    # Now we can use the custom tool with a ReAct agent
    # The agent will use the tool's description to decide when to call it
    #
    from langgraph.prebuilt import create_react_agent
    
    print("-"*70)
    print("🤖 Creating ReAct Agent with Custom Tool:")
    print("-"*70)
    print("  The agent will use the tool's description to decide when to call it")
    print("  When a question involves product information, it will use our tool\n")
    
    # Create the agent with our custom tool
    agent = create_react_agent(llm, [get_product_info])
    
    print("✓ ReAct agent created with custom tool!\n")
    
    # ============================================================================
    # USING THE AGENT WITH CUSTOM TOOL
    # ============================================================================
    #
    # When we ask the agent a question, it will:
    # 1. Analyze the question
    # 2. Decide if it needs to use the tool
    # 3. Call the tool if needed
    # 4. Use the tool's output to answer
    #
    print("="*70)
    print("🔄 Using the Agent with Custom Tool")
    print("="*70)
    
    question = "What is the price and stock level of the laptop-pro-15 product?"
    print(f"\n📥 Question: '{question}'\n")
    
    print("🔄 Invoking agent...")
    print("   (The agent will decide to use the get_product_info tool)\n")
    
    # Invoke the agent with the question
    response = agent.invoke({"messages": [("human", question)]})
    
    # Extract the final answer from the response
    final_answer = response['messages'][-1].content
    
    print("="*70)
    print("✨ Agent Response:")
    print("="*70)
    print(f"\n{final_answer}\n")
    print("="*70 + "\n")
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("="*70)
    print("📊 Summary")
    print("="*70)
    print("\nKey Concepts:")
    print("  1. Custom tools are functions decorated with @tool")
    print("  2. The tool's docstring becomes its description")
    print("  3. The LLM uses the description to decide when to call the tool")
    print("  4. Tools extend agent capabilities with domain-specific functions")
    print("  5. Tools have .name, .description, and .args attributes")
    print("\nCustom tools enable you to build agents for specific use cases!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

