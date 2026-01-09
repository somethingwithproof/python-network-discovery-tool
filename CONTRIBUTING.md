# Contributing

Contributions are welcome! This guide explains how to contribute to the Network Device Discovery Tool.

## Getting Started

### Prerequisites

- Python 3.12 or later
- Git
- System dependencies for SNMP and MySQL (see [Getting Started](docs/getting-started.md))

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/python-auto-discover-network-Device-Management.git
cd python-auto-discover-network-Device-Management

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

Follow these code style guidelines:

- Use Python 3.14+ features (type aliases, pattern matching, StrEnum)
- Add type hints to all public functions and methods
- Write docstrings for all public classes and functions
- Use `slots=True` on dataclasses for memory efficiency
- Validate all external input for security

### 3. Run Quality Checks

```bash
# Linting
ruff check .
ruff check --fix .  # Auto-fix issues

# Type checking
mypy .

# Tests
pytest
pytest --cov  # With coverage report
```

### 4. Commit Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: add support for SNMPv3 authentication"
```

Commit message prefixes:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions or fixes
- `refactor:` Code refactoring

### 5. Submit a Pull Request

1. Push your branch to GitHub
2. Open a pull request against the `main` branch
3. Fill out the PR template with:
   - Description of changes
   - Related issues
   - Testing performed

## Types of Contributions

### Report Bugs

File issues at [GitHub Issues](https://github.com/thomasvincent/python-auto-discover-network-Device-Management/issues).

Include:
- Python version (`python --version`)
- Operating system and version
- Steps to reproduce the issue
- Expected vs. actual behavior
- Error messages and tracebacks

### Suggest Features

Open a GitHub issue with the `enhancement` label. Describe:
- The problem you're trying to solve
- Your proposed solution
- Alternative approaches you considered

### Improve Documentation

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add examples
- Improve API documentation
- Add troubleshooting guides

### Write Tests

Help improve test coverage:
- Add tests for untested code paths
- Add integration tests
- Add edge case tests

## Pull Request Guidelines

Before submitting a pull request:

1. **Tests pass**: All existing and new tests must pass
2. **Linting passes**: No ruff or mypy errors
3. **Documentation updated**: Update docs if adding features
4. **Backwards compatible**: Avoid breaking existing functionality
5. **Focused changes**: One feature or fix per PR

## Code Review Process

1. A maintainer will review your PR
2. Address any feedback or requested changes
3. Once approved, a maintainer will merge your PR

## Questions?

- Open a [GitHub Discussion](https://github.com/thomasvincent/python-auto-discover-network-Device-Management/discussions)
- Check existing issues and discussions first

Thank you for contributing!
