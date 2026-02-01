"""
Challenge Solution: ReAct Agent

This is the complete solution for the ReAct agent challenge.
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
# SOLUTION: Complete code
# ============================================================================

# Step 1: Import and load tools
from langchain_community.agent_toolkits.load_tools import load_tools
tools = load_tools(["llm-math"], llm=llm)

# Step 2: Import and create the ReAct agent
from langgraph.prebuilt import create_react_agent

# Create the agent
agent = create_react_agent(llm, tools)

# Step 3: Invoke the agent
question = "What is 25 multiplied by 8?"
response = agent.invoke({"messages": [("human", question)]})

# Step 4: Extract and print the response
final_answer = response['messages'][-1].content

print(f"\nQuestion: {question}")
print(f"Answer: {final_answer}\n")

