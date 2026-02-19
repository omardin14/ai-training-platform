include ../Makefile.common

.PHONY: help run all

help:
	@echo "LangChain Markdown and Python Loaders Demo - Makefile Commands"
	@echo "=============================================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup        - Create root .env file from template"
	@echo "  make venv         - Create virtual environment only"
	@echo "  make install      - Create venv and install all dependencies"
	@echo "  make run          - Run the markdown and Python loader example"
	@echo "  make learn        - Interactive learning tool (run from project root)"
	@echo "  make all          - Run all examples"
	@echo "  make clean        - Clean Python cache files and virtual environment"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. Run 'make setup' to create root .env file"
	@echo "  2. Edit ../.env and add your OpenAI API key (required)"
	@echo "  3. Run 'make install' to set up virtual environment and install dependencies"
	@echo "  4. Run 'make run' to see the example"
	@echo ""

run: install
	@echo "Running markdown and Python loader example..."
	@if [ ! -f ../.env ] && [ -z "$$OPENAI_API_KEY" ]; then \
		echo "⚠️  Note: .env file not found and OPENAI_API_KEY not set"; \
		echo "   This module requires an OpenAI API key."; \
		echo "   Run 'make setup' to create .env file, then add your API key."; \
		echo ""; \
	fi
	@$(PYTHON) python_markdown_example.py

all: run
	@echo ""
	@echo "✓ All examples completed!"
