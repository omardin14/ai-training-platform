"""
Challenge: Memory & Conversation

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Setting up MemorySaver for conversation memory
- Compiling the graph with checkpointing
- Configuring a session with thread_id
- Streaming responses with memory enabled
"""

import os
import warnings
from typing import Annotated

from dotenv import load_dotenv
from typing_extensions import TypedDict

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
# CHALLENGE: Complete the code below
# ============================================================================

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langgraph.prebuilt import ToolNode, tools_condition

# Replace XXXX___ with the correct import for memory checkpointing
from langgraph.checkpoint.memory import XXXX___

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# State class at module level
class State(TypedDict):
    messages: Annotated[list, add_messages]


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

# Replace XXXX___ with the correct class to create a memory checkpoint
memory = XXXX___()

# Replace XXXX___ with the correct keyword argument to enable checkpointing
graph = graph_builder.compile(XXXX___=memory)


# Stream responses with memory
def stream_memory_responses(user_input: str):
    # Replace XXXX___ with the correct key for the thread identifier
    config = {"configurable": {"XXXX___": "single_session_memory"}}
    # Replace XXXX___ with the variable to pass as the second argument
    for event in graph.stream({"messages": [("human", user_input)]}, XXXX___):
        for value in event.values():
            # Replace XXXX___ with the correct key to check for messages
            if "XXXX___" in value and value["messages"]:
                print("Agent:", value["messages"][-1].content)


# Test conversation memory
question1 = "What is the Sahara Desert?"
print(f"\nQuestion 1: {question1}\n")
stream_memory_responses(question1)

question2 = "How large is it?"
print(f"\nQuestion 2 (follow-up): {question2}\n")
stream_memory_responses(question2)
