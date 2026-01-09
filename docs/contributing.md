# Contributing

For contribution guidelines, see the main [CONTRIBUTING.md](../CONTRIBUTING.md) file in the repository root.

## Quick Reference

### Setup

```bash
git clone https://github.com/thomasvincent/python-auto-discover-network-Device-Management.git
cd python-auto-discover-network-Device-Management
pip install -e ".[dev]"
```

### Quality Checks

```bash
ruff check .          # Linting
mypy .                # Type checking
pytest                # Tests
pytest --cov          # Tests with coverage
```

### Submit Changes

1. Fork the repository
2. Create a feature branch
3. Make changes and run quality checks
4. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for complete guidelines.
