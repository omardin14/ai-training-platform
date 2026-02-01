.PHONY: help run all install setup venv clean quiz challenge

# Virtual environment directory
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

help:
	@echo "LangChain Few-Shot Prompts Demo - Makefile Commands"
	@echo "===================================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup        - Create .env file from template"
	@echo "  make venv         - Create virtual environment only"
	@echo "  make install      - Create venv and install all dependencies"
	@echo "  make run          - Run the few-shot prompt example"
	@echo "  make quiz         - Take a quiz to test your knowledge"
	@echo "  make challenge    - Complete the coding challenge"
	@echo "  make all          - Run all examples"
	@echo "  make clean        - Clean Python cache files and virtual environment"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. Run 'make setup' to create .env file"
	@echo "  2. Edit .env and add your API keys (optional)"
	@echo "  3. Run 'make install' to set up virtual environment and install dependencies"
	@echo "  4. Run 'make run' to see the example"
	@echo ""

setup:
	@if [ ! -f .env ]; then \
		if [ -f .env.example ]; then \
			echo "Creating .env file from .env.example..."; \
			cp .env.example .env; \
			echo "✓ .env file created from .env.example!"; \
			echo "  Edit .env and add your API key if you want to use OpenAI."; \
			echo "  If no API key is set, the example will use Hugging Face model."; \
		else \
			echo "Creating .env file from template..."; \
			echo "# OpenAI API Key (Optional)" > .env; \
			echo "# Get your key from: https://platform.openai.com/api-keys" >> .env; \
			echo "# If not set, the example will use Hugging Face model" >> .env; \
			echo "OPENAI_API_KEY=your-openai-api-key-here" >> .env; \
			echo "✓ .env file created! Please edit it and add your API keys."; \
		fi \
	else \
		echo "⚠️  .env file already exists. Skipping..."; \
	fi

venv:
	@if [ ! -d $(VENV) ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV); \
		echo "✓ Virtual environment created!"; \
	else \
		echo "✓ Virtual environment already exists."; \
	fi

install: venv
	@echo "Installing dependencies..."
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "✓ Installation complete!"
	@echo ""
	@echo "Virtual environment is ready! All commands will use it automatically."

run: install
	@echo "Running few-shot prompt example..."
	@if [ ! -f .env ] && [ -z "$$OPENAI_API_KEY" ]; then \
		echo "⚠️  Note: .env file not found and OPENAI_API_KEY not set"; \
		echo "   The example will use Hugging Face model (may take time on first run)"; \
		echo ""; \
	fi
	@$(PYTHON) few_shot_example.py

all: run
	@echo ""
	@echo "✓ All examples completed!"

quiz:
	@echo ""
	@echo "======================================================================"
	@echo "📝 Few-Shot Prompts Quiz"
	@echo "======================================================================"
	@echo ""
	@echo "Test your knowledge of few-shot prompts!"
	@echo "Answer each question by typing a, b, or c"
	@echo ""
	@score=0; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 1 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  What is the main purpose of few-shot prompting?"; \
	echo ""; \
	echo "    a) To provide examples that help the model understand the desired format"; \
	echo "    b) To reduce API costs"; \
	echo "    c) To make models run faster"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans1; \
	echo ""; \
	if [ "$$ans1" = "a" ] || [ "$$ans1" = "A" ]; then \
		echo "  ✓ Correct! Few-shot prompts provide examples to guide the model."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is a) To provide examples for format understanding"; \
	fi; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 2 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  Which class is used to create few-shot prompts in LangChain?"; \
	echo ""; \
	echo "    a) PromptTemplate"; \
	echo "    b) FewShotPromptTemplate"; \
	echo "    c) ExampleTemplate"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans2; \
	echo ""; \
	if [ "$$ans2" = "b" ] || [ "$$ans2" = "B" ]; then \
		echo "  ✓ Correct! FewShotPromptTemplate is used for few-shot prompts."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is b) FewShotPromptTemplate"; \
	fi; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 3 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  How do examples help the model?"; \
	echo ""; \
	echo "    a) They reduce token usage"; \
	echo "    b) They make the model run faster"; \
	echo "    c) They show the model the pattern to follow and improve accuracy"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans3; \
	echo ""; \
	if [ "$$ans3" = "c" ] || [ "$$ans3" = "C" ]; then \
		echo "  ✓ Correct! Examples show patterns and improve model accuracy."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is c) They show patterns and improve accuracy"; \
	fi; \
	echo ""; \
	echo "======================================================================"; \
	echo "📊 Quiz Results"; \
	echo "======================================================================"; \
	echo ""; \
	echo "  Your score: $$score/3"; \
	echo ""; \
	if [ $$score -eq 3 ]; then \
		echo "  🎉 Perfect! You've mastered few-shot prompts!"; \
		echo "     You understand how to use examples to guide model behavior."; \
	elif [ $$score -eq 2 ]; then \
		echo "  👍 Great job! You have a good understanding of few-shot prompts."; \
		echo "     Review the concepts you missed and try again!"; \
	elif [ $$score -eq 1 ]; then \
		echo "  📚 Good start! You're on the right track."; \
		echo "     Review the README and examples to strengthen your understanding."; \
	else \
		echo "  📖 Don't worry! Learning takes time."; \
		echo "     Review the README and run 'make run' to see the example in action."; \
	fi; \
	echo ""

challenge: install
	@echo ""
	@echo "======================================================================"
	@echo "💻 Coding Challenge"
	@echo "======================================================================"
	@echo ""
	@echo "Your task: Complete the code in challenge.py"
	@echo "  - Replace the XXXX___ placeholders with the correct code"
	@echo "  - The challenge tests your understanding of few-shot prompts"
	@echo ""
	@echo "Steps:"
	@echo "  1. Open challenge.py in your editor"
	@echo "  2. Replace each XXXX___ with the correct code"
	@echo "  3. Run 'make challenge' again to test your solution"
	@echo ""
	@if [ ! -f challenge.py ]; then \
		echo "❌ Error: challenge.py not found!"; \
		exit 1; \
	fi
	@echo "Checking your solution..."
	@echo ""
	@if grep -q "XXXX___" challenge.py; then \
		echo "⚠️  You still have XXXX___ placeholders in your code."; \
		echo "   Please complete all the challenges first."; \
		echo ""; \
		echo "Hints:"; \
		echo "  - Look at few_shot_example.py for reference"; \
		echo "  - The first XXXX___ should be imports (PromptTemplate, FewShotPromptTemplate)"; \
		echo "  - The second XXXX___ should be a class name (PromptTemplate)"; \
		echo "  - The third XXXX___ should be a method name (from_template)"; \
		echo "  - The fourth XXXX___ should be a class name (FewShotPromptTemplate)"; \
		echo ""; \
		exit 1; \
	else \
		echo "✓ No placeholders found. Testing your solution..."; \
		echo ""; \
		$(PYTHON) challenge.py && echo "" && echo "🎉 Congratulations! Your solution works!" || echo "" && echo "❌ Your code has errors. Check the output above."; \
	fi

clean:
	@echo "Cleaning Python cache files and virtual environment..."
	@find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@if [ -d $(VENV) ]; then \
		rm -rf $(VENV); \
		echo "✓ Virtual environment removed"; \
	fi
	@echo "✓ Clean complete!"

