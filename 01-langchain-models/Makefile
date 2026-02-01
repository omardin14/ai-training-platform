.PHONY: help openai huggingface all install setup venv clean quiz challenge

# Virtual environment directory
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

help:
	@echo "LangChain Models Demo - Makefile Commands"
	@echo "=========================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup        - Create .env file from template"
	@echo "  make venv         - Create virtual environment only"
	@echo "  make install      - Create venv and install all dependencies"
	@echo "  make openai       - Run OpenAI examples"
	@echo "  make huggingface  - Run Hugging Face examples"
	@echo "  make quiz         - Take a quiz to test your knowledge"
	@echo "  make challenge    - Complete the coding challenge"
	@echo "  make all          - Run all examples"
	@echo "  make clean        - Clean Python cache files and virtual environment"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. Run 'make setup' to create .env file"
	@echo "  2. Edit .env and add your API keys"
	@echo "  3. Run 'make install' to set up virtual environment and install dependencies"
	@echo "  4. Run 'make all' to test examples"
	@echo ""

setup:
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		echo "# OpenAI API Key" > .env; \
		echo "# Get your key from: https://platform.openai.com/api-keys" >> .env; \
		echo "OPENAI_API_KEY=your-openai-api-key-here" >> .env; \
		echo "" >> .env; \
		echo "# Hugging Face Hub API Token (Optional)" >> .env; \
		echo "# Get your token from: https://huggingface.co/settings/tokens" >> .env; \
		echo "HUGGINGFACEHUB_API_TOKEN=your-huggingface-token-here" >> .env; \
		echo "✓ .env file created! Please edit it and add your API keys."; \
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

openai: install
	@echo "Running OpenAI examples..."
	@if [ ! -f .env ] && [ -z "$$OPENAI_API_KEY" ]; then \
		echo "⚠️  Warning: .env file not found and OPENAI_API_KEY not set"; \
		echo "   Run 'make setup' to create .env file, or set environment variable"; \
		echo ""; \
	fi
	@$(PYTHON) openai_example.py

huggingface: install
	@echo "Running Hugging Face examples..."
	@if [ -z "$$HUGGINGFACEHUB_API_TOKEN" ]; then \
		echo "⚠️  Note: HUGGINGFACEHUB_API_TOKEN not set"; \
		echo "   Hub API examples will be skipped, but local examples will run"; \
		echo ""; \
	fi
	@$(PYTHON) huggingface_example.py

all: openai huggingface
	@echo ""
	@echo "✓ All examples completed!"

quiz:
	@echo ""
	@echo "======================================================================"
	@echo "📝 LangChain Models Quiz"
	@echo "======================================================================"
	@echo ""
	@echo "Test your knowledge of LangChain models!"
	@echo "Answer each question by typing a, b, or c"
	@echo ""
	@score=0; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 1 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  What method is used to send a prompt to a LangChain model?"; \
	echo ""; \
	echo "    a) .call()"; \
	echo "    b) .invoke()"; \
	echo "    c) .run()"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans1; \
	echo ""; \
	if [ "$$ans1" = "b" ] || [ "$$ans1" = "B" ]; then \
		echo "  ✓ Correct! The .invoke() method is used to send prompts to models."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is b) .invoke()"; \
	fi; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 2 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  Which class is used to load OpenAI models in LangChain?"; \
	echo ""; \
	echo "    a) OpenAI"; \
	echo "    b) ChatOpenAI"; \
	echo "    c) GPTModel"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans2; \
	echo ""; \
	if [ "$$ans2" = "b" ] || [ "$$ans2" = "B" ]; then \
		echo "  ✓ Correct! ChatOpenAI is used for OpenAI chat models."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is b) ChatOpenAI"; \
	fi; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 3 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  What is a key advantage of using LangChain for models?"; \
	echo ""; \
	echo "    a) It provides a unified interface across different model providers"; \
	echo "    b) It makes models run faster"; \
	echo "    c) It reduces API costs"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans3; \
	echo ""; \
	if [ "$$ans3" = "a" ] || [ "$$ans3" = "A" ]; then \
		echo "  ✓ Correct! LangChain provides a unified interface for different providers."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is a) Unified interface across providers"; \
	fi; \
	echo ""; \
	echo "======================================================================"; \
	echo "📊 Quiz Results"; \
	echo "======================================================================"; \
	echo ""; \
	echo "  Your score: $$score/3"; \
	echo ""; \
	if [ $$score -eq 3 ]; then \
		echo "  🎉 Perfect! You've mastered LangChain models!"; \
		echo "     You understand how to work with different model providers."; \
	elif [ $$score -eq 2 ]; then \
		echo "  👍 Great job! You have a good understanding of LangChain models."; \
		echo "     Review the concepts you missed and try again!"; \
	elif [ $$score -eq 1 ]; then \
		echo "  📚 Good start! You're on the right track."; \
		echo "     Review the README and examples to strengthen your understanding."; \
	else \
		echo "  📖 Don't worry! Learning takes time."; \
		echo "     Review the README and run 'make all' to see the examples in action."; \
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
	@echo "  - The challenge tests your understanding of loading and using models"
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
		echo "  - Look at openai_example.py for reference"; \
		echo "  - The first XXXX___ should be a class name (ChatOpenAI)"; \
		echo "  - The second XXXX___ should be the same class name"; \
		echo "  - The third XXXX___ should be a method name (invoke)"; \
		echo "  - The fourth XXXX___ should be an attribute name (content)"; \
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

