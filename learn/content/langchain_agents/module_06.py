"""Module 06: Memory & Conversation - Interactive lesson content."""

MODULE = {
    "id": "06",
    "title": "Memory & Conversation",
    "directory": "06-memory-and-conversation",
    "examples": ["memory_and_conversation_example.py"],
    "quiz": [
        {
            "question": "What does MemorySaver do in a LangGraph chatbot?",
            "choices": [
                "Stores conversation history as checkpoints so the chatbot can handle follow-up questions",
                "Saves the graph structure to a file on disk for later reloading",
                "Compresses messages to reduce memory usage during long conversations",
            ],
            "answer": 0,
            "explanation": (
                "MemorySaver stores the graph's conversation state as "
                "in-memory checkpoints. This allows the chatbot to "
                "reference previous messages when answering follow-up "
                "questions, maintaining conversation context across turns."
            ),
        },
        {
            "question": "What is the purpose of thread_id in the config dictionary?",
            "choices": [
                "It identifies a unique conversation session for storing and retrieving memory",
                "It sets the maximum number of messages the chatbot can remember",
                "It specifies which LLM model to use for the conversation",
            ],
            "answer": 0,
            "explanation": (
                "The thread_id is a unique identifier for a conversation "
                "session. All messages sent with the same thread_id share "
                "the same memory. Different thread_id values create "
                "separate, independent conversations."
            ),
        },
        {
            "question": "How do you enable memory in a compiled graph?",
            "choices": [
                "Pass checkpointer=memory to graph_builder.compile()",
                "Call graph.enable_memory() after compiling",
                "Add a memory node to the graph with graph_builder.add_node('memory')",
            ],
            "answer": 0,
            "explanation": (
                "Memory is enabled by passing the MemorySaver instance "
                "as the checkpointer parameter when compiling: "
                "graph_builder.compile(checkpointer=memory). This tells "
                "the graph to save its state after each step."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Memory and conversation with MemorySaver",
        "hints": [
            "The first XXXX___ should be the memory checkpoint class (MemorySaver)",
            "The second XXXX___ should be the class to create a memory instance (MemorySaver)",
            "The third XXXX___ should be the keyword argument for checkpointing (checkpointer)",
            "The fourth XXXX___ should be the key for the thread identifier (thread_id)",
            "The fifth XXXX___ should be the variable to pass to .stream() (config)",
            "The sixth XXXX___ should be the key to check for in the event value (messages)",
        ],
    },
}
