"""Module 01: ReAct Agents & Custom Tools - Interactive lesson content."""

MODULE = {
    "id": "01",
    "title": "ReAct Agents & Custom Tools",
    "directory": "01-react-agents-tools",
    "examples": ["react_agent_tools_example.py"],
    "quiz": [
        {
            "question": "What does ReAct stand for in the context of LangChain agents?",
            "choices": [
                "Reasoning and Action",
                "Reactive and Autonomous",
                "Read and Compile Tokens",
            ],
            "answer": 0,
            "explanation": (
                "ReAct stands for Reasoning and Action. The agent reasons "
                "about what it needs to do and then acts by calling tools "
                "to produce an answer."
            ),
        },
        {
            "question": "What is the purpose of the @tool decorator in LangChain?",
            "choices": [
                "It converts a Python function into a tool that agents can call",
                "It optimises the function to run faster on GPUs",
                "It automatically generates unit tests for the function",
            ],
            "answer": 0,
            "explanation": (
                "The @tool decorator from langchain_core.tools converts a "
                "regular Python function into a tool that ReAct agents can "
                "discover and call. The function's docstring becomes the "
                "tool description the LLM uses to decide when to invoke it."
            ),
        },
        {
            "question": "How does a ReAct agent decide which tool to call?",
            "choices": [
                "It calls every tool and picks the best result",
                "It reads the tool's docstring description and matches it to the question",
                "It uses the tool's function name alphabetically",
            ],
            "answer": 1,
            "explanation": (
                "The LLM reads each tool's description (from the docstring) "
                "and matches it against the user's question to decide which "
                "tool is most relevant. A clear, descriptive docstring is "
                "essential for the agent to pick the right tool."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "ReAct agents and custom tools",
        "hints": [
            "The first XXXX___ should be an import (tool)",
            "The second XXXX___ should be the decorator name (tool)",
            "The third XXXX___ should be an import (create_agent)",
            "The fourth XXXX___ should be a function name (create_agent)",
            "The fifth XXXX___ should be a method name (invoke)",
        ],
    },
}
