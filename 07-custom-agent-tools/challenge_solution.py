"""
Challenge Solution: Custom Tool

This is the complete solution for the custom tool challenge.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key or openai_api_key == "your-openai-api-key-here":
    print("❌ Error: OPENAI_API_KEY not found. ReAct agents require an OpenAI API key.")
    print("   Please set it in your .env file.")
    exit(1)

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Sample data
book_library = {
    "python-basics": {
        "title": "Python Basics",
        "author": "Jane Smith",
        "pages": 350,
        "available": True
    },
    "data-science": {
        "title": "Data Science Handbook",
        "author": "John Doe",
        "pages": 520,
        "available": False
    }
}

# ============================================================================
# SOLUTION: Complete code
# ============================================================================

# Step 1: Import the @tool decorator
from langchain_core.tools import tool

# Step 2: Create a custom tool using the @tool decorator
@tool
def get_book_info(book_id: str) -> str:
    """Retrieve book information from library based on book ID."""
    if book_id in book_library:
        book = book_library[book_id]
        status = "Available" if book['available'] else "Checked Out"
        return f"Title: {book['title']}\nAuthor: {book['author']}\nPages: {book['pages']}\nStatus: {status}"
    else:
        return f"Book '{book_id}' not found in library."

# Step 3: Import and create the ReAct agent with the custom tool
from langgraph.prebuilt import create_react_agent

# Create the agent with the custom tool
agent = create_react_agent(llm, [get_book_info])

# Step 4: Invoke the agent
question = "What is the author and availability status of the python-basics book?"
response = agent.invoke({"messages": [("human", question)]})

# Step 5: Extract and print the response
final_answer = response['messages'][-1].content

print(f"\nQuestion: {question}")
print(f"Answer: {final_answer}\n")

