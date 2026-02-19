include ../Makefile.common

.PHONY: help run all

help:
	@echo "LangChain Document Splitters Demo - Makefile Commands"
	@echo "====================================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup        - Create root .env file from template"
	@echo "  make venv         - Create virtual environment only"
	@echo "  make install      - Create venv and install all dependencies"
	@echo "  make run          - Run the document splitter example"
	@echo "  make learn        - Interactive learning tool (run from project root)"
	@echo "  make all          - Run all examples"
	@echo "  make clean        - Clean Python cache files and virtual environment"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. Run 'make setup' to create root .env file (optional)"
	@echo "  2. Run 'make install' to set up virtual environment and install dependencies"
	@echo "  3. Run 'make run' to see the example"
	@echo ""

run: install
	@echo "Running document splitter example..."
	@$(PYTHON) document_splitter_example.py

all: run
	@echo ""
	@echo "✓ All examples completed!"
