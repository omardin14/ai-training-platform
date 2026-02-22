"""
Challenge: Building Graphs

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Defining a State class with TypedDict and Annotated
- Initialising a StateGraph
- Creating a chatbot function node
- Connecting nodes with edges (START → chatbot → END)
- Compiling the graph
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
# CHALLENGE: Complete the code below
# ============================================================================

# Step 1: Import the modules for structuring text
from typing import Annotated
from typing_extensions import TypedDict

# Step 2: Import LangGraph modules
# Replace XXXX___ with the correct imports (StateGraph, START, END)
from langgraph.graph import XXXX___, XXXX___, XXXX___
from langgraph.graph.message import add_messages

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Step 3: Define the State class using TypedDict
# Replace XXXX___ with the correct base class
class State(XXXX___):
    # Replace XXXX___ with the correct annotation for messages
    messages: Annotated[list, XXXX___]

# Step 4: Initialise the graph builder with the State
# Replace XXXX___ with the correct class name
graph_builder = XXXX___(State)

# Step 5: Define the chatbot function that generates a response
def chatbot(state: State):
    # Replace XXXX___ with the correct method to call the LLM
    return {"messages": [llm.XXXX___(state["messages"])]}

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
