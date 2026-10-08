# Contributing to Network Discovery Tool

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/thomasvincent/python-network-discovery-tool/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "feature" is open to whoever wants to implement it.

### Write Documentation

Network Discovery Tool could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/thomasvincent/python-network-discovery-tool/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome!

## Get Started!

1. Fork the `python-network-discovery-tool` repo on GitHub and clone your fork.
2. Create a virtualenv with the development extras:
   ```bash
   mise exec python@3.14 -- uv sync --locked --extra dev
   ```
3. Create a branch for your change:
   ```bash
   git checkout -b name-of-your-bugfix-or-feature
   ```
4. Before pushing, run the same checks as CI:
   ```bash
   uv run ruff check .
   uv run ruff format --check .
   uv run mypy
   uv run pytest --cov=netprobe
   ```
5. Commit with `git commit -s`, push, and open a pull request.

The code lives in `src/netprobe/`; tests live in `tests/`.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in README.md.
3. The pull request should work for Python 3.12, 3.13, and 3.14. Check the GitHub Actions workflow and make sure that the tests pass for all supported Python versions.

## Code of Conduct

Please note that the Network Discovery Tool project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

## Versioning and releases

Add user-visible changes under `## Unreleased` in `CHANGES.md`. Use conventional PR titles and choose release bumps based on the documented compatibility contract. See [Versioning and releases](docs/releasing.md) for preparation, tag validation, GitHub draft releases, and optional PyPI trusted publishing.
