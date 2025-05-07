.PHONY: help setup test lint docs clean verify dev-env

# Colors
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

# Help target
help: ## Show this help
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  ${YELLOW}%-15s${RESET} %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Set up development environment
	@echo "${YELLOW}Setting up development environment...${RESET}"
	./setup-dev-env
	@echo "${GREEN}Setup complete! Run 'source .venv/bin/activate' to activate the virtual environment${RESET}"

test: ## Run tests
	@echo "${YELLOW}Running tests...${RESET}"
	./dev-tools test

test-watch: ## Run tests in watch mode
	@echo "${YELLOW}Running tests in watch mode...${RESET}"
	./dev-tools test -w

test-cov: ## Run tests with coverage
	@echo "${YELLOW}Running tests with coverage...${RESET}"
	./dev-tools test -c

lint: ## Run all linting tools
	@echo "${YELLOW}Running linting tools...${RESET}"
	./dev-tools lint

docs: ## Build documentation
	@echo "${YELLOW}Building documentation...${RESET}"
	./dev-tools docs

docs-serve: ## Serve documentation locally
	@echo "${YELLOW}Starting documentation server...${RESET}"
	./dev-tools docs -s

clean: ## Clean up development artifacts
	@echo "${YELLOW}Cleaning up development artifacts...${RESET}"
	./dev-tools clean

verify: ## Verify development environment
	@echo "${YELLOW}Verifying development environment...${RESET}"
	./dev-tools verify

dev-env: ## Activate development environment (run with source)
	@echo "${YELLOW}Activating development environment...${RESET}"
	@echo "Please run: ${GREEN}source .venv/bin/activate${RESET}"

check: lint test ## Run linting and tests

all: setup lint test docs ## Set up environment and run all checks

# Development workflow shortcuts
.PHONY: format type-check security-check

format: ## Format code with black
	@echo "${YELLOW}Formatting code...${RESET}"
	black src tests

type-check: ## Run type checking
	@echo "${YELLOW}Running type checks...${RESET}"
	mypy src

security-check: ## Run security checks
	@echo "${YELLOW}Running security checks...${RESET}"
	bandit -r src/

# Quick development tasks
.PHONY: quick-test quick-lint

quick-test: ## Run only fast tests
	@echo "${YELLOW}Running quick tests...${RESET}"
	pytest -m "not slow" tests/

quick-lint: ## Run quick linting checks
	@echo "${YELLOW}Running quick lint...${RESET}"
	black --check src tests
	mypy --no-incremental src

# Docker specific tasks
.PHONY: docker-build docker-run docker-test docker-dev docker-lint docker-clean

docker-build: ## Build the Docker image
	docker-compose build

docker-run: docker-build ## Run the network discovery tool (use ARGS='192.168.1.0/24' to pass arguments)
	docker-compose run --rm network-discovery $(ARGS)

docker-test: docker-build ## Run tests in Docker (use ARGS='tests/test_scanner.py' to specify tests)
	docker-compose run --rm test $(ARGS)

docker-dev: docker-build ## Start a development shell in Docker
	docker-compose run --rm dev

docker-lint: docker-build ## Run linters in Docker
	docker-compose run --rm dev bash -c "flake8 src tests && black src tests && isort src tests && mypy src tests"

docker-clean: ## Clean up Docker resources
	docker-compose down --rmi local
	rm -rf output/*.html output/*.csv output/*.xlsx output/*.json
	rm -rf devices.json
	rm -rf __pycache__ .pytest_cache
	find . -name "*.pyc" -delete