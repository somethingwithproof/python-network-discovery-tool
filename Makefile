.PHONY: install test lint lab-up lab-down test-integration demo clean

LAB = docker compose -f tests/integration/compose.yml --profile tester

install:
	uv pip install -e ".[dev]"

test:
	uv run pytest --cov=netprobe --cov-report=term-missing

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy

lab-up:
	$(LAB) up -d --build --wait ssh db snmp quiet

lab-down:
	$(LAB) down -v

# Runs inside the lab network so container IPs are reachable on any Docker host.
test-integration:
	$(LAB) run --rm --build tester pytest -m integration -v -p no:cacheprovider

demo:
	$(LAB) run --rm --build tester python -m netprobe scan 172.30.57.8/29

clean:
	rm -rf .pytest_cache htmlcov .coverage
	$(LAB) down -v 2>/dev/null || true
