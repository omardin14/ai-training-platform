.PHONY: help run all install setup venv clean quiz challenge

# Virtual environment directory
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

help:
	@echo "LangChain Prompt Chains Demo - Makefile Commands"
	@echo "================================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup        - Create .env file from template"
	@echo "  make venv         - Create virtual environment only"
	@echo "  make install      - Create venv and install all dependencies"
	@echo "  make run          - Run the prompt chain example"
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
	@echo "Running prompt chain example..."
	@if [ ! -f .env ] && [ -z "$$OPENAI_API_KEY" ]; then \
		echo "⚠️  Note: .env file not found and OPENAI_API_KEY not set"; \
		echo "   The example will use Hugging Face model (may take time on first run)"; \
		echo ""; \
	fi
	@$(PYTHON) prompt_chain_example.py

all: run
	@echo ""
	@echo "✓ All examples completed!"

quiz:
	@echo ""
	@echo "======================================================================"
	@echo "📝 Prompt Chains Quiz"
	@echo "======================================================================"
	@echo ""
	@echo "Test your knowledge of prompt chains!"
	@echo "Answer each question by typing a, b, or c"
	@echo ""
	@score=0; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 1 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  What operator is used to chain prompt templates with models in LangChain?"; \
	echo ""; \
	echo "    a) + (plus)"; \
	echo "    b) | (pipe)"; \
	echo "    c) -> (arrow)"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans1; \
	echo ""; \
	if [ "$$ans1" = "b" ] || [ "$$ans1" = "B" ]; then \
		echo "  ✓ Correct! The pipe operator (|) is used to chain components."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is b) | (pipe)"; \
	fi; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 2 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  What method is used to invoke a chain with input variables?"; \
	echo ""; \
	echo "    a) .invoke()"; \
	echo "    b) .call()"; \
	echo "    c) .run()"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans2; \
	echo ""; \
	if [ "$$ans2" = "a" ] || [ "$$ans2" = "A" ]; then \
		echo "  ✓ Correct! The .invoke() method is used to run the chain."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is a) .invoke()"; \
	fi; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 3 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  In the code 'chain = prompt | llm', what does the pipe operator do?"; \
	echo ""; \
	echo "    a) It saves the prompt to a file"; \
	echo "    b) It formats the prompt and sends it to the model"; \
	echo "    c) It connects the prompt template with the LLM to create a chain"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans3; \
	echo ""; \
	if [ "$$ans3" = "c" ] || [ "$$ans3" = "C" ]; then \
		echo "  ✓ Correct! The pipe operator connects components to create a chain."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is c) It connects the prompt template with the LLM"; \
	fi; \
	echo ""; \
	echo "======================================================================"; \
	echo "📊 Quiz Results"; \
	echo "======================================================================"; \
	echo ""; \
	echo "  Your score: $$score/3"; \
	echo ""; \
	if [ $$score -eq 3 ]; then \
		echo "  🎉 Perfect! You've mastered prompt chains!"; \
		echo "     You understand how to use the pipe operator and create chains."; \
	elif [ $$score -eq 2 ]; then \
		echo "  👍 Great job! You have a good understanding of prompt chains."; \
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
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  💻 CODING CHALLENGE"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "  📄 File:  challenge.py"
	@echo "  📚 Topic: Prompt chains"
	@echo ""
	@echo "  Steps:"
	@echo "    1. Open challenge.py in your editor"
	@echo "    2. Replace each XXXX___ placeholder with the correct code"
	@echo "    3. Run 'make challenge' again to test your solution"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@if [ ! -f challenge.py ]; then \
		echo ""; \
		echo "  ❌ Error: challenge.py not found!"; \
		echo ""; \
		echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		exit 1; \
	fi
	@echo ""
	@echo "  Checking your solution..."
	@echo ""
	@if $(PYTHON) -c "import re,sys; code=open('challenge.py').read(); code=re.sub(r'\"\"\".*?\"\"\"','',code,flags=re.DOTALL); code='\n'.join(l for l in code.split('\n') if not l.strip().startswith('#')); sys.exit(0 if 'XXXX___' in code else 1)"; then \
		echo "  ⚠️  INCOMPLETE: You still have XXXX___ placeholders in your code."; \
		echo ""; \
		echo "  Hints:"; \
		echo "  - Look at prompt_chain_example.py for reference"; \
		echo "  - The first XXXX___ should be a method name (from_template)"; \
		echo "  - The second XXXX___ should be an operator (|)"; \
		echo "  - The third XXXX___ should be a method name (invoke)"; \
		echo ""; \
		echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		exit 1; \
	else \
		echo "  ✓ No placeholders found. Running your solution..."; \
		echo ""; \
		$(PYTHON) challenge.py && { echo ""; echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; echo "  ✅ PASSED - Your solution works!"; echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; } || { echo ""; echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; echo "  ❌ FAILED - Your code has errors. Check the output above."; echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; }; \
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

