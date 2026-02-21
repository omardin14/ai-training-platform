"""
ReAct Agents & Custom Tools

This example demonstrates ReAct (Reasoning + Action) agents and how to build
custom tools that extend agent capabilities with domain-specific functions.
"""

from __future__ import annotations

import os
import warnings
from dotenv import load_dotenv

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*LangGraphDeprecated.*")

# Load environment variables from .env file
load_dotenv()


def main():
    """Example: ReAct agents with built-in and custom tools."""

    print("\n" + "="*70)
    print("🤖 ReAct Agents & Custom Tools")
    print("="*70)

    # Check for API key - ReAct agents require OpenAI
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key or openai_api_key == "your-openai-api-key-here":
        print("\n❌ Error: ReAct agents require an OpenAI API key.")
        print("   Hugging Face models do not support the bind_tools method")
        print("   required by ReAct agents.")
        print("   Please set OPENAI_API_KEY in your .env file.")
        print("   Get your key from: https://platform.openai.com/api-keys\n")
        return

    # Use OpenAI model (required for ReAct agents)
    from langchain_openai import ChatOpenAI
    print("\n📦 Loading OpenAI model (gpt-4o-mini)...")
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    print("✓ OpenAI model loaded successfully!\n")

    # ========================================================================
    # PART 1: BASIC ReAct AGENT
    # ========================================================================
    #
    # ReAct stands for "Reasoning" and "Action".
    # Agents can reason about what they need and then act by calling tools.
    # For instance, an agent could reason that it needs a math tool, call it,
    # and return the answer to the user.
    #
    print("-"*70)
    print("🧠 Part 1: Basic ReAct Agent")
    print("-"*70)
    print("  ReAct agents can reason about a question and decide which")
    print("  tools to call in order to answer it.\n")

    import math
    from langchain_core.tools import tool
    from langchain.agents import create_agent

    # Define a simple math tool
    @tool
    def square_root(value: str) -> float:
        """Calculate the square root of a number."""
        return math.sqrt(float(value))

    # Create the ReAct agent with the tool
    agent = create_agent(model, [square_root])

    # Invoke the agent with a natural language query
    query = "What is the square root of 256?"
    print(f"  📥 Query: '{query}'\n")
    print("  🔄 Agent reasoning...")
    print("     → Sees the question involves a square root")
    print("     → Decides to call the square_root tool")
    print("     → Uses the result to answer\n")

    response = agent.invoke({"messages": [("human", query)]})
    answer = response['messages'][-1].content

    print("="*70)
    print("  ✨ Agent Response:")
    print("="*70)
    print(f"\n  {answer}\n")
    print("="*70 + "\n")

    # ========================================================================
    # PART 2: BUILDING A CUSTOM TOOL
    # ========================================================================
    #
    # Custom tools let you give agents access to your own data and logic.
    # Steps to build a custom tool:
    # 1. Use the @tool decorator from langchain_core.tools
    # 2. Define a function that accepts a string input
    # 3. Include a docstring describing what the tool does
    # 4. Parse the input, perform the calculation, and return the result
    #
    print("-"*70)
    print("🔧 Part 2: Building a Custom Tool")
    print("-"*70)
    print("  Custom tools extend agent capabilities with your own functions.")
    print("  The @tool decorator tells LangChain to treat a function as a tool.\n")

    # Sample recipe database (in a real app, this could be a database or API)
    recipe_catalog = {
        "tomato-soup": {
            "name": "Tomato Soup",
            "prep_time": "15 min",
            "cook_time": "30 min",
            "servings": 4,
            "difficulty": "Easy",
        },
        "grilled-salmon": {
            "name": "Grilled Salmon",
            "prep_time": "10 min",
            "cook_time": "20 min",
            "servings": 2,
            "difficulty": "Medium",
        },
        "pasta-carbonara": {
            "name": "Pasta Carbonara",
            "prep_time": "10 min",
            "cook_time": "15 min",
            "servings": 3,
            "difficulty": "Medium",
        },
    }

    @tool
    def triangle_area(base: float, height: float) -> float:
        """Calculates the area of a triangle given the base and height."""
        return 0.5 * base * height

    print("  Step 1: Defined function 'triangle_area'")
    print("    → Accepts base and height as typed parameters")
    print("    → The LLM extracts values from the query automatically\n")

    print("  Step 2: Applied @tool decorator")
    print(f"    → Tool name: {triangle_area.name}")
    print(f"    → Tool description: {triangle_area.description}\n")

    # ========================================================================
    # TOOL ATTRIBUTES
    # ========================================================================
    print("-"*70)
    print("🔍 Tool Attributes:")
    print("-"*70)
    print(f"  Name:        {triangle_area.name}")
    print(f"  Description: {triangle_area.description}")
    print(f"  Arguments:   {triangle_area.args}\n")

    # ========================================================================
    # PART 3: USING THE CUSTOM TOOL WITH AN AGENT
    # ========================================================================
    #
    # Pass the custom tool to a ReAct agent. The agent reads the tool's
    # description and decides when to call it based on the user's question.
    # LangChain also has a large library of pre-built tools for tasks like
    # database querying, web scraping, and image generation.
    #
    print("-"*70)
    print("🤖 Part 3: Using the Custom Tool with an Agent")
    print("-"*70)

    tools = [triangle_area]
    app = create_agent(model, tools)

    query = "What is the area of a triangle with base 12 and height 8?"
    print(f"\n  📥 Query: '{query}'\n")
    print("  🔄 Agent reasoning...")
    print("     → Sees the question is about triangle area")
    print("     → Matches it to the triangle_area tool")
    print("     → Calls the tool with base=12, height=8")
    print("     → Uses the result to answer\n")

    response = app.invoke({"messages": [("human", query)]})
    final_answer = response['messages'][-1].content

    print("="*70)
    print("  ✨ Agent Response:")
    print("="*70)
    print(f"\n  {final_answer}\n")
    print("="*70 + "\n")

    # ========================================================================
    # PART 4: MULTIPLE CUSTOM TOOLS
    # ========================================================================
    print("-"*70)
    print("📚 Part 4: Multiple Custom Tools")
    print("-"*70)
    print("  Agents can use multiple tools. Pass them all in a list and the")
    print("  agent decides which one to call based on the question.\n")

    @tool
    def get_recipe(recipe_id: str) -> str:
        """Look up a recipe from the catalog by its ID."""
        if recipe_id in recipe_catalog:
            r = recipe_catalog[recipe_id]
            return (
                f"Recipe: {r['name']}\n"
                f"Prep: {r['prep_time']} | Cook: {r['cook_time']}\n"
                f"Servings: {r['servings']} | Difficulty: {r['difficulty']}"
            )
        return f"Recipe '{recipe_id}' not found in catalog."

    # Agent with both tools
    multi_agent = create_agent(model, [triangle_area, get_recipe])

    query = "Can you find me the recipe for pasta-carbonara?"
    print(f"  📥 Query: '{query}'\n")

    response = multi_agent.invoke({"messages": [("human", query)]})
    print("="*70)
    print("  ✨ Agent Response:")
    print("="*70)
    print(f"\n  {response['messages'][-1].content}\n")
    print("="*70 + "\n")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("="*70)
    print("📊 Summary")
    print("="*70)
    print("\nKey Concepts:")
    print("  1. ReAct agents reason about questions and act by calling tools")
    print("  2. The @tool decorator converts functions into agent tools")
    print("  3. The tool's docstring tells the LLM when to use it")
    print("  4. Tools have .name, .description, and .args attributes")
    print("  5. Agents can use multiple tools and pick the right one")
    print("\nCustom tools let you build agents tailored to any domain!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
