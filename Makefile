.PHONY: help test test-unit test-e2e test-all docker-up docker-down docker-logs lint format install clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:
	pip install -e ".[dev]"

test-unit:
	pytest tests -v

test-e2e:
	@echo "🐳 Starting Docker test environment..."
	docker-compose -f docker-compose.test.yml up -d
	@echo "⏳ Waiting for services..."
	@sleep 20
	@echo "🧪 Running E2E tests..."
	pytest test_e2e.py -v -m e2e || (docker-compose -f docker-compose.test.yml down && exit 1)
	@echo "🧹 Cleaning up..."
	docker-compose -f docker-compose.test.yml down

test-all:
	pytest tests test_e2e.py -v

test:
	pytest -v --cov=netprobe --cov-report=html

docker-up:
	docker-compose -f docker-compose.test.yml up -d
	@sleep 20
	@echo "✅ Test services ready at 172.20.0.10-14"

docker-down:
	docker-compose -f docker-compose.test.yml down

clean:
	rm -rf .pytest_cache htmlcov .coverage __pycache__
	docker-compose -f docker-compose.test.yml down 2>/dev/null || true

demo:
	@make docker-up
	python -m netprobe scan 172.20.0.0/28
	@make docker-down
