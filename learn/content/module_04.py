"""Module 04: Few-Shot Prompts - Interactive lesson content."""

MODULE = {
    "id": "04",
    "title": "Few-Shot Prompts",
    "directory": "04-few-shot-prompts",
    "examples": ["few_shot_example.py"],
    "quiz": [
        {
            "question": "What is the main purpose of few-shot prompting?",
            "choices": [
                "To provide examples that help the model understand the desired format",
                "To reduce API costs",
                "To make models run faster",
            ],
            "answer": 0,
            "explanation": (
                "Few-shot prompts provide examples to guide "
                "the model's understanding of the desired format and behavior."
            ),
        },
        {
            "question": (
                "Which class is used to create few-shot prompts "
                "in LangChain?"
            ),
            "choices": [
                "PromptTemplate",
                "FewShotPromptTemplate",
                "ExampleTemplate",
            ],
            "answer": 1,
            "explanation": (
                "FewShotPromptTemplate is the LangChain class "
                "specifically designed for creating few-shot prompts."
            ),
        },
        {
            "question": "How do examples help the model?",
            "choices": [
                "They reduce token usage",
                "They make the model run faster",
                "They show the model the pattern to follow and improve accuracy",
            ],
            "answer": 2,
            "explanation": (
                "Examples show the model the pattern to follow, "
                "which improves accuracy and format consistency."
            ),
        },
    ],
    "challenge": {
        "file": "challenge.py",
        "topic": "Few-shot prompts",
        "hints": [
            "The first XXXX___ should be imports (PromptTemplate, FewShotPromptTemplate)",
            "The second XXXX___ should be a class name (PromptTemplate)",
            "The third XXXX___ should be a method name (from_template)",
            "The fourth XXXX___ should be a class name (FewShotPromptTemplate)",
        ],
    },
}
