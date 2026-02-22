"""
Building Graphs with LangGraph

This example demonstrates how to create a custom chatbot using LangGraph's
StateGraph. We define nodes, edges, and an agent state to build a
conversational workflow.
"""

import os
import warnings
from typing import Annotated

from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*LangGraphDeprecated.*")

# Load environment variables from .env file
load_dotenv()


# State must be defined at module level so get_type_hints() can resolve it.
class State(TypedDict):
    messages: Annotated[list, add_messages]


def main():
    """Example: Build a chatbot using LangGraph's StateGraph."""

    print("\n" + "="*70)
    print("📊 Building Graphs with LangGraph")
    print("="*70)

    # Check for API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key or openai_api_key == "your-openai-api-key-here":
        print("\n❌ Error: This example requires an OpenAI API key.")
        print("   Please set OPENAI_API_KEY in your .env file.")
        print("   Get your key from: https://platform.openai.com/api-keys\n")
        return

    # ========================================================================
    # PART 1: UNDERSTANDING GRAPH CONCEPTS
    # ========================================================================
    print("-"*70)
    print("🧠 Part 1: Understanding Graph Concepts")
    print("-"*70)
    print("  In LangGraph, a graph organises the agent's workflow:")
    print()
    print("  • Nodes  = functions (generate a response, call a tool, etc.)")
    print("  • Edges  = connections between nodes")
    print("  • State  = tracks progress through the workflow")
    print()
    print("  A simple chatbot graph looks like this:")
    print()
    print("      ┌───────┐      ┌─────────┐      ┌─────┐")
    print("      │ START │ ───▶ │ chatbot │ ───▶ │ END │")
    print("      └───────┘      └─────────┘      └─────┘")
    print()
    print("  START sends the user's message to the chatbot node,")
    print("  which generates a response and passes it to END.\n")

    # ========================================================================
    # PART 2: SETTING UP IMPORTS AND THE LLM
    # ========================================================================
    print("-"*70)
    print("📦 Part 2: Setting Up Imports and the LLM")
    print("-"*70)

    from langchain_openai import ChatOpenAI

    print("  Imported:")
    print("    • Annotated, TypedDict  — structure the chatbot's text data")
    print("    • StateGraph, START, END — set up the workflow")
    print("    • add_messages           — append messages with metadata")
    print("    • ChatOpenAI             — the LLM provider\n")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    print("  ✓ OpenAI model (gpt-4o-mini) loaded\n")

    # ========================================================================
    # PART 3: DEFINING THE STATE
    # ========================================================================
    #
    # The graph state tracks the agent's progress. It stores all text
    # interactions as a list of messages. The Annotated type combined with
    # add_messages ensures new messages are appended with metadata rather
    # than replacing the list.
    #
    print("-"*70)
    print("📝 Part 3: Defining the State")
    print("-"*70)

    print("  Created State class with TypedDict:")
    print("    • messages: Annotated[list, add_messages]")
    print("    • Annotated + add_messages ensures new messages are appended")
    print("    • This list stores every interaction with the chatbot\n")

    # ========================================================================
    # PART 4: BUILDING THE GRAPH
    # ========================================================================
    #
    # Steps:
    # 1. Initialise a StateGraph with our State structure
    # 2. Define a chatbot function node
    # 3. Add the node to the graph builder
    # 4. Connect START → chatbot → END with edges
    # 5. Compile the graph into a runnable application
    #
    print("-"*70)
    print("🔨 Part 4: Building the Graph")
    print("-"*70)

    # Step 1: Initialise the graph builder
    graph_builder = StateGraph(State)
    print("  Step 1: Initialised StateGraph(State)")

    # Step 2: Define the chatbot function node
    def chatbot(state: State):
        return {"messages": [llm.invoke(state["messages"])]}

    print("  Step 2: Defined chatbot(state) function")
    print("    → Uses llm.invoke(state['messages']) to generate a response")

    # Step 3: Add the node to the graph
    graph_builder.add_node("chatbot", chatbot)
    print("  Step 3: Added 'chatbot' node to graph_builder")

    # Step 4: Connect the edges
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    print("  Step 4: Connected START → chatbot → END")

    # Step 5: Compile the graph
    graph = graph_builder.compile()
    print("  Step 5: Compiled the graph into a runnable app")
    print()
    print("  Final graph structure:")
    print()
    print("      ┌───────┐      ┌─────────┐      ┌─────┐")
    print("      │ START │ ───▶ │ chatbot │ ───▶ │ END │")
    print("      └───────┘      └─────────┘      └─────┘")
    print()

    # ========================================================================
    # PART 5: USING THE GRAPH
    # ========================================================================
    print("-"*70)
    print("🤖 Part 5: Using the Graph")
    print("-"*70)
    print("  Now we can invoke the compiled graph just like any agent.\n")

    question = "What are the four largest moons of Jupiter?"
    print(f"  📥 Query: '{question}'\n")

    response = graph.invoke({"messages": [("human", question)]})
    answer = response["messages"][-1].content

    print("="*70)
    print("  ✨ Chatbot Response:")
    print("="*70)
    print(f"\n  {answer}\n")
    print("="*70 + "\n")

    # ========================================================================
    # PART 6: MULTI-TURN CONVERSATION
    # ========================================================================
    print("-"*70)
    print("💬 Part 6: Multi-Turn Conversation")
    print("-"*70)
    print("  The graph supports conversation history, just like agents.\n")

    message_history = response["messages"]
    follow_up = "Which of those is the largest?"
    print(f"  📥 Follow-up: '{follow_up}'\n")

    response = graph.invoke({
        "messages": message_history + [("human", follow_up)]
    })
    answer = response["messages"][-1].content

    print("="*70)
    print("  ✨ Chatbot Response:")
    print("="*70)
    print(f"\n  {answer}\n")
    print("="*70 + "\n")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("="*70)
    print("📊 Summary")
    print("="*70)
    print("\nKey Concepts:")
    print("  1. StateGraph organises the agent's workflow as a graph")
    print("  2. Nodes are functions (e.g. chatbot) that process state")
    print("  3. Edges connect nodes (START → chatbot → END)")
    print("  4. State tracks messages using Annotated[list, add_messages]")
    print("  5. .compile() turns the graph into a runnable application")
    print("  6. The compiled graph supports conversation history")
    print("\nLangGraph gives you full control over your agent's workflow!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
