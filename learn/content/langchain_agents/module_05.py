"""Module 05: Adding External Tools - Interactive lesson content."""

MODULE = {
    "id": "05",
    "title": "Adding External Tools",
    "directory": "05-adding-external-tools",
    "examples": ["adding_external_tools_example.py"],
    "quiz": [
        {
            "question": "What does .bind_tools(tools) do?",
            "choices": [
                "Enables the LLM to recognise tools and decide when to call them",
                "Installs the tools as Python packages in the environment",
                "Permanently modifies the LLM to always use tools for every query",
            ],
            "answer": 0,
            "explanation": (
                ".bind_tools(tools) creates a new LLM instance that knows "
                "about the available tools. The LLM can then decide when to "
                "call a tool based on the question, rather than always using "
                "one or never using one."
            ),
        },
        {
            "question": "What is the role of tools_condition in the graph?",
            "choices": [
                "It checks if the last message contains tool calls and routes to tools or END",
                "It validates that all tools are properly installed before running",
                "It counts how many times each tool has been called during the session",
            ],
            "answer": 0,
            "explanation": (
                "tools_condition is a prebuilt function that inspects the "
                "chatbot's last message. If it contains a tool call request, "
                "the graph routes to the tools node. Otherwise, the graph "
                "routes to END and the response is returned to the user."
            ),
        },
        {
            "question": "How does ToolNode work in the graph?",
            "choices": [
                "It executes the requested tools and returns results as messages",
                "It displays a list of available tools to the user",
                "It removes tools from the graph after they have been used once",
            ],
            "answer": 0,
            "explanation": (
                "ToolNode is a prebuilt LangGraph node that receives tool "
                "call requests from the chatbot, executes the appropriate "
                "tool (like Wikipedia), and returns the results as "
                "ToolMessages that the chatbot can then use to formulate "
                "its response."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Adding external tools to a LangGraph chatbot",
        "hints": [
            "The first XXXX___ should be the Wikipedia API wrapper class (WikipediaAPIWrapper)",
            "The second XXXX___ should be the Wikipedia query tool class (WikipediaQueryRun)",
            "The third XXXX___ should be the prebuilt tool node class (ToolNode)",
            "The fourth XXXX___ should be the prebuilt routing function (tools_condition)",
            "The fifth XXXX___ should be the method to bind tools to the LLM (bind_tools)",
            "The sixth XXXX___ should be the class to create the tool node (ToolNode)",
            "The seventh XXXX___ should be the routing function for conditional edges (tools_condition)",
        ],
    },
}
