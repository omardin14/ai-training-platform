"""
ReAct Agents with LangChain

This example demonstrates how to create ReAct (Reasoning + Acting) agents that can
use tools to answer questions. ReAct agents can reason about what to do and take
actions using available tools.
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
    """Example: Create a ReAct agent that uses tools to answer questions."""
    
    print("\n" + "="*70)
    print("🤖 ReAct Agent Example")
    print("="*70)
    
    # Check for API key - ReAct agents require OpenAI
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key or openai_api_key == "your-openai-api-key-here":
        print("\n❌ Error: ReAct agents require an OpenAI API key.")
        print("   Please set OPENAI_API_KEY in your .env file.")
        print("   Get your key from: https://platform.openai.com/api-keys\n")
        return
    
    # Use OpenAI model (required for ReAct agents)
    from langchain_openai import ChatOpenAI
    print("\n📦 Loading OpenAI model (gpt-3.5-turbo)...")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    print("✓ OpenAI model loaded successfully!\n")
    
    # ============================================================================
    # LOADING TOOLS - Tools the agent can use
    # ============================================================================
    #
    # Tools are functions the agent can call to perform actions
    # Here we load the calculator tool which can perform mathematical calculations
    # The agent will decide when to use this tool based on the question
    #
    from langchain_community.agent_toolkits.load_tools import load_tools
    
    print("-"*70)
    print("🔧 Loading Tools:")
    print("-"*70)
    print("  Loading calculator tool...")
    tools = load_tools(["llm-math"], llm=llm)
    print(f"✓ Loaded {len(tools)} tool(s)")
    print("    → Calculator: Performs mathematical calculations\n")
    
    # ============================================================================
    # CREATING THE REACT AGENT
    # ============================================================================
    #
    # A ReAct agent combines:
    # - Reasoning: The agent thinks about what to do
    # - Acting: The agent uses tools to perform actions
    #
    # We use langgraph.prebuilt.create_react_agent to create the agent
    #
    from langgraph.prebuilt import create_react_agent
    
    print("-"*70)
    print("🤖 Creating ReAct Agent:")
    print("-"*70)
    print("  ReAct = Reasoning + Acting")
    print("    → Reasoning: Agent thinks about what to do")
    print("    → Acting: Agent uses tools to perform actions")
    print("    → The agent decides when to use tools automatically\n")
    
    # Create the ReAct agent
    agent = create_react_agent(llm, tools)
    
    print("✓ ReAct agent created successfully!\n")
    
    # ============================================================================
    # INVOKING THE AGENT
    # ============================================================================
    #
    # When we invoke the agent:
    # 1. The agent receives the question
    # 2. It reasons about whether it needs a tool
    # 3. If needed, it calls the calculator tool
    # 4. It uses the tool's output to formulate an answer
    # 5. Returns the final answer
    #
    print("="*70)
    print("🔄 Using the ReAct Agent")
    print("="*70)
    
    question = "What is 15 multiplied by 23, then add 100 to the result?"
    print(f"\n📥 Question: '{question}'\n")
    
    print("🔄 Invoking agent...")
    print("   (The agent will decide to use the calculator tool)\n")
    
    # Invoke the agent with the question
    # The format is a list of messages, with the human message containing the question
    response = agent.invoke({"messages": [("human", question)]})
    
    # Extract the final answer from the response
    # The last message contains the agent's final response
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
    print("  1. ReAct agents combine reasoning and acting")
    print("  2. Agents can use tools to perform actions")
    print("  3. The agent decides when to use tools automatically")
    print("  4. Tools extend the agent's capabilities beyond just text generation")
    print("  5. The agent uses the tool output to answer questions")
    print("\nReAct agents enable intelligent tool use for complex tasks!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
