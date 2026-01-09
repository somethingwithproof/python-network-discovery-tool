# Variables
PROJECT_NAME := auto-discover
VENV_NAME := .venv
PYTHON := $(VENV_NAME)/bin/python
PIP := $(VENV_NAME)/bin/pip

# Targets
.PHONY: clean-pyc clean-build clean-venv docs test lint install install-dev help

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  install       to install dependencies"
	@echo "  install-dev   to install development dependencies"
	@echo "  clean         to remove all build artifacts"
	@echo "  clean-build   to remove build artifacts"
	@echo "  clean-pyc     to remove Python file artifacts"
	@echo "  clean-venv    to remove the virtual environment"
	@echo "  lint          to check style with flake8"
	@echo "  test          to run tests"
	@echo "  docs          to generate documentation"

clean: clean-build clean-pyc

clean-all: clean clean-venv

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean-pyc:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete
	find . -name '__pycache__' -delete

clean-venv:
	rm -rf $(VENV_NAME)

$(VENV_NAME):
	python3 -m venv $(VENV_NAME)
	$(PIP) install -U pip

install: $(VENV_NAME)
	$(PIP) install -r requirements.txt

install-dev: $(VENV_NAME)
	$(PIP) install -e ".[dev]"

lint:
	$(VENV_NAME)/bin/flake8 *.py

test:
	$(PYTHON) -m pytest tests/

docs:
	cd docs && mkdocs build
