.PHONY: help run all install setup venv clean quiz challenge

# Virtual environment directory
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

help:
	@echo "LangChain Markdown and Python Loaders Demo - Makefile Commands"
	@echo "=============================================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup        - Create .env file from template"
	@echo "  make venv         - Create virtual environment only"
	@echo "  make install      - Create venv and install all dependencies"
	@echo "  make run          - Run the markdown and Python loader example"
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
		else \
			echo "Creating .env file from template..."; \
			echo "# OpenAI API Key (Required)" > .env; \
			echo "# Get your key from: https://platform.openai.com/api-keys" >> .env; \
			echo "OPENAI_API_KEY=your-openai-api-key-here" >> .env; \
			echo "✓ .env file created! Please edit it and add your OpenAI API key."; \
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
	@echo "Running markdown and Python loader example..."
	@if [ ! -f .env ] && [ -z "$$OPENAI_API_KEY" ]; then \
		echo "⚠️  Note: .env file not found and OPENAI_API_KEY not set"; \
		echo "   This module requires an OpenAI API key."; \
		echo "   Run 'make setup' to create .env file, then add your API key."; \
		echo ""; \
	fi
	@$(PYTHON) python_markdown_example.py

all: run
	@echo ""
	@echo "✓ All examples completed!"

quiz:
	@echo ""
	@echo "======================================================================"
	@echo "📝 Markdown and Python Loaders Quiz"
	@echo "======================================================================"
	@echo ""
	@echo "Test your knowledge of Markdown and Python document loaders!"
	@echo "Answer each question by typing a, b, or c"
	@echo ""
	@score=0; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 1 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  What loader is used to load Markdown files?"; \
	echo ""; \
	echo "    a) MarkdownLoader"; \
	echo "    b) TextLoader"; \
	echo "    c) UnstructuredMarkdownLoader"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans1; \
	echo ""; \
	if [ "$$ans1" = "c" ] || [ "$$ans1" = "C" ]; then \
		echo "  ✓ Correct! UnstructuredMarkdownLoader is used for Markdown files."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is c) UnstructuredMarkdownLoader"; \
	fi; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 2 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  What is the best way to split Python code files?"; \
	echo ""; \
	echo "    a) CharacterTextSplitter"; \
	echo "    b) Simple split by lines"; \
	echo "    c) RecursiveCharacterTextSplitter.from_language(Language.PYTHON)"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans2; \
	echo ""; \
	if [ "$$ans2" = "c" ] || [ "$$ans2" = "C" ]; then \
		echo "  ✓ Correct! Use RecursiveCharacterTextSplitter.from_language() for code."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is c) RecursiveCharacterTextSplitter.from_language()"; \
	fi; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 3 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  What loader is used to load Python source files?"; \
	echo ""; \
	echo "    a) PythonFileLoader"; \
	echo "    b) CodeLoader"; \
	echo "    c) PythonLoader"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans3; \
	echo ""; \
	if [ "$$ans3" = "c" ] || [ "$$ans3" = "C" ]; then \
		echo "  ✓ Correct! PythonLoader is used for Python source files."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is c) PythonLoader"; \
	fi; \
	echo ""; \
	echo "======================================================================"; \
	echo "📊 Quiz Results"; \
	echo "======================================================================"; \
	echo ""; \
	echo "  Your score: $$score/3"; \
	echo ""; \
	if [ $$score -eq 3 ]; then \
		echo "  🎉 Perfect! You've mastered Markdown and Python loaders!"; \
		echo "     You understand how to load and split code and documentation."; \
	elif [ $$score -eq 2 ]; then \
		echo "  👍 Great job! You have a good understanding of document loaders."; \
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
	@echo "  - The challenge tests your understanding of Markdown and Python loaders"
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
		echo "  - Look at python_markdown_example.py for reference"; \
		echo "  - The first XXXX___ should be an import (UnstructuredMarkdownLoader)"; \
		echo "  - The second XXXX___ should be a method name (load)"; \
		echo "  - The third XXXX___ should be an import (PythonLoader)"; \
		echo "  - The fourth XXXX___ should be an import (RecursiveCharacterTextSplitter)"; \
		echo "  - The fifth XXXX___ should be an import (Language)"; \
		echo "  - The sixth XXXX___ should be a method name (from_language)"; \
		echo "  - The seventh XXXX___ should be Language.PYTHON"; \
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
