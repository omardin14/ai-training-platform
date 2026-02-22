"""Module 03: Building Graphs - Interactive lesson content."""

MODULE = {
    "id": "03",
    "title": "Building Graphs",
    "directory": "03-building-graphs",
    "examples": ["building_graphs_example.py"],
    "quiz": [
        {
            "question": "In LangGraph, what do nodes and edges represent?",
            "choices": [
                "Nodes are functions and edges are connections between them",
                "Nodes are data stores and edges are API calls",
                "Nodes are users and edges are their messages",
            ],
            "answer": 0,
            "explanation": (
                "In LangGraph, nodes represent functions (like generating "
                "a response or calling a tool) and edges define the "
                "connections between them, creating the workflow."
            ),
        },
        {
            "question": "What does Annotated[list, add_messages] do in the State class?",
            "choices": [
                "It ensures new messages are appended to the list rather than replacing it",
                "It encrypts the messages for security",
                "It limits the list to a maximum number of messages",
            ],
            "answer": 0,
            "explanation": (
                "The Annotated type combined with add_messages tells "
                "LangGraph to append new messages to the existing list "
                "with metadata, rather than overwriting the entire list. "
                "This preserves conversation history."
            ),
        },
        {
            "question": "What does graph_builder.compile() do?",
            "choices": [
                "It turns the graph builder into a runnable application",
                "It saves the graph to a file on disk",
                "It validates the Python syntax of all node functions",
            ],
            "answer": 0,
            "explanation": (
                "The .compile() method takes the graph builder with its "
                "nodes and edges and produces a compiled graph that can be "
                "invoked like any LangChain agent, processing messages "
                "through the defined workflow."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Building graphs with LangGraph",
        "hints": [
            "The first three XXXX___ should be imports (StateGraph, START, END)",
            "The fourth XXXX___ should be the base class for State (TypedDict)",
            "The fifth XXXX___ should be the message annotation (add_messages)",
            "The sixth XXXX___ should be the graph class (StateGraph)",
            "The seventh XXXX___ should be the LLM method (invoke)",
        ],
    },
}
