"""
Challenge Solution: ReAct Agents & Custom Tools

This is the complete solution for the ReAct agents and custom tools challenge.
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
    print("❌ Error: OPENAI_API_KEY not found. ReAct agents require an OpenAI API key.")
    print("   Please set it in your .env file.")
    exit(1)

from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Sample data: a small inventory of planets
planet_catalog = {
    "mars": {
        "name": "Mars",
        "distance_from_sun_km": 227_900_000,
        "diameter_km": 6_779,
        "moons": 2,
    },
    "jupiter": {
        "name": "Jupiter",
        "distance_from_sun_km": 778_500_000,
        "diameter_km": 139_820,
        "moons": 95,
    },
}

# ============================================================================
# SOLUTION: Complete code
# ============================================================================

# Step 1: Import the @tool decorator
from langchain_core.tools import tool

# Step 2: Create a custom tool using the @tool decorator
@tool
def get_planet_info(planet_id: str) -> str:
    """Retrieve information about a planet from the catalog by its ID."""
    if planet_id in planet_catalog:
        p = planet_catalog[planet_id]
        return (
            f"Planet: {p['name']}\n"
            f"Distance from Sun: {p['distance_from_sun_km']:,} km\n"
            f"Diameter: {p['diameter_km']:,} km\n"
            f"Moons: {p['moons']}"
        )
    return f"Planet '{planet_id}' not found in catalog."

# Step 3: Import and create the ReAct agent
from langgraph.prebuilt import create_react_agent

# Create the agent with the custom tool
agent = create_react_agent(model, [get_planet_info])

# Step 4: Invoke the agent with a natural language question
question = "How many moons does Jupiter have and what is its diameter?"
response = agent.invoke({"messages": [("human", question)]})

# Step 5: Extract and print the response
final_answer = response['messages'][-1].content

print(f"\nQuestion: {question}")
print(f"Answer: {final_answer}\n")
