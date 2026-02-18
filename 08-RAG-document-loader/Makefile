include ../Makefile.common

.PHONY: help run all quiz challenge

help:
	@echo "LangChain Document Loaders Demo - Makefile Commands"
	@echo "==================================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup        - Create root .env file from template"
	@echo "  make venv         - Create virtual environment only"
	@echo "  make install      - Create venv and install all dependencies"
	@echo "  make run          - Run the document loader example"
	@echo "  make quiz         - Take a quiz to test your knowledge"
	@echo "  make challenge    - Complete the coding challenge"
	@echo "  make all          - Run all examples"
	@echo "  make clean        - Clean Python cache files and virtual environment"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. Run 'make setup' to create root .env file (optional)"
	@echo "  2. Run 'make install' to set up virtual environment and install dependencies"
	@echo "  3. Run 'make run' to see the example"
	@echo ""

run: install
	@echo "Running document loader example..."
	@$(PYTHON) document_loader_example.py

all: run
	@echo ""
	@echo "✓ All examples completed!"

quiz:
	@echo ""
	@echo "======================================================================"
	@echo "📝 Document Loaders Quiz"
	@echo "======================================================================"
	@echo ""
	@echo "Test your knowledge of document loaders!"
	@echo "Answer each question by typing a, b, or c"
	@echo ""
	@score=0; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 1 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  What does a document loader return?"; \
	echo ""; \
	echo "    a) A list of Document objects with page_content and metadata"; \
	echo "    b) A string containing the file content"; \
	echo "    c) A dictionary with file information"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans1; \
	echo ""; \
	if [ "$$ans1" = "a" ] || [ "$$ans1" = "A" ]; then \
		echo "  ✓ Correct! Document loaders return Document objects with content and metadata."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is a) Document objects"; \
	fi; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 2 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  Which loader would you use for a PDF file?"; \
	echo ""; \
	echo "    a) TextLoader"; \
	echo "    b) PyPDFLoader"; \
	echo "    c) CSVLoader"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans2; \
	echo ""; \
	if [ "$$ans2" = "b" ] || [ "$$ans2" = "B" ]; then \
		echo "  ✓ Correct! PyPDFLoader is used for PDF files."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is b) PyPDFLoader"; \
	fi; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "  Question 3 of 3"; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo ""; \
	echo "  What is the main purpose of document loaders in RAG applications?"; \
	echo ""; \
	echo "    a) To train models on new data"; \
	echo "    b) To extract text content from files for retrieval and generation"; \
	echo "    c) To compress documents"; \
	echo ""; \
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	read -p "  Your answer (a/b/c): " ans3; \
	echo ""; \
	if [ "$$ans3" = "b" ] || [ "$$ans3" = "B" ]; then \
		echo "  ✓ Correct! Document loaders extract text for RAG applications."; \
		score=$$((score + 1)); \
	else \
		echo "  ✗ Incorrect. The correct answer is b) Extract text for RAG"; \
	fi; \
	echo ""; \
	echo "======================================================================"; \
	echo "📊 Quiz Results"; \
	echo "======================================================================"; \
	echo ""; \
	echo "  Your score: $$score/3"; \
	echo ""; \
	if [ $$score -eq 3 ]; then \
		echo "  🎉 Perfect! You've mastered document loaders!"; \
		echo "     You understand how to load documents from various sources."; \
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
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  💻 CODING CHALLENGE"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "  📄 File:  challenge.py"
	@echo "  📚 Topic: Document loaders"
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
		echo "  - Look at document_loader_example.py for reference"; \
		echo "  - The first XXXX___ should be an import (PyPDFLoader)"; \
		echo "  - The second XXXX___ should be a class name (PyPDFLoader)"; \
		echo "  - The third XXXX___ should be a method name (load)"; \
		echo ""; \
		echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		exit 1; \
	else \
		echo "  ✓ No placeholders found. Running your solution..."; \
		echo ""; \
		$(PYTHON) challenge.py && { echo ""; echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; echo "  ✅ PASSED - Your solution works!"; echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; } || { echo ""; echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; echo "  ❌ FAILED - Your code has errors. Check the output above."; echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; }; \
	fi
