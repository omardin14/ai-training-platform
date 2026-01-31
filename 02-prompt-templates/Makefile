.PHONY: help run all install setup venv clean

# Virtual environment directory
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

help:
	@echo "LangChain Prompt Templates Demo - Makefile Commands"
	@echo "===================================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup        - Create .env file from template"
	@echo "  make venv         - Create virtual environment only"
	@echo "  make install      - Create venv and install all dependencies"
	@echo "  make run          - Run the prompt template example"
	@echo "  make all          - Run all examples"
	@echo "  make clean        - Clean Python cache files and virtual environment"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. Run 'make setup' to create .env file"
	@echo "  2. Edit .env and add your API keys"
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
	@echo "Running prompt template example..."
	@if [ ! -f .env ] && [ -z "$$OPENAI_API_KEY" ]; then \
		echo "⚠️  Warning: .env file not found and OPENAI_API_KEY not set"; \
		echo "   Run 'make setup' to create .env file, or set environment variable"; \
		echo ""; \
	fi
	@$(PYTHON) prompt_template_example.py

all: run
	@echo ""
	@echo "✓ All examples completed!"

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

