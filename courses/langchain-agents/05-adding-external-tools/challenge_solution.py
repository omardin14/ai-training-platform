"""
Challenge Solution: Adding External Tools

This is the complete solution for the adding external tools challenge.
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
# SOLUTION: Complete code
# ============================================================================

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun

from langgraph.prebuilt import ToolNode, tools_condition

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
graph = graph_builder.compile()


# Test the chatbot with a factual question
def stream_graph_updates(user_input):
    for event in graph.stream({"messages": [("human", user_input)]}):
        for value in event.values():
            if value["messages"][-1].content:
                print("Agent:", value["messages"][-1].content)


question = "What is the Great Wall of China?"
print(f"\nQuestion: {question}\n")
stream_graph_updates(question)
