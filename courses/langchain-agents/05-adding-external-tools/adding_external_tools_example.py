"""
Adding External Tools to a LangGraph Chatbot

This example demonstrates how to extend a chatbot with external tools
using Wikipedia as a knowledge source. The chatbot can decide when to
query Wikipedia for verified information and when to answer directly.
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
    """Example: Adding Wikipedia as an external tool to a chatbot."""

    print("\n" + "="*70)
    print("Adding External Tools to a LangGraph Chatbot")
    print("="*70)

    # Check for API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key or openai_api_key == "your-openai-api-key-here":
        print("\nError: This example requires an OpenAI API key.")
        print("   Please set OPENAI_API_KEY in your .env file.")
        print("   Get your key from: https://platform.openai.com/api-keys\n")
        return

    from langchain_openai import ChatOpenAI
    from langchain_community.utilities import WikipediaAPIWrapper
    from langchain_community.tools import WikipediaQueryRun
    from langgraph.prebuilt import ToolNode, tools_condition

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # ========================================================================
    # PART 1: RECAP -- WHY EXTERNAL TOOLS MATTER
    # ========================================================================
    print("-"*70)
    print("Part 1: Recap -- Why External Tools Matter")
    print("-"*70)
    print("  In Module 04, we saw that LLMs can hallucinate -- generating")
    print("  confident but incorrect information. External tools solve this")
    print("  by giving the chatbot access to verified data sources.")
    print()
    print("  Our graph will change from:")
    print("      START --> chatbot --> END")
    print()
    print("  To a conditional loop:")
    print("      START --> chatbot --[tools_condition]--> tools --> chatbot --> END")
    print()
    print("  The chatbot decides when to use tools and when to answer directly.\n")

    # ========================================================================
    # PART 2: SETTING UP THE WIKIPEDIA TOOL
    # ========================================================================
    print("-"*70)
    print("Part 2: Setting Up the Wikipedia Tool")
    print("-"*70)
    print("  WikipediaAPIWrapper connects to the Wikipedia API.")
    print("  WikipediaQueryRun wraps it into a tool agents can use.\n")

    api_wrapper = WikipediaAPIWrapper(top_k_results=1)
    wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
    tools = [wikipedia_tool]

    print(f"  Tool name:        {wikipedia_tool.name}")
    print(f"  Tool description: {wikipedia_tool.description[:80]}...")
    print()
    print("  The LLM reads these properties to decide when to use the tool.\n")

    # ========================================================================
    # PART 3: BINDING TOOLS TO THE LLM
    # ========================================================================
    print("-"*70)
    print("Part 3: Binding Tools to the LLM")
    print("-"*70)
    print("  .bind_tools(tools) creates a new LLM instance that knows")
    print("  about the available tools. It does not modify the original LLM.")
    print()
    print("  The chatbot function now uses llm_with_tools instead of llm.\n")

    llm_with_tools = llm.bind_tools(tools)

    def chatbot(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    print("  LLM with tools bound successfully.")
    print("  The LLM can now choose to call Wikipedia or answer directly.\n")

    # ========================================================================
    # PART 4: BUILDING THE GRAPH WITH TOOL NODES
    # ========================================================================
    print("-"*70)
    print("Part 4: Building the Graph with Tool Nodes")
    print("-"*70)
    print("  We add two new components to the graph:")
    print("    1. ToolNode -- executes tool calls")
    print("    2. tools_condition -- routes to tools or END")
    print()
    print("  Graph structure:")
    print()
    print("      +-------+")
    print("      | START |")
    print("      +---+---+")
    print("          |")
    print("          v")
    print("      +---------+")
    print("      | chatbot |<-----+")
    print("      +----+----+      |")
    print("      tools_condition  |")
    print("      +----+-----+    |")
    print("      v          v    |")
    print("  +-------+  +-----+ |")
    print("  | tools |  | END | |")
    print("  +---+---+  +-----+ |")
    print("      +---------------+")
    print()

    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)

    tool_node = ToolNode(tools=[wikipedia_tool])
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge("tools", "chatbot")

    graph = graph_builder.compile()
    print("  Graph compiled successfully.\n")

    # ========================================================================
    # PART 5: TESTING QUERIES
    # ========================================================================
    print("-"*70)
    print("Part 5: Testing Queries")
    print("-"*70)
    print("  We will test three queries:")
    print("    1. A factual question (should trigger Wikipedia)")
    print("    2. Another factual question (should trigger Wikipedia)")
    print("    3. A simple calculation (no tool needed)\n")

    def stream_graph_updates(user_input):
        """Stream events from the graph and print agent responses."""
        for event in graph.stream({"messages": [("human", user_input)]}):
            for value in event.values():
                if value["messages"][-1].content:
                    print("  Agent:", value["messages"][-1].content)

    # Query 1: Should trigger Wikipedia
    query1 = "What is photosynthesis?"
    print(f"  Query 1: '{query1}'\n")
    stream_graph_updates(query1)
    print()

    # Query 2: Should trigger Wikipedia
    query2 = "Tell me about the Colosseum in Rome"
    print(f"  Query 2: '{query2}'\n")
    stream_graph_updates(query2)
    print()

    # Query 3: Should NOT trigger Wikipedia (simple calculation)
    query3 = "What is 15 multiplied by 7?"
    print(f"  Query 3: '{query3}'\n")
    stream_graph_updates(query3)
    print()

    print("  Notice: The first two queries likely triggered Wikipedia,")
    print("  while the multiplication question was answered directly.\n")

    # ========================================================================
    # PART 6: GRAPH VISUALISATION AND SUMMARY
    # ========================================================================
    print("-"*70)
    print("Part 6: Graph Visualisation and Summary")
    print("-"*70)
    print("  The graph now includes conditional routing.\n")

    # Mermaid text diagram
    print("  Mermaid diagram (text format):")
    mermaid_text = graph.get_graph().draw_mermaid()
    for line in mermaid_text.strip().split("\n"):
        print(f"    {line}")
    print()

    # PNG diagram
    try:
        png_data = graph.get_graph().draw_mermaid_png()
        output_path = "graph_diagram.png"
        with open(output_path, "wb") as f:
            f.write(png_data)
        print(f"  Graph diagram saved to: {output_path}")
        print("  Open the PNG file to see the conditional routing.\n")
    except Exception as e:
        print(f"  Note: Could not generate graph image: {e}")
        print("  Install grandalf with: pip install grandalf\n")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("="*70)
    print("Summary")
    print("="*70)
    print("\nKey Concepts:")
    print("  1. WikipediaAPIWrapper + WikipediaQueryRun = Wikipedia tool")
    print("  2. .bind_tools(tools) lets the LLM recognise and call tools")
    print("  3. ToolNode executes tool calls and returns results")
    print("  4. tools_condition routes to tools or END based on the response")
    print("  5. The tools --> chatbot edge creates a loop for tool results")
    print("  6. The LLM decides when to use tools vs answering directly")
    print("\nExternal tools ground your chatbot in verified data!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
