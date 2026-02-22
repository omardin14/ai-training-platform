"""
Challenge: Adding External Tools

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Setting up the Wikipedia tool with WikipediaAPIWrapper and WikipediaQueryRun
- Binding tools to the LLM with .bind_tools()
- Using ToolNode and tools_condition for conditional routing
- Building a complete graph with tool integration
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

# Replace XXXX___ with the correct import for the Wikipedia API wrapper
from langchain_community.utilities import XXXX___
# Replace XXXX___ with the correct import for the Wikipedia query tool
from langchain_community.tools import XXXX___

# Replace XXXX___ with the correct imports for ToolNode and tools_condition
from langgraph.prebuilt import XXXX___, XXXX___

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# State class at module level
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Set up the Wikipedia tool
api_wrapper = WikipediaAPIWrapper(top_k_results=1)
wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
tools = [wikipedia_tool]

# Bind tools to the LLM
# Replace XXXX___ with the correct method to bind tools
llm_with_tools = llm.XXXX___(tools)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# Build the graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

# Replace XXXX___ with the correct class to create the tool node
tool_node = XXXX___(tools=[wikipedia_tool])
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")

# Replace XXXX___ with the correct function for conditional routing
graph_builder.add_conditional_edges("chatbot", XXXX___)

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
