.PHONY: help run all install setup venv clean quiz challenge

# Virtual environment directory
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

help:
	@echo "LangChain Document Storage Demo - Makefile Commands"
	@echo "==================================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup        - Create .env file from template"
	@echo "  make venv         - Create virtual environment only"
	@echo "  make install      - Create venv and install all dependencies"
	@echo "  make run          - Run the document storage example"
	@echo "  make quiz         - Take a quiz to test your knowledge"
	@echo "  make challenge    - Complete the coding challenge"
	@echo "  make all          - Run all examples"
	@echo "  make clean        - Clean Python cache files and virtual environment"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. Run 'make setup' to create .env file (optional but recommended)"
	@echo "  2. Edit .env and add your OpenAI API key (optional, uses Hugging Face if not set)"
	@echo "  3. Run 'make install' to set up virtual environment and install dependencies"
	@echo "  4. Run 'make run' to see the example"
	@echo ""

setup:
	@if [ ! -f .env ]; then \
		if [ -f .env.example ]; then \
			echo "Creating .env file from .env.example..."; \
			cp .env.example .env; \
			echo "✓ .env file created from .env.example!"; \
			echo "  Edit .env and add your OpenAI API key (optional, uses Hugging Face if not set)."; \
		else \
			echo "Creating .env file from template..."; \
			echo "# OpenAI API Key (Optional but recommended)" > .env; \
			echo "# Get your key from: https://platform.openai.com/api-keys" >> .env; \
			echo "# If not set, will use Hugging Face embeddings" >> .env; \
			echo "OPENAI_API_KEY=your-openai-api-key-here" >> .env; \
			echo "✓ .env file created! Please edit it and add your API key (optional)."; \
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
	@echo "Running document storage example..."
	@if [ ! -f .env ] && [ -z "$$OPENAI_API_KEY" ]; then \
		echo "⚠️  Note: .env file not found and OPENAI_API_KEY not set"; \
		echo "   Will use Hugging Face embeddings (OpenAI recommended for best results)"; \
		echo ""; \
	fi
	@$(PYTHON) document_storage_example.py

all: run
	@echo ""
	@echo "✓ All examples completed!"

quiz:
	@echo ""
	@echo "======================================================================"
	@echo "📝 Document Storage Quiz"
	@echo "======================================================================"
	@echo ""
	@echo "Test your knowledge of document storage with vector databases!"
	@echo "Answer each question by typing a, b, or c"
	@echo ""
	@score=0; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 1 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  What is the purpose of embeddings in vector databases?"; \
	echo ""; \
	echo "    a) To compress documents"; \
	echo "    b) To convert text into numerical vectors that capture semantic meaning"; \
	echo "    c) To encrypt documents"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans1; \
	echo ""; \
	if [ "$$ans1" = "b" ] || [ "$$ans1" = "B" ]; then \
		echo "  ✓ Correct! Embeddings convert text to vectors for semantic search."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is b) Convert text to vectors"; \
	fi; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 2 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  What is the main purpose of storing documents in a vector database?"; \
	echo ""; \
	echo "    a) To compress documents"; \
	echo "    b) To enable semantic search and retrieval of similar documents"; \
	echo "    c) To encrypt documents"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans2; \
	echo ""; \
	if [ "$$ans2" = "b" ] || [ "$$ans2" = "B" ]; then \
		echo "  ✓ Correct! Vector databases enable semantic search and retrieval."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is b) Enable semantic search and retrieval"; \
	fi; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 3 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  What is Chroma?"; \
	echo ""; \
	echo "    a) A programming language"; \
	echo "    b) A vector database for storing embeddings"; \
	echo "    c) A text editor"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans3; \
	echo ""; \
	if [ "$$ans3" = "b" ] || [ "$$ans3" = "B" ]; then \
		echo "  ✓ Correct! Chroma is a lightweight vector database."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is b) A vector database"; \
	fi; \
	echo ""; \
	echo "======================================================================"; \
	echo "📊 Quiz Results"; \
	echo "======================================================================"; \
	echo ""; \
	echo "  Your score: $$score/3"; \
	echo ""; \
	if [ $$score -eq 3 ]; then \
		echo "  🎉 Perfect! You've mastered document storage!"; \
		echo "     You understand how to store documents in vector databases."; \
	elif [ $$score -eq 2 ]; then \
		echo "  👍 Great job! You have a good understanding of document storage."; \
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
	@echo "  📚 Topic: Document storage"
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
		echo "  - Look at document_storage_example.py for reference"; \
		echo "  - The first XXXX___ should be an import (OpenAIEmbeddings or HuggingFaceEmbeddings)"; \
		echo "  - The second XXXX___ should be a class name (Chroma)"; \
		echo "  - The third XXXX___ should be a method name (from_documents)"; \
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
	@if [ -d chroma_db ]; then \
		rm -rf chroma_db; \
		echo "✓ Vector database directory removed"; \
	fi
	@if [ -d $(VENV) ]; then \
		rm -rf $(VENV); \
		echo "✓ Virtual environment removed"; \
	fi
	@echo "✓ Clean complete!"

