"""
Agent Conversations

This example demonstrates how to maintain conversation history with agents,
ask follow-up questions, and inspect the full message exchange.
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
    """Example: Conversation history and follow-up questions with agents."""

    print("\n" + "="*70)
    print("💬 Agent Conversations")
    print("="*70)

    # Check for API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key or openai_api_key == "your-openai-api-key-here":
        print("\n❌ Error: Agents require an OpenAI API key.")
        print("   Please set OPENAI_API_KEY in your .env file.")
        print("   Get your key from: https://platform.openai.com/api-keys\n")
        return

    from langchain_openai import ChatOpenAI
    from langchain_core.tools import tool
    from langchain_core.messages import HumanMessage, AIMessage
    from langchain.agents import create_agent

    print("\n📦 Loading OpenAI model (gpt-4o-mini)...")
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    print("✓ OpenAI model loaded successfully!\n")

    # ========================================================================
    # SETUP: Define a tool for the agent
    # ========================================================================

    @tool
    def circle_area(radius: float) -> float:
        """Calculates the area of a circle given its radius."""
        import math
        return round(math.pi * radius ** 2, 2)

    tools = [circle_area]
    app = create_agent(model, tools)

    # ========================================================================
    # PART 1: SINGLE QUERY WITH INPUT/OUTPUT LOGGING
    # ========================================================================
    #
    # It's useful to print both the user's query and the agent's response
    # to verify the agent is working correctly. We label them "user_input"
    # and "agent_output" for clarity.
    #
    print("-"*70)
    print("📝 Part 1: Single Query with Input/Output Logging")
    print("-"*70)
    print("  Printing both user_input and agent_output helps verify")
    print("  that the agent is responding correctly.\n")

    query = "What is the area of a circle with radius 7?"
    response = app.invoke({"messages": [("human", query)]})

    # Print both input and output for debugging
    print({"user_input": query,
           "agent_output": response['messages'][-1].content})
    print()

    # ========================================================================
    # PART 2: FOLLOW-UP QUESTIONS WITH CONVERSATION HISTORY
    # ========================================================================
    #
    # To ask follow-up questions, we pass the full message history along
    # with the new query. The agent sees the entire conversation and can
    # answer questions that reference earlier context.
    #
    # While answering, LangChain updates the whole conversation, so we can
    # inspect all messages exchanged so far.
    #
    print("-"*70)
    print("💬 Part 2: Follow-Up Questions with Conversation History")
    print("-"*70)
    print("  We pass message_history + the new query so the agent")
    print("  remembers what was discussed before.\n")

    # Save the message history from the first response
    message_history = response["messages"]

    # Ask a follow-up question without repeating context
    new_query = "What about one with radius 3?"
    print(f"  📥 Follow-up query: '{new_query}'")
    print("     (The agent remembers we were talking about circles)\n")

    # Invoke the agent with the full message history + new query
    response = app.invoke({"messages": message_history + [("human", new_query)]})

    print("="*70)
    print("  ✨ Agent Response:")
    print("="*70)
    print(f"\n  {response['messages'][-1].content}\n")
    print("="*70 + "\n")

    # ========================================================================
    # PART 3: INSPECTING THE FULL CONVERSATION
    # ========================================================================
    #
    # We import HumanMessage and AIMessage from langchain_core.messages.
    # These classes represent our queries and the agent's answers.
    #
    # We filter the response messages to extract only HumanMessage and
    # AIMessage instances that contain actual content (using .strip() to
    # remove trailing whitespace). Then we label each message with its
    # class name for a clean conversation log.
    #
    print("-"*70)
    print("📋 Part 3: Inspecting the Full Conversation")
    print("-"*70)
    print("  HumanMessage = our queries")
    print("  AIMessage    = the agent's answers\n")

    # Filter out only human and AI messages with actual content
    filtered_messages = [msg for msg in response["messages"]
                         if isinstance(msg, (HumanMessage, AIMessage))
                         and msg.content.strip()]

    # Format and print the conversation log
    result = {
        "user_input": new_query,
        "agent_output": [
            f"{msg.__class__.__name__}: {msg.content}"
            for msg in filtered_messages
        ]
    }

    print("  Full conversation log:")
    print("  " + "-"*40)
    for entry in result["agent_output"]:
        print(f"  {entry}")
    print("  " + "-"*40)
    print()

    # ========================================================================
    # PART 4: CONTINUING THE CONVERSATION
    # ========================================================================
    print("-"*70)
    print("🔄 Part 4: Continuing the Conversation")
    print("-"*70)
    print("  Each response carries the full history, so we can keep going.\n")

    message_history = response["messages"]
    third_query = "And radius 10?"

    print(f"  📥 Third query: '{third_query}'\n")

    response = app.invoke({"messages": message_history + [("human", third_query)]})

    # Show the latest answer
    print("="*70)
    print("  ✨ Agent Response:")
    print("="*70)
    print(f"\n  {response['messages'][-1].content}\n")
    print("="*70 + "\n")

    # Show the full conversation so far
    filtered = [msg for msg in response["messages"]
                if isinstance(msg, (HumanMessage, AIMessage))
                and msg.content.strip()]

    print("  Complete conversation history:")
    print("  " + "-"*40)
    for msg in filtered:
        label = "You" if isinstance(msg, HumanMessage) else "Agent"
        print(f"  {label}: {msg.content}")
    print("  " + "-"*40)
    print()

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("="*70)
    print("📊 Summary")
    print("="*70)
    print("\nKey Concepts:")
    print("  1. Print user_input and agent_output to verify agent behaviour")
    print("  2. Pass message_history + new query for follow-up questions")
    print("  3. HumanMessage and AIMessage represent the conversation")
    print("  4. Filter messages with isinstance() to get a clean log")
    print("  5. Each response carries the full history for continuation")
    print("\nConversation history is essential for building chatbot agents!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
