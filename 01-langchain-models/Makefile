include ../Makefile.common

.PHONY: help run openai huggingface all

help:
	@echo "LangChain Models Demo - Makefile Commands"
	@echo "=========================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup        - Create root .env file from template"
	@echo "  make venv         - Create virtual environment only"
	@echo "  make install      - Create venv and install all dependencies"
	@echo "  make openai       - Run OpenAI examples"
	@echo "  make huggingface  - Run Hugging Face examples"
	@echo "  make learn        - Interactive learning tool (run from project root)"
	@echo "  make all          - Run all examples"
	@echo "  make clean        - Clean Python cache files and virtual environment"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. Run 'make setup' to create root .env file"
	@echo "  2. Edit ../.env and add your API keys"
	@echo "  3. Run 'make install' to set up virtual environment and install dependencies"
	@echo "  4. Run 'make all' to test examples"
	@echo ""

openai: install
	@echo "Running OpenAI examples..."
	@if [ ! -f ../.env ] && [ -z "$$OPENAI_API_KEY" ]; then \
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

run: all

all: openai huggingface
	@echo ""
	@echo "✓ All examples completed!"
