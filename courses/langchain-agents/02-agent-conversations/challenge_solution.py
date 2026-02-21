"""
Challenge Solution: Agent Conversations

This is the complete solution for the agent conversations challenge.
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
    print("❌ Error: OPENAI_API_KEY not found. Agents require an OpenAI API key.")
    print("   Please set it in your .env file.")
    exit(1)

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import create_agent

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Sample tool: convert miles to kilometres
@tool
def miles_to_km(miles: float) -> float:
    """Convert a distance from miles to kilometres."""
    return round(miles * 1.60934, 2)

# ============================================================================
# SOLUTION: Complete code
# ============================================================================

# Step 1: Create the agent with the tool
app = create_agent(model, [miles_to_km])

# Step 2: Send the first query and capture the response
query = "How many kilometres is 26.2 miles?"
response = app.invoke({"messages": [("human", query)]})

# Print input and output
print({"user_input": query,
       "agent_output": response['messages'][-1].content})

# Step 3: Save the message history for follow-up
message_history = response["messages"]

# Step 4: Ask a follow-up question using the conversation history
new_query = "What about 100 miles?"
response = app.invoke({"messages": message_history + [("human", new_query)]})

# Step 5: Filter and display the conversation
filtered_messages = [msg for msg in response["messages"]
                     if isinstance(msg, (HumanMessage, AIMessage))
                     and msg.content.strip()]

print({"user_input": new_query,
       "agent_output": [f"{msg.__class__.__name__}: {msg.content}"
                        for msg in filtered_messages]})
