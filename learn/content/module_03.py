"""Module 03: Prompt Chains - Interactive lesson content."""

MODULE = {
    "id": "03",
    "title": "Prompt Chains",
    "directory": "03-prompt-chains",
    "examples": ["prompt_chain_example.py"],
    "quiz": [
        {
            "question": (
                "What operator is used to chain prompt templates "
                "with models in LangChain?"
            ),
            "choices": [
                "+ (plus)",
                "| (pipe)",
                "-> (arrow)",
            ],
            "answer": 1,
            "explanation": (
                "The pipe operator (|) is used to chain "
                "components together in LangChain."
            ),
        },
        {
            "question": (
                "What method is used to invoke a chain "
                "with input variables?"
            ),
            "choices": [
                ".invoke()",
                ".call()",
                ".run()",
            ],
            "answer": 0,
            "explanation": (
                "The .invoke() method is used to run "
                "a chain with input variables."
            ),
        },
        {
            "question": (
                "In the code 'chain = prompt | llm', "
                "what does the pipe operator do?"
            ),
            "choices": [
                "It saves the prompt to a file",
                "It formats the prompt and sends it to the model",
                "It connects the prompt template with the LLM to create a chain",
            ],
            "answer": 2,
            "explanation": (
                "The pipe operator connects components "
                "to create a chain that can be invoked later."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Prompt chains",
        "hints": [
            "The first XXXX___ should be a method name (from_template)",
            "The second XXXX___ should be an operator (|)",
            "The third XXXX___ should be a method name (invoke)",
        ],
    },
}
