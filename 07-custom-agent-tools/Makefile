.PHONY: help run all install setup venv clean quiz challenge

# Virtual environment directory
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

help:
	@echo "LangChain Custom Tools Demo - Makefile Commands"
	@echo "================================================"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup        - Create .env file from template"
	@echo "  make venv         - Create virtual environment only"
	@echo "  make install      - Create venv and install all dependencies"
	@echo "  make run          - Run the custom tools example"
	@echo "  make quiz         - Take a quiz to test your knowledge"
	@echo "  make challenge    - Complete the coding challenge"
	@echo "  make all          - Run all examples"
	@echo "  make clean        - Clean Python cache files and virtual environment"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. Run 'make setup' to create .env file"
	@echo "  2. Edit .env and add your OpenAI API key (required)"
	@echo "  3. Run 'make install' to set up virtual environment and install dependencies"
	@echo "  4. Run 'make run' to see the example"
	@echo ""

setup:
	@if [ ! -f .env ]; then \
		if [ -f .env.example ]; then \
			echo "Creating .env file from .env.example..."; \
			cp .env.example .env; \
			echo "✓ .env file created from .env.example!"; \
			echo "  Edit .env and add your OpenAI API key (required for ReAct agents)."; \
		else \
			echo "Creating .env file from template..."; \
			echo "# OpenAI API Key (Required for ReAct agents)" > .env; \
			echo "# Get your key from: https://platform.openai.com/api-keys" >> .env; \
			echo "OPENAI_API_KEY=your-openai-api-key-here" >> .env; \
			echo "✓ .env file created! Please edit it and add your API key."; \
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
	@echo "Running custom tools example..."
	@if [ ! -f .env ] && [ -z "$$OPENAI_API_KEY" ]; then \
		echo "❌ Error: OPENAI_API_KEY not found. ReAct agents require an OpenAI API key."; \
		echo "   Please set OPENAI_API_KEY in your .env file or as an environment variable."; \
		echo ""; \
		exit 1; \
	fi
	@$(PYTHON) custom_tool_example.py

all: run
	@echo ""
	@echo "✓ All examples completed!"

quiz:
	@echo ""
	@echo "======================================================================"
	@echo "📝 Custom Tools Quiz"
	@echo "======================================================================"
	@echo ""
	@echo "Test your knowledge of custom tools!"
	@echo "Answer each question by typing a, b, or c"
	@echo ""
	@score=0; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 1 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  What decorator is used to convert a function into a tool?"; \
	echo ""; \
	echo "    a) @tool"; \
	echo "    b) @function"; \
	echo "    c) @agent"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans1; \
	echo ""; \
	if [ "$$ans1" = "a" ] || [ "$$ans1" = "A" ]; then \
		echo "  ✓ Correct! The @tool decorator converts functions into tools."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is a) @tool"; \
	fi; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 2 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  What is used by the LLM to decide when to call a custom tool?"; \
	echo ""; \
	echo "    a) The tool's name"; \
	echo "    b) The tool's description (docstring)"; \
	echo "    c) The tool's arguments"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans2; \
	echo ""; \
	if [ "$$ans2" = "b" ] || [ "$$ans2" = "B" ]; then \
		echo "  ✓ Correct! The tool's description helps the LLM decide when to use it."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is b) The tool's description"; \
	fi; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 3 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  What are the key attributes of a custom tool?"; \
	echo ""; \
	echo "    a) name, description, and args"; \
	echo "    b) name, type, and value"; \
	echo "    c) function, decorator, and result"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans3; \
	echo ""; \
	if [ "$$ans3" = "a" ] || [ "$$ans3" = "A" ]; then \
		echo "  ✓ Correct! Tools have name, description, and args attributes."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is a) name, description, and args"; \
	fi; \
	echo ""; \
	echo "======================================================================"; \
	echo "📊 Quiz Results"; \
	echo "======================================================================"; \
	echo ""; \
	echo "  Your score: $$score/3"; \
	echo ""; \
	if [ $$score -eq 3 ]; then \
		echo "  🎉 Perfect! You've mastered custom tools!"; \
		echo "     You understand how to create and use custom tools with agents."; \
	elif [ $$score -eq 2 ]; then \
		echo "  👍 Great job! You have a good understanding of custom tools."; \
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
	@echo "  - The challenge tests your understanding of custom tools"
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
		echo "  - Look at custom_tool_example.py for reference"; \
		echo "  - The first XXXX___ should be an import (@tool decorator)"; \
		echo "  - The second XXXX___ should be the decorator name (@tool)"; \
		echo "  - The third XXXX___ should be an import (create_react_agent)"; \
		echo "  - The fourth XXXX___ should be a function name (create_react_agent)"; \
		echo "  - The fifth XXXX___ should be a method name (invoke)"; \
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

