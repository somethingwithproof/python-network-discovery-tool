# Variables
PROJECT_NAME := auto-discover
VENV_NAME := $(PROJECT_NAME)-venv
FLAKE8_EXECUTABLE := flake8

# Targets
.PHONY: clean-pyc clean-build clean-venv lint test docs help

help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  clean-build   to remove build artifacts"
	@echo "  clean-pyc     to remove Python file artifacts"
	@echo "  clean-venv    to remove the virtual environment"
	@echo "  lint          to check style with flake8"
	@echo "  test          to run tests"
	@echo "  docs          to generate Sphinx HTML documentation, including API docs"

clean: clean-build clean-pyc clean-venv

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean-pyc:
	find . -name '*.pyc' -delete -o -name '*.pyo' -delete -o -name '*~' -delete -o -name '__pycache__' -delete -print0 | xargs -0 -P4 rm -f

clean-venv:
	rm -rf $(VENV_NAME)

lint:
	$(FLAKE8_EXECUTABLE) auto-discover tests

test:
	python -m unittest discover

docs:
	rm -f docs/$(PROJECT_NAME).rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ auto-discover
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	@echo "Documentation build complete. Open 'docs/_build/html/index.html' to view."

# Development targets
venv:
	python3 -m venv $(VENV_NAME)
	$(VENV_NAME)/bin/pip install -U pip
	$(VENV_NAME)/bin/pip install -r requirements.txt

venv-dev: venv
	$(VENV_NAME)/bin/pip install -r requirements-dev.txt
