# Release Process

This document outlines the release process for the Network Discovery Tool. It provides a step-by-step guide for maintainers to follow when releasing new versions of the software.

## Release Workflow

The project follows a GitFlow-inspired workflow:

1. Development happens on the `develop` branch
2. For releases, a release branch is created from `develop`
3. After testing and finalization, the release branch is merged into `main`
4. The release branch is also merged back into `develop`
5. The release is tagged and published

## Version Numbering

The project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version when you make incompatible API changes
- **MINOR** version when you add functionality in a backward-compatible manner
- **PATCH** version when you make backward-compatible bug fixes

## Release Checklist

Before initiating a release, ensure:

- All tests are passing
- Documentation is up-to-date
- The changelog is updated with all notable changes
- All pull requests for the release have been merged into `develop`

## Release Process

### Option 1: Using GitHub Actions (Recommended)

1. Go to the GitHub repository's "Actions" tab
2. Select the "Release" workflow
3. Click "Run workflow"
4. Enter the version number (e.g., `0.3.0`)
5. Choose whether to run in dry-run mode
6. Choose whether to publish to PyPI
7. Click "Run workflow"

The GitHub Action will:
- Run tests
- Update version numbers
- Update the changelog
- Create a git tag
- Create a GitHub release
- Build and publish the package to PyPI (if selected)

### Option 2: Using the Release Script Locally

1. Ensure you have the necessary dependencies:
   ```bash
   pip install build twine pytest pytest-cov
   ```

2. Run the release script:
   ```bash
   python scripts/release.py 0.3.0
   ```
   
   You can add the `--dry-run` flag to test the process without making any changes:
   ```bash
   python scripts/release.py --dry-run 0.3.0
   ```
   
   You can add the `--no-publish` flag to skip publishing to PyPI:
   ```bash
   python scripts/release.py --no-publish 0.3.0
   ```

### Option 3: Using GitFlow with Release Branches

1. Create a release branch from `develop`:
   ```bash
   python scripts/create_release_branch.py 0.3.0
   ```

2. Make any final adjustments to the release in the release branch

3. When ready, merge the release branch into `main`:
   ```bash
   git checkout main
   git merge --no-ff release/0.3.0
   ```

4. Create a tag for the release:
   ```bash
   git tag -a v0.3.0 -m "Release 0.3.0"
   git push origin v0.3.0
   ```

5. Merge the release branch back into `develop`:
   ```bash
   git checkout develop
   git merge --no-ff release/0.3.0
   ```

6. Delete the release branch:
   ```bash
   git branch -d release/0.3.0
   git push origin --delete release/0.3.0
   ```

7. Create a GitHub release:
   ```bash
   gh release create v0.3.0 --title "Release 0.3.0" --notes-file release_notes.md
   ```

8. Build and publish the package to PyPI:
   ```bash
   python -m build
   python -m twine upload dist/*
   ```

## Post-Release Tasks

After a successful release:

1. Bump the version number for development:
   ```bash
   python scripts/bump_dev_version.py
   ```
   This will increment the minor version and add a ".dev0" suffix (e.g., 0.3.0 → 0.4.0.dev0)

2. Announce the release to users through appropriate channels
3. Update the documentation site if necessary
4. Close any issues that were fixed in the release
5. Plan the next release cycle

## Hotfix Process

For critical bug fixes that need to be released immediately:

1. Create a hotfix branch from `main`:
   ```bash
   git checkout main
   git checkout -b hotfix/0.3.1
   ```

2. Fix the bug and commit the changes

3. Update the version number and changelog

4. Merge the hotfix branch into `main`:
   ```bash
   git checkout main
   git merge --no-ff hotfix/0.3.1
   ```

5. Tag the release:
   ```bash
   git tag -a v0.3.1 -m "Hotfix 0.3.1"
   git push origin v0.3.1
   ```

6. Merge the hotfix branch into `develop`:
   ```bash
   git checkout develop
   git merge --no-ff hotfix/0.3.1
   ```

7. Delete the hotfix branch:
   ```bash
   git branch -d hotfix/0.3.1
   git push origin --delete hotfix/0.3.1
   ```

8. Follow the same steps as a regular release for creating a GitHub release and publishing to PyPI

## Troubleshooting

### Common Issues

1. **Tests failing during release**
   - Fix the failing tests in the `develop` branch
   - Create a new release branch once tests are passing

2. **Version conflicts**
   - Ensure the version number is incremented correctly
   - Check that the version number is updated in all necessary files

3. **PyPI upload issues**
   - Verify your PyPI credentials
   - Ensure the package version doesn't already exist on PyPI

### Getting Help

If you encounter issues with the release process, please:

1. Check the GitHub Actions logs for detailed error information
2. Review this documentation for any steps you might have missed
3. Reach out to the maintainers for assistance
