# Google Python Style Guide

This project follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).

## Key Principles

### Code Formatting
- **Line Length**: 80 characters maximum
- **Indentation**: 4 spaces (no tabs)
- **Import Organization**: Google style import grouping

### Tools
- **Black**: Code formatter with 80-character line length
- **isort**: Import sorting with Google profile
- **flake8**: Style guide enforcement
- **mypy**: Type checking

### Running Style Checks

```bash
# Format code
python -m black .
python -m isort .

# Check formatting without applying changes
python -m black --check .
python -m isort --check-only .

# Run linter
python -m flake8

# Type checking
python -m mypy src/

# Run all checks
python -m black --check . && python -m isort --check-only . && python -m flake8 && python -m mypy src/
```

### Configuration Files
- `pyproject.toml`: Main configuration for all tools
- `.editorconfig`: Editor settings

## Import Organization

Following Google Python Style Guide:
1. Future imports
2. Standard library imports  
3. Third-party imports
4. First-party imports
5. Local folder imports

## Integration

Style checks are integrated into:
- Pre-commit hooks
- CI/CD pipeline
- IDE/editor settings via `.editorconfig`