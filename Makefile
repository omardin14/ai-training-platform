.PHONY: help run quiz challenge clean setup install list learn

MODULES = \
  01-langchain-models \
  02-prompt-templates \
  03-prompt-chains \
  04-few-shot-prompts \
  05-sequential-chain \
  06-ReAct-agents \
  07-custom-agent-tools \
  08-RAG-document-loader \
  09-RAG-document-splitter \
  10-RAG-document-storage \
  11-lcel-retrival-chain \
  12-RAG-python-markdown \
  13-advanced-splitting \
  14-advanced-retrieval \
  15-rag-evaluation

NUM_MODULES := $(words $(MODULES))

# Resolve M=01 → full directory name
ifdef M
  MODULE_DIR := $(strip $(firstword $(filter $(M)-%,$(MODULES)) $(filter $(M),$(MODULES))))
  ifeq ($(MODULE_DIR),)
    $(error No module matching "$(M)". Run 'make list' to see available modules.)
  endif
endif

help:
ifdef M
	@$(MAKE) --no-print-directory -C $(MODULE_DIR) help
else
	@echo "LangChain Training - Root Makefile"
	@echo "=================================="
	@echo ""
	@echo "Usage:"
	@echo "  make learn            - Interactive learning tool (lessons, quizzes, challenges, examples)"
	@echo ""
	@echo "  make run M=01         - Run module 01 examples directly"
	@echo "  make setup            - Create .env file from template"
	@echo "  make install M=01     - Install dependencies for module 01"
	@echo "  make clean M=01       - Clean module 01"
	@echo "  make list             - Show all available modules"
	@echo ""
endif

run quiz challenge clean install:
	@if [ -z "$(MODULE_DIR)" ]; then \
		echo ""; \
		echo "Select a module:"; \
		echo ""; \
		i=1; \
		for m in $(MODULES); do \
			printf "  %2d) %s\n" $$i "$$m"; \
			i=$$((i + 1)); \
		done; \
		echo ""; \
		read -p "Enter number (1-$(NUM_MODULES)): " choice; \
		i=1; \
		selected=""; \
		for m in $(MODULES); do \
			if [ $$i -eq "$$choice" ] 2>/dev/null; then \
				selected=$$m; \
			fi; \
			i=$$((i + 1)); \
		done; \
		if [ -z "$$selected" ]; then \
			echo "Invalid selection."; \
			exit 1; \
		fi; \
		echo ""; \
		$(MAKE) --no-print-directory -C "$$selected" $@; \
	else \
		$(MAKE) --no-print-directory -C $(MODULE_DIR) $@; \
	fi

setup:
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		cp .env.example .env; \
		echo "✓ .env file created at project root!"; \
		echo "  Edit .env and add your API keys."; \
	else \
		echo "✓ .env file already exists."; \
	fi

list:
	@echo ""
	@echo "Available modules:"
	@echo ""
	@i=1; \
	for m in $(MODULES); do \
		printf "  %2d) %s\n" $$i "$$m"; \
		i=$$((i + 1)); \
	done
	@echo ""
	@echo "Usage: make run M=01  (or any module number/name)"
	@echo ""

learn:
	@if [ ! -d venv ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv venv; \
	fi
	@venv/bin/pip install -q -r requirements.txt 2>/dev/null
	@venv/bin/python learn.py
