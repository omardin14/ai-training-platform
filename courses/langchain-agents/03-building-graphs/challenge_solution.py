"""
Challenge Solution: Building Graphs

This is the complete solution for the building graphs challenge.
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
    print("❌ Error: OPENAI_API_KEY not found.")
    print("   Please set it in your .env file.")
    exit(1)

# ============================================================================
# SOLUTION: Complete code
# ============================================================================

# Step 1: Import the modules for structuring text
from typing import Annotated
from typing_extensions import TypedDict

# Step 2: Import LangGraph modules
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Step 3: Define the State class
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Step 4: Initialise the graph builder
graph_builder = StateGraph(State)

# Step 5: Define the chatbot function
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# Add node, edges, and compile
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

# Test the chatbot
question = "What are three popular programming languages for data science?"
response = graph.invoke({"messages": [("human", question)]})
answer = response["messages"][-1].content

print(f"\nQuestion: {question}")
print(f"Answer: {answer}\n")
