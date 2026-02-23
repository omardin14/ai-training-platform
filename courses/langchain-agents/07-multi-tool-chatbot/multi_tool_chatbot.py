"""
Multi-Tool Chatbot

This example demonstrates how to build a chatbot with multiple custom tools
and a structured workflow. We combine an LLM-powered tool, a pure Python
tool, and the Wikipedia tool into a single chatbot with MessagesState,
a should_continue router, and a call_model dynamic dispatcher.
"""

import os
import warnings

from dotenv import load_dotenv
from langgraph.graph import StateGraph, MessagesState, START, END

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*LangGraphDeprecated.*")

# Load environment variables from .env file
load_dotenv()


def main():
    """Example: Multi-Tool Chatbot."""

    print("\n" + "=" * 70)
    print("Multi-Tool Chatbot")
    print("=" * 70)

    # Check for API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key or openai_api_key == "your-openai-api-key-here":
        print("\nError: This example requires an OpenAI API key.")
        print("   Please set OPENAI_API_KEY in your .env file.")
        print("   Get your key from: https://platform.openai.com/api-keys\n")
        return

    from langchain_openai import ChatOpenAI
    from langchain_core.tools import tool
    from langchain_core.messages import AIMessage, HumanMessage
    from langchain_community.tools import WikipediaQueryRun
    from langchain_community.utilities import WikipediaAPIWrapper
    from langgraph.prebuilt import ToolNode
    from langgraph.checkpoint.memory import MemorySaver

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # ========================================================================
    # PART 1: Why Multiple Tools?
    # ========================================================================
    print("-" * 70)
    print("Part 1: Why Multiple Tools?")
    print("-" * 70)
    print("  In previous modules we built chatbots with a single external tool")
    print("  (Wikipedia). Now we'll create a chatbot that has THREE tools and")
    print("  lets the LLM decide which one to use for each query.\n")
    print("  Our tools:")
    print("    1. concept_lookup  — LLM-powered (explains technical concepts)")
    print("    2. char_counter    — Pure Python (counts characters and words)")
    print("    3. wikipedia_tool  — External API (factual lookups)\n")

    # ========================================================================
    # PART 2: Building Custom Tools
    # ========================================================================
    print("-" * 70)
    print("Part 2: Building Custom Tools")
    print("-" * 70)
    print("  The @tool decorator labels a function as a LangChain tool.")
    print("  The LLM reads the function name, type hints, and docstring")
    print("  to decide when to call it.\n")

    @tool
    def concept_lookup(topic: str) -> str:
        """Look up and explain a technical concept in simple terms."""
        try:
            answer = llm.invoke(
                f"Explain the concept of {topic} in 2-3 simple sentences."
            )
            return answer.content
        except Exception as e:
            return f"Error looking up concept: {str(e)}"

    @tool
    def char_counter(text: str) -> str:
        """Count the number of characters, words, and unique words in a text."""
        chars = len(text)
        words = text.split()
        word_count = len(words)
        unique_count = len(set(w.lower() for w in words))
        return (
            f"'{text}' has {chars} characters, "
            f"{word_count} words, and {unique_count} unique words."
        )

    print(f"  Created: {concept_lookup.name} (LLM-powered)")
    print(f"  Created: {char_counter.name} (pure Python)\n")

    # ========================================================================
    # PART 3: Combining Tools with ToolNode and bind_tools
    # ========================================================================
    print("-" * 70)
    print("Part 3: Combining Tools with ToolNode and bind_tools")
    print("-" * 70)
    print("  We combine all three tools into a list, wrap them in a ToolNode,")
    print("  and bind them to the LLM.\n")

    wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    tools = [wikipedia_tool, concept_lookup, char_counter]
    tool_node = ToolNode(tools)
    model_with_tools = llm.bind_tools(tools)

    print(f"  Tools registered: {[t.name for t in tools]}")
    print("  ToolNode created, tools bound to LLM\n")

    # ========================================================================
    # PART 4: Building the Workflow
    # ========================================================================
    print("-" * 70)
    print("Part 4: Building the Workflow")
    print("-" * 70)
    print("  Using MessagesState (pre-built state), should_continue (router),")
    print("  and call_model (dynamic dispatcher).\n")

    # The stopping function — routes based on tool_calls
    def should_continue(state: MessagesState):
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tools"
        return END

    # The dynamic dispatcher — returns tool response or invokes LLM
    def call_model(state: MessagesState):
        last_message = state["messages"][-1]
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return {
                "messages": [
                    AIMessage(content=last_message.tool_calls[0]["response"])
                ]
            }
        return {"messages": [model_with_tools.invoke(state["messages"])]}

    print("  should_continue: checks last_message.tool_calls → 'tools' or END")
    print("  call_model: AIMessage with tool_calls → return response,")
    print("              otherwise → invoke LLM\n")

    # Wire the graph
    workflow = StateGraph(MessagesState)
    workflow.add_node("chatbot", call_model)
    workflow.add_node("tools", tool_node)
    workflow.add_edge(START, "chatbot")
    workflow.add_conditional_edges("chatbot", should_continue, ["tools", END])
    workflow.add_edge("tools", "chatbot")

    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    print("  Workflow compiled with MemorySaver")
    print()
    print("  Graph structure:")
    print("        ┌──────────┐")
    print("        │  START    │")
    print("        └────┬─────┘")
    print("             │")
    print("             ▼")
    print("        ┌──────────┐       should_continue")
    print("   ┌───►│ chatbot   │──────────────────┐")
    print("   │    │(call_model)│                  │")
    print("   │    └────┬─────┘              no tool calls")
    print("   │         │                         │")
    print("   │    tool_calls?                    ▼")
    print("   │         │                    ┌────────┐")
    print("   │         ▼                    │  END   │")
    print("   │    ┌──────────┐              └────────┘")
    print("   │    │  tools    │")
    print("   │    │(ToolNode) │")
    print("   │    └────┬─────┘")
    print("   │         │")
    print("   └─────────┘\n")

    # ========================================================================
    # PART 5: Testing Multi-Tool Queries
    # ========================================================================
    print("-" * 70)
    print("Part 5: Testing Multi-Tool Queries")
    print("-" * 70)
    print("  Sending queries that take different paths through the workflow.\n")

    # Query 1: Concept explanation → concept_lookup
    config1 = {"configurable": {"thread_id": "demo-concept"}}
    query1 = "What is transfer learning?"
    print(f"  Query 1: \"{query1}\"")
    print("  Expected: chatbot → tools (concept_lookup) → chatbot → END\n")
    response1 = app.invoke({"messages": [("user", query1)]}, config=config1)
    answer1 = response1["messages"][-1].content
    print(f"  Response: {answer1[:200]}..." if len(answer1) > 200 else f"  Response: {answer1}")
    print()

    # Query 2: Text analysis → char_counter
    config2 = {"configurable": {"thread_id": "demo-count"}}
    query2 = "Count the words in: agents use tools to interact with the world"
    print(f"  Query 2: \"{query2}\"")
    print("  Expected: chatbot → tools (char_counter) → chatbot → END\n")
    response2 = app.invoke({"messages": [("user", query2)]}, config=config2)
    answer2 = response2["messages"][-1].content
    print(f"  Response: {answer2}")
    print()

    # Query 3: Factual lookup → wikipedia_tool
    config3 = {"configurable": {"thread_id": "demo-wiki"}}
    query3 = "Tell me about the Hubble Space Telescope"
    print(f"  Query 3: \"{query3}\"")
    print("  Expected: chatbot → tools (wikipedia_tool) → chatbot → END\n")
    response3 = app.invoke({"messages": [("user", query3)]}, config=config3)
    answer3 = response3["messages"][-1].content
    print(f"  Response: {answer3[:200]}..." if len(answer3) > 200 else f"  Response: {answer3}")
    print()

    # Query 4: Memory follow-up in same thread as Query 1
    query4 = "Can you explain that in more detail?"
    print(f"  Query 4 (same thread as Q1): \"{query4}\"")
    print("  Expected: uses memory to recall transfer learning context\n")
    response4 = app.invoke({"messages": [("user", query4)]}, config=config1)
    answer4 = response4["messages"][-1].content
    print(f"  Response: {answer4[:200]}..." if len(answer4) > 200 else f"  Response: {answer4}")
    print()

    # ========================================================================
    # PART 6: Streaming Responses
    # ========================================================================
    print("-" * 70)
    print("Part 6: Streaming Responses")
    print("-" * 70)
    print("  app.invoke() waits for the full response. app.stream() delivers")
    print("  messages in real time using stream_mode='messages'.\n")

    # Single-query streaming helper
    def stream_query(query):
        inputs = {"messages": [HumanMessage(content=query)]}
        for msg, metadata in app.stream(
            inputs, config1, stream_mode="messages"
        ):
            if msg.content and not isinstance(msg, HumanMessage):
                print(msg.content, end="", flush=True)
        print()

    # Stream a concept explanation
    query5 = "What is gradient descent?"
    print(f"  Streaming Query: \"{query5}\"\n")
    config_stream = {"configurable": {"thread_id": "demo-stream"}}
    print("  ", end="")
    inputs5 = {"messages": [HumanMessage(content=query5)]}
    for msg, metadata in app.stream(
        inputs5, config_stream, stream_mode="messages"
    ):
        if msg.content and not isinstance(msg, HumanMessage):
            print(msg.content, end="", flush=True)
    print("\n")

    # Multi-turn streaming conversation
    print("  Multi-turn streaming (same thread, with memory):\n")
    queries = [
        "What is backpropagation?",
        "Can you go into more detail about that?",
        "Count the words in: streaming enables real-time responses",
    ]
    for query in queries:
        print(f"  User: {query}")
        response_text = ""
        for msg, metadata in app.stream(
            {"messages": [HumanMessage(content=query)]},
            config_stream,
            stream_mode="messages",
        ):
            if msg.content and not isinstance(msg, HumanMessage):
                response_text += msg.content
        truncated = response_text[:200] + "..." if len(response_text) > 200 else response_text
        print(f"  Agent: {truncated}\n")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print("\nKey Concepts:")
    print("  1. The @tool decorator labels functions as LangChain tools")
    print("  2. LLM-powered tools call the model; Python tools use code logic")
    print("  3. ToolNode wraps the tools list into a graph-ready node")
    print("  4. bind_tools() gives the LLM awareness of all available tools")
    print("  5. MessagesState provides pre-built state with message accumulation")
    print("  6. should_continue routes based on tool_calls in the last message")
    print("  7. call_model dispatches tool responses or invokes the LLM")
    print("  8. app.stream() with stream_mode='messages' enables real-time output")
    print("\nTo add more capabilities, just create a new @tool function and")
    print("add it to the tools list — no graph changes needed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
