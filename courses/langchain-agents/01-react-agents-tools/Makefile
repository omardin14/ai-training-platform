include ../Makefile.common

.PHONY: help run all

help:
	@echo "ReAct Agents & Custom Tools - Makefile Commands"
	@echo "================================================"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup        - Create root .env file from template"
	@echo "  make venv         - Create virtual environment only"
	@echo "  make install      - Create venv and install all dependencies"
	@echo "  make run          - Run the ReAct agents & custom tools example"
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
	@echo "Running ReAct agents & custom tools example..."
	@if [ ! -f $(ROOT_DIR)/.env ] && [ -z "$$OPENAI_API_KEY" ]; then \
		echo "❌ Error: OPENAI_API_KEY not found. ReAct agents require an OpenAI API key."; \
		echo "   Please set OPENAI_API_KEY in your .env file or as an environment variable."; \
		echo ""; \
		exit 1; \
	fi
	@$(PYTHON) react_agent_tools_example.py

all: run
	@echo ""
	@echo "✓ All examples completed!"
