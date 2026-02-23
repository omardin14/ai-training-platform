"""Module 07: Multi-Tool Chatbot - Interactive lesson content."""

MODULE = {
    "id": "07",
    "title": "Multi-Tool Chatbot",
    "directory": "07-multi-tool-chatbot",
    "examples": ["multi_tool_chatbot.py"],
    "quiz": [
        {
            "question": "What is the purpose of the @tool decorator in LangChain?",
            "choices": [
                "It labels a function as a tool, exposing its name, input type, and docstring so the LLM can decide when to call it",
                "It converts a Python function into a REST API endpoint for external services",
                "It automatically optimises the function to run faster inside a LangGraph node",
            ],
            "answer": 0,
            "explanation": (
                "The @tool decorator registers a Python function as a "
                "LangChain tool. The LLM reads the function name, type "
                "hints, and docstring to decide when and how to call "
                "the tool during a conversation. Without this metadata "
                "the LLM would not know the tool exists."
            ),
        },
        {
            "question": "What is the key difference between an LLM-powered tool and a pure Python tool?",
            "choices": [
                "An LLM-powered tool invokes the language model internally to generate a response, while a pure Python tool uses standard code logic without any LLM call",
                "An LLM-powered tool is always faster because it runs on a GPU, while a Python tool runs on a CPU",
                "There is no difference -- both types always require an LLM call to produce output",
            ],
            "answer": 0,
            "explanation": (
                "LLM-powered tools call the language model internally "
                "for tasks that need natural language understanding, such "
                "as explaining a concept or summarising text. Pure Python "
                "tools use standard programming logic for deterministic "
                "tasks like counting characters or performing calculations, "
                "making them faster and more predictable."
            ),
        },
        {
            "question": "What do should_continue and call_model do in a multi-tool workflow?",
            "choices": [
                "should_continue checks if the last message has tool_calls and routes accordingly, while call_model dispatches tool responses or invokes the LLM depending on the message type",
                "should_continue stops the workflow after a fixed number of turns, while call_model always calls the LLM regardless of the message",
                "should_continue logs messages for debugging, while call_model forwards messages to an external API",
            ],
            "answer": 0,
            "explanation": (
                "should_continue is the routing gate -- it inspects the "
                "last message for tool_calls and returns 'tools' or END. "
                "call_model is the dynamic dispatcher -- if the last "
                "message is an AIMessage with tool_calls it returns the "
                "tool response directly, otherwise it invokes the LLM "
                "with the full message history. Together they separate "
                "routing from execution."
            ),
        },
        {
            "question": "What does app.stream() with stream_mode='messages' do differently from app.invoke()?",
            "choices": [
                "It returns an iterator of (message, metadata) tuples in real time instead of waiting for the complete response",
                "It sends the response to a WebSocket server for browser rendering",
                "It splits the response into fixed-size chunks and writes them to a file",
            ],
            "answer": 0,
            "explanation": (
                "app.stream() with stream_mode='messages' yields "
                "(message, metadata) tuples as they flow through the "
                "graph, enabling real-time output. You filter out "
                "HumanMessage instances to display only the chatbot's "
                "responses. This is ideal for interactive chatbots where "
                "users expect to see tokens appear as they are generated."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "building a multi-tool chatbot workflow with custom tools, routing, and streaming",
        "hints": [
            "First XXXX___ should be 'tool' (the decorator from langchain_core.tools)",
            "Second XXXX___ should be 'MessagesState' (the pre-built state class from langgraph.graph)",
            "Third XXXX___ should be 'concept_lookup' (the LLM-powered tool function name)",
            "Fourth XXXX___ should be 'char_counter' (the pure Python tool function name)",
            "Fifth XXXX___ should be 'call_model' (the dynamic dispatcher function name)",
            "Sixth XXXX___ should be 'bind_tools' (the method to attach tools to the LLM)",
            "Seventh XXXX___ should be '\"messages\"' (the stream mode for real-time output)",
            "Eighth XXXX___ should be 'HumanMessage' (the message type to filter out of the stream)",
        ],
    },
}
