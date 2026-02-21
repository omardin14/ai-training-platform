"""Module 02: Agent Conversations - Interactive lesson content."""

MODULE = {
    "id": "02",
    "title": "Agent Conversations",
    "directory": "02-agent-conversations",
    "examples": ["agent_conversations_example.py"],
    "quiz": [
        {
            "question": "How do you pass conversation history when asking a follow-up question?",
            "choices": [
                "Combine message_history + the new query in the messages list",
                "Set a 'history=True' flag on the agent",
                "Call agent.remember() before invoking again",
            ],
            "answer": 0,
            "explanation": (
                "You pass the full message history from the previous response "
                "together with the new query: "
                'app.invoke({"messages": message_history + [("human", new_query)]}). '
                "This lets the agent see the entire conversation so far."
            ),
        },
        {
            "question": "What do HumanMessage and AIMessage represent in a conversation?",
            "choices": [
                "HumanMessage is the user's query, AIMessage is the agent's response",
                "HumanMessage is the tool input, AIMessage is the tool output",
                "HumanMessage is the system prompt, AIMessage is the model config",
            ],
            "answer": 0,
            "explanation": (
                "HumanMessage represents queries from the user, while AIMessage "
                "represents responses from the agent. Together they form the "
                "conversation history that the agent uses for context."
            ),
        },
        {
            "question": "Why do we filter messages with isinstance() and .strip()?",
            "choices": [
                "To extract only HumanMessage and AIMessage with actual content",
                "To remove duplicate messages from the history",
                "To convert all messages to plain strings",
            ],
            "answer": 0,
            "explanation": (
                "The response contains internal messages like tool calls. "
                "Filtering with isinstance(msg, (HumanMessage, AIMessage)) "
                "and msg.content.strip() gives us only the human-readable "
                "conversation with non-empty content."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Agent conversations and message history",
        "hints": [
            "The first XXXX___ should be the function to create an agent (create_agent)",
            'The second XXXX___ should be the dictionary key for messages ("messages")',
            "The third XXXX___ should be the variable holding previous messages (message_history)",
            "The fourth XXXX___ should be the user message class (HumanMessage)",
            "The fifth XXXX___ should be the agent message class (AIMessage)",
        ],
    },
}
