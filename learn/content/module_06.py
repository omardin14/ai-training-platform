"""Module 06: ReAct Agents - Interactive lesson content."""

MODULE = {
    "id": "06",
    "title": "ReAct Agents",
    "directory": "06-ReAct-agents",
    "examples": ["react_agent_example.py"],
    "quiz": [
        {
            "question": "What does ReAct stand for?",
            "choices": [
                "Reasoning + Acting",
                "Reading + Action",
                "Response + Action",
            ],
            "answer": 0,
            "explanation": (
                "ReAct stands for Reasoning + Acting, combining "
                "the ability to reason about problems with taking "
                "actions through tools."
            ),
        },
        {
            "question": (
                "What is the main advantage of ReAct agents "
                "over regular LLMs?"
            ),
            "choices": [
                "They are faster",
                "They can use tools to perform actions and gather information",
                "They use less memory",
            ],
            "answer": 1,
            "explanation": (
                "ReAct agents can use tools to extend their capabilities "
                "beyond text generation, such as performing calculations "
                "or searching for information."
            ),
        },
        {
            "question": "How does a ReAct agent decide when to use a tool?",
            "choices": [
                "The user must specify which tool to use",
                "Tools are used randomly",
                "The agent automatically reasons about the question and decides",
            ],
            "answer": 2,
            "explanation": (
                "The agent automatically reasons about the question "
                "and decides when and which tools to use based on "
                "what is needed to answer the question."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "ReAct agents",
        "hints": [
            "The first XXXX___ should be an import (load_tools)",
            "The second XXXX___ should be an import (create_react_agent)",
            "The third XXXX___ should be a function name (create_react_agent)",
            "The fourth XXXX___ should be a method name (invoke)",
        ],
    },
}
