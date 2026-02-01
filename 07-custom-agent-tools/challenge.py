"""
Challenge: Create a Custom Tool

Your task is to complete the code below by filling in the missing parts.
Replace the XXXX___ placeholders with the correct code.

This challenge tests your understanding of:
- Creating custom tools with the @tool decorator
- Using custom tools with ReAct agents
- Invoking agents with custom tools
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
# CHALLENGE: Complete the code below
# ============================================================================

# Step 1: Import the @tool decorator
# Replace XXXX___ with the correct import (tool)
from langchain_core.tools import XXXX___

# Step 2: Create a custom tool using the @tool decorator
# Replace XXXX___ with the decorator name (@tool)
@XXXX___
def get_book_info(book_id: str) -> str:
    """Retrieve book information from library based on book ID."""
    if book_id in book_library:
        book = book_library[book_id]
        status = "Available" if book['available'] else "Checked Out"
        return f"Title: {book['title']}\nAuthor: {book['author']}\nPages: {book['pages']}\nStatus: {status}"
    else:
        return f"Book '{book_id}' not found in library."

# Step 3: Import and create the ReAct agent with the custom tool
# Replace XXXX___ with the correct import (create_react_agent)
from langgraph.prebuilt import XXXX___

# Create the agent with the custom tool
# Replace XXXX___ with the correct function name
agent = XXXX___(llm, [get_book_info])

# Step 4: Invoke the agent
# Replace XXXX___ with the correct method name
question = "What is the author and availability status of the python-basics book?"
response = agent.XXXX___({"messages": [("human", question)]})

# Step 5: Extract and print the response
final_answer = response['messages'][-1].content

print(f"\nQuestion: {question}")
print(f"Answer: {final_answer}\n")

