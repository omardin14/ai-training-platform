"""
Challenge: Complete the ReAct Agent

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Loading tools for agents
- Creating ReAct agents
- Invoking agents with questions
- Extracting agent responses
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key or openai_api_key == "your-openai-api-key-here":
    print("❌ Error: OPENAI_API_KEY not found. Please set it in your .env file.")
    exit(1)

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# ============================================================================
# CHALLENGE: Complete the code below
# ============================================================================

# Step 1: Import and load tools
# Replace XXXX___ with the correct import (load_tools)
from langchain_community.agent_toolkits.load_tools import XXXX___
tools = XXXX___(["llm-math"], llm=llm)

# Step 2: Import and create the ReAct agent
# Replace XXXX___ with the correct import (create_react_agent)
from langgraph.prebuilt import XXXX___

# Create the agent
# Replace XXXX___ with the correct function name
agent = XXXX___(llm, tools)

# Step 3: Invoke the agent
# Replace XXXX___ with the correct method name
question = "What is 25 multiplied by 8?"
response = agent.XXXX___({"messages": [("human", question)]})

# Step 4: Extract and print the response
final_answer = response['messages'][-1].content

print(f"\nQuestion: {question}")
print(f"Answer: {final_answer}\n")

