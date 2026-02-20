include ../Makefile.common

NEO4J_CONTAINER := neo4j-langchain-training
NEO4J_PASSWORD := langchain-training
NEO4J_HTTP_PORT := 7474
NEO4J_BOLT_PORT := 7687

.PHONY: help run all setup-neo4j stop-neo4j neo4j-status

help:
	@echo "Neo4j Graph Store & Cypher Queries - Makefile Commands"
	@echo "======================================================"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup          - Create root .env file from template"
	@echo "  make venv           - Create virtual environment only"
	@echo "  make install        - Create venv and install all dependencies"
	@echo "  make setup-neo4j    - Start a local Neo4j database using Docker"
	@echo "  make stop-neo4j     - Stop and remove the Neo4j Docker container"
	@echo "  make neo4j-status   - Check if Neo4j is running"
	@echo "  make run            - Run the Neo4j graph store example"
	@echo "  make learn          - Interactive learning tool (run from project root)"
	@echo "  make all            - Run all examples"
	@echo "  make clean          - Clean Python cache files and virtual environment"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. Run 'make install' to install dependencies"
	@echo "  2. Run 'make setup-neo4j' to start a local Neo4j database"
	@echo "  3. Run 'make run' to see the example"
	@echo ""

setup-neo4j:
	@echo ""
	@echo "Setting up Neo4j with Docker..."
	@echo "================================"
	@if ! command -v docker >/dev/null 2>&1; then \
		echo ""; \
		echo "  Docker is not installed."; \
		echo ""; \
		echo "  To install Docker:"; \
		echo "    macOS:   brew install --cask docker  (or https://docker.com/products/docker-desktop)"; \
		echo "    Linux:   https://docs.docker.com/engine/install/"; \
		echo "    Windows: https://docs.docker.com/desktop/install/windows/"; \
		echo ""; \
		echo "  Alternatively, install Neo4j Desktop: https://neo4j.com/download/"; \
		echo "  Or use Neo4j Aura (free cloud): https://neo4j.com/cloud/aura/"; \
		echo ""; \
		exit 1; \
	fi
	@if docker ps -a --format '{{.Names}}' | grep -q '^$(NEO4J_CONTAINER)$$'; then \
		if docker ps --format '{{.Names}}' | grep -q '^$(NEO4J_CONTAINER)$$'; then \
			echo ""; \
			echo "  Neo4j is already running!"; \
			echo "  Web UI:  http://localhost:$(NEO4J_HTTP_PORT)"; \
			echo "  Bolt:    bolt://localhost:$(NEO4J_BOLT_PORT)"; \
			echo ""; \
		else \
			echo "  Starting existing container..."; \
			docker start $(NEO4J_CONTAINER); \
			echo ""; \
			echo "  Neo4j started!"; \
			echo "  Web UI:  http://localhost:$(NEO4J_HTTP_PORT)"; \
			echo "  Bolt:    bolt://localhost:$(NEO4J_BOLT_PORT)"; \
			echo ""; \
		fi \
	else \
		echo "  Pulling and starting Neo4j..."; \
		echo ""; \
		docker run -d \
			--name $(NEO4J_CONTAINER) \
			-p $(NEO4J_HTTP_PORT):7474 \
			-p $(NEO4J_BOLT_PORT):7687 \
			-e NEO4J_AUTH=neo4j/$(NEO4J_PASSWORD) \
			-e NEO4J_PLUGINS='["apoc"]' \
			neo4j:latest; \
		echo ""; \
		echo "  Neo4j is starting up (may take 10-15 seconds)..."; \
		echo ""; \
		echo "  Connection details:"; \
		echo "    Web UI:   http://localhost:$(NEO4J_HTTP_PORT)"; \
		echo "    Bolt URL: bolt://localhost:$(NEO4J_BOLT_PORT)"; \
		echo "    Username: neo4j"; \
		echo "    Password: $(NEO4J_PASSWORD)"; \
		echo ""; \
		echo "  Add these to your .env file:"; \
		echo "    NEO4J_URI=bolt://localhost:$(NEO4J_BOLT_PORT)"; \
		echo "    NEO4J_USERNAME=neo4j"; \
		echo "    NEO4J_PASSWORD=$(NEO4J_PASSWORD)"; \
		echo ""; \
	fi

stop-neo4j:
	@echo ""
	@echo "Stopping Neo4j..."
	@if docker ps -a --format '{{.Names}}' | grep -q '^$(NEO4J_CONTAINER)$$'; then \
		docker stop $(NEO4J_CONTAINER) >/dev/null 2>&1 || true; \
		docker rm $(NEO4J_CONTAINER) >/dev/null 2>&1 || true; \
		echo "  Neo4j stopped and container removed."; \
	else \
		echo "  No Neo4j container found."; \
	fi
	@echo ""

neo4j-status:
	@echo ""
	@if docker ps --format '{{.Names}}' 2>/dev/null | grep -q '^$(NEO4J_CONTAINER)$$'; then \
		echo "  Neo4j is RUNNING"; \
		echo "  Web UI:  http://localhost:$(NEO4J_HTTP_PORT)"; \
		echo "  Bolt:    bolt://localhost:$(NEO4J_BOLT_PORT)"; \
	elif docker ps -a --format '{{.Names}}' 2>/dev/null | grep -q '^$(NEO4J_CONTAINER)$$'; then \
		echo "  Neo4j container exists but is STOPPED"; \
		echo "  Run 'make setup-neo4j' to start it"; \
	else \
		echo "  Neo4j is NOT SET UP"; \
		echo "  Run 'make setup-neo4j' to start a local instance"; \
	fi
	@echo ""

run: install
	@echo "Running Neo4j graph store example..."
	@$(PYTHON) neo4j_graph_store_example.py

all: run
	@echo ""
	@echo "All examples completed!"
