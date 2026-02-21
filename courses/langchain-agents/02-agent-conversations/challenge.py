"""
Challenge: Agent Conversations

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Sending a query and reading the agent's response
- Saving message history for follow-up questions
- Passing conversation history to the agent
- Filtering HumanMessage and AIMessage from the response
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
# CHALLENGE: Complete the code below
# ============================================================================

# Step 1: Create the agent with the tool
# Replace XXXX___ with the correct function name
app = XXXX___(model, [miles_to_km])

# Step 2: Send the first query and capture the response
query = "How many kilometres is 26.2 miles?"
response = app.invoke({"messages": [("human", query)]})

# Print input and output
print({"user_input": query,
       "agent_output": response['messages'][-1].content})

# Step 3: Save the message history for follow-up
# Replace XXXX___ with the correct key to access the messages list
message_history = response[XXXX___]

# Step 4: Ask a follow-up question using the conversation history
# Replace XXXX___ with the variable that holds the previous messages
new_query = "What about 100 miles?"
response = app.invoke({"messages": XXXX___ + [("human", new_query)]})

# Step 5: Filter and display the conversation
# Replace XXXX___ with the two message classes to filter for
filtered_messages = [msg for msg in response["messages"]
                     if isinstance(msg, (XXXX___, XXXX___))
                     and msg.content.strip()]

print({"user_input": new_query,
       "agent_output": [f"{msg.__class__.__name__}: {msg.content}"
                        for msg in filtered_messages]})
