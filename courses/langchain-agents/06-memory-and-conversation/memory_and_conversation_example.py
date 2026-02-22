"""
Memory & Conversation

This example demonstrates how to add memory to a LangGraph chatbot
so it can maintain conversation context across multiple turns.
We build on the Wikipedia tool integration from Module 05 and add
MemorySaver checkpointing for persistent conversation history.
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
    """Example: Adding memory and conversation to a chatbot with tools."""

    print("\n" + "="*70)
    print("Memory & Conversation")
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
    from langgraph.checkpoint.memory import MemorySaver

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # ========================================================================
    # PART 1: RECAP -- BUILDING THE GRAPH WITH TOOLS
    # ========================================================================
    print("-"*70)
    print("Part 1: Recap -- Building the Graph with Tools")
    print("-"*70)
    print("  We start with the same graph from Module 05:")
    print("  - Wikipedia tool for factual lookups")
    print("  - ToolNode for executing tool calls")
    print("  - tools_condition for conditional routing\n")

    # Set up the Wikipedia tool
    api_wrapper = WikipediaAPIWrapper(top_k_results=1)
    wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
    tools = [wikipedia_tool]

    # Bind tools to the LLM
    llm_with_tools = llm.bind_tools(tools)

    def chatbot(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    # Build the graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)

    tool_node = ToolNode(tools=[wikipedia_tool])
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge("tools", "chatbot")

    # Compile WITHOUT memory first
    graph = graph_builder.compile()
    print("  Graph compiled successfully (without memory).\n")

    # ========================================================================
    # PART 2: VERIFYING TOOL RESPONSES
    # ========================================================================
    print("-"*70)
    print("Part 2: Verifying Tool Responses")
    print("-"*70)
    print("  We use stream_tool_responses() to print the full message")
    print("  objects, revealing tool call metadata and Wikipedia results.\n")

    def stream_tool_responses(user_input: str):
        """Stream events showing tool calls and responses."""
        for event in graph.stream({"messages": [("human", user_input)]}):
            for value in event.values():
                print("  Agent:", value["messages"])

    query = "Tell me about the Northern Lights"
    print(f"  Query: '{query}'\n")
    stream_tool_responses(query)
    print()
    print("  The output shows the tool call metadata (name, query)")
    print("  followed by the Wikipedia content and the final answer.\n")

    # Visualise the graph
    print("  Mermaid diagram (text format):")
    mermaid_text = graph.get_graph().draw_mermaid()
    for line in mermaid_text.strip().split("\n"):
        print(f"    {line}")
    print()

    # ========================================================================
    # PART 3: SETTING UP MEMORYSAVER
    # ========================================================================
    print("-"*70)
    print("Part 3: Setting Up MemorySaver")
    print("-"*70)
    print("  MemorySaver stores conversation state as in-memory checkpoints.")
    print("  We pass it to .compile() using the checkpointer parameter.\n")

    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)

    print("  memory = MemorySaver()")
    print("  graph = graph_builder.compile(checkpointer=memory)")
    print()
    print("  The graph now saves its state after each step,")
    print("  allowing the chatbot to remember previous messages.\n")

    # ========================================================================
    # PART 4: STREAMING WITH MEMORY
    # ========================================================================
    print("-"*70)
    print("Part 4: Streaming with Memory")
    print("-"*70)
    print("  With memory enabled, we pass a config dictionary containing")
    print("  a thread_id to identify the conversation session.\n")

    def stream_memory_responses(user_input: str):
        """Stream events with memory, showing content responses."""
        config = {"configurable": {"thread_id": "single_session_memory"}}
        for event in graph.stream({"messages": [("human", user_input)]}, config):
            for value in event.values():
                if "messages" in value and value["messages"]:
                    print("  Agent:", value["messages"][-1].content)

    print("  Key differences from previous streaming:")
    print("    - config dict with thread_id identifies the session")
    print("    - config passed as second argument to .stream()")
    print("    - Guard check: if 'messages' in value\n")

    # ========================================================================
    # PART 5: TESTING CONVERSATION MEMORY
    # ========================================================================
    print("-"*70)
    print("Part 5: Testing Conversation Memory")
    print("-"*70)
    print("  We send two queries with the same thread_id.")
    print("  The follow-up should use context from the first query.\n")

    query1 = "What is the Panama Canal?"
    print(f"  Query 1: '{query1}'\n")
    stream_memory_responses(query1)
    print()

    query2 = "When was it completed?"
    print(f"  Query 2 (follow-up): '{query2}'\n")
    stream_memory_responses(query2)
    print()

    print("  The chatbot correctly understood that 'it' refers to the")
    print("  Panama Canal because it has access to the conversation history.\n")

    # ========================================================================
    # PART 6: GRAPH VISUALISATION AND SUMMARY
    # ========================================================================
    print("-"*70)
    print("Part 6: Graph Visualisation and Summary")
    print("-"*70)

    # PNG diagram
    try:
        png_data = graph.get_graph().draw_mermaid_png()
        output_path = "graph_diagram.png"
        with open(output_path, "wb") as f:
            f.write(png_data)
        print(f"  Graph diagram saved to: {output_path}")
        print("  The graph structure is the same as Module 05,")
        print("  but now with memory checkpointing enabled.\n")
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
    print("  1. MemorySaver stores conversation state as checkpoints")
    print("  2. checkpointer=memory in .compile() enables memory")
    print("  3. thread_id in config identifies a conversation session")
    print("  4. config is passed as the second argument to .stream()")
    print("  5. Guard check ensures safe message access with checkpointing")
    print("  6. Different thread_id values create independent conversations")
    print("\nMemory turns your chatbot into a true conversational agent!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
