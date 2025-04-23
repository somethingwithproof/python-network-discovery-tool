# Release Management Scripts

This directory contains scripts for managing the release process of the Network Discovery Tool.

## Available Scripts

### `release.py`

Automates the release process by:
- Validating the release version
- Running tests to ensure everything is working
- Updating version numbers in files
- Creating a git tag
- Generating release notes and changelog entries
- Creating a GitHub release
- Building and publishing the package to PyPI (optional)

Usage:
```bash
python scripts/release.py [--dry-run] [--no-publish] <version>
```

### `create_release_branch.py`

Creates a release branch from the develop branch following GitFlow practices.

Usage:
```bash
python scripts/create_release_branch.py <version>
```

### `create_hotfix.py`

Creates a hotfix branch from the main branch for critical bug fixes.

Usage:
```bash
python scripts/create_hotfix.py <version>
```

### `generate_release_notes.py`

Extracts release notes from the changelog for a specific version.

Usage:
```bash
python scripts/generate_release_notes.py [--version VERSION] [--output FILE]
```

### `bump_dev_version.py`

Bumps the version number for development after a release by incrementing the minor version and adding a ".dev0" suffix.

Usage:
```bash
python scripts/bump_dev_version.py [--dry-run]
```

### `make_scripts_executable.sh`

Makes all Python scripts in this directory executable.

Usage:
```bash
bash scripts/make_scripts_executable.sh
```

## Setting Up

1. Make the scripts executable:
   ```bash
   bash scripts/make_scripts_executable.sh
   ```

2. Ensure you have the required dependencies:
   ```bash
   pip install build twine pytest pytest-cov
   ```

## GitHub Actions Integration

These scripts are integrated with GitHub Actions workflows:

- `.github/workflows/release.yml`: Runs the release process
- `.github/workflows/release-notes.yml`: Generates release notes when a tag is pushed
- `.github/workflows/publish.yml`: Builds and publishes the package to PyPI when a tag is pushed
- `.github/workflows/ci.yml`: Runs tests and linting on push and pull requests

## Documentation

For more detailed information about the release process, see the [Release Process Documentation](../docs/release-process.md).
