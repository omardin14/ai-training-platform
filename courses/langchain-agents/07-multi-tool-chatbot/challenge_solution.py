"""
Challenge Solution: Multi-Tool Chatbot

This is the complete solution for reference.
Try to solve the challenge yourself before looking at this!
"""

import os
import warnings

from dotenv import load_dotenv

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*deprecated.*", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*LangGraphDeprecated.*")

# Load environment variables
load_dotenv()

# Check for API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key or openai_api_key == "your-openai-api-key-here":
    print("Error: OPENAI_API_KEY not found.")
    print("   Please set it in your .env file.")
    exit(1)

# ============================================================================
# SOLUTION
# ============================================================================

# Solution: import the 'tool' decorator
from langchain_core.tools import tool

# Solution: import MessagesState
from langgraph.graph import MessagesState, START, END, StateGraph

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# --- Tool 1: LLM-powered concept explainer ---
# Solution: function name is 'concept_lookup'
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


# --- Tool 2: Pure Python text analyser ---
# Solution: function name is 'char_counter'
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


# --- Combine tools ---
wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
tools = [wikipedia_tool, concept_lookup, char_counter]
tool_node = ToolNode(tools)

# Solution: use bind_tools() to attach tools to the LLM
model_with_tools = llm.bind_tools(tools)


# --- Workflow functions ---
def should_continue(state: MessagesState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END


# Solution: function name is 'call_model'
def call_model(state: MessagesState):
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return {
            "messages": [
                AIMessage(content=last_message.tool_calls[0]["response"])
            ]
        }
    return {"messages": [model_with_tools.invoke(state["messages"])]}


# --- Build the graph ---
workflow = StateGraph(MessagesState)
workflow.add_node("chatbot", call_model)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "chatbot")
workflow.add_conditional_edges("chatbot", should_continue, ["tools", END])
workflow.add_edge("tools", "chatbot")

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


# --- Test the multi-tool chatbot ---
print("\n" + "=" * 60)
print("Testing the Multi-Tool Chatbot")
print("=" * 60)

# Test 1: Concept explanation (should use concept_lookup)
query1 = "What is reinforcement learning?"
print(f"\nQuery 1: {query1}")
config1 = {"configurable": {"thread_id": "test-1"}}
response1 = app.invoke({"messages": [("user", query1)]}, config=config1)
print(f"Answer:  {response1['messages'][-1].content[:200]}")

# Test 2: Text analysis (should use char_counter)
query2 = "Count the words in: the graph routes each message to the right tool"
print(f"\nQuery 2: {query2}")
config2 = {"configurable": {"thread_id": "test-2"}}
response2 = app.invoke({"messages": [("user", query2)]}, config=config2)
print(f"Answer:  {response2['messages'][-1].content}")

# Test 3: Memory follow-up (same thread as Test 1)
query3 = "Can you go into more detail about that?"
print(f"\nQuery 3 (follow-up): {query3}")
response3 = app.invoke({"messages": [("user", query3)]}, config=config1)
print(f"Answer:  {response3['messages'][-1].content[:200]}")

# --- Streaming responses ---
print("\n" + "-" * 60)
print("Test 4: Streaming Responses")
print("-" * 60)


# Solution: stream_mode is "messages", filter out HumanMessage
def stream_query(query):
    inputs = {"messages": [HumanMessage(content=query)]}
    for msg, metadata in app.stream(inputs, config1, stream_mode="messages"):
        if msg.content and not isinstance(msg, HumanMessage):
            print(msg.content, end="", flush=True)
    print()


query4 = "What is gradient descent?"
print(f"\nStreaming: {query4}")
stream_query(query4)

print("\n" + "=" * 60)
print("All tests passed! Your multi-tool chatbot works correctly.")
print("=" * 60 + "\n")
