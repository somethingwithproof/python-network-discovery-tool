#!/usr/bin/env python3
"""
Release script for the network-discovery package.

This script automates the release process by:
1. Validating the release version
2. Running tests to ensure everything is working
3. Updating version numbers in files
4. Creating a git tag
5. Generating release notes and changelog entries
6. Creating a GitHub release
7. Building and publishing the package to PyPI (optional)
8. Optionally bumping the version for development after release

Usage:
    python scripts/release.py [--dry-run] [--no-publish] [--bump-dev] <version>

Arguments:
    version     The version to release (e.g., 0.3.0)

Options:
    --dry-run     Run the script without making any changes
    --no-publish  Skip publishing to PyPI
    --bump-dev    Bump version for development after release (e.g., 0.3.0 → 0.4.0.dev0)
"""

import argparse
from datetime import datetime
import os
from pathlib import Path
import re
import subprocess
import sys


def run_command(command, dry_run=False, check=True):
    """Run a shell command and return its output."""
    print(f"Running: {command}")
    if dry_run:
        return ""
    result = subprocess.run(
        command, shell=True, check=check, text=True, capture_output=True
    )
    return result.stdout.strip()


def validate_version(version):
    """Validate that the version string is in the correct format."""
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        print(f"Error: Version '{version}' does not match the format X.Y.Z")
        sys.exit(1)
    return version


def get_current_version():
    """Get the current version from __init__.py."""
    init_path = Path("src/network_discovery/__init__.py")
    with open(init_path, "r") as f:
        content = f.read()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    return None


def update_version(version, dry_run=False):
    """Update the version in __init__.py."""
    init_path = Path("src/network_discovery/__init__.py")
    with open(init_path, "r") as f:
        content = f.read()

    new_content = re.sub(
        r'__version__\s*=\s*["\']([^"\']+)["\']',
        f'__version__ = "{version}"',
        content,
    )

    if dry_run:
        print(f"Would update {init_path} with version {version}")
    else:
        with open(init_path, "w") as f:
            f.write(new_content)
        print(f"Updated {init_path} with version {version}")


def run_tests(dry_run=False):
    """Run the test suite to ensure everything is working."""
    print("Running tests...")
    if dry_run:
        print("Would run: pytest")
        return True

    try:
        subprocess.run("pytest", shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        print("Tests failed. Aborting release.")
        return False


def get_changes_since_last_tag():
    """Get the git log since the last tag."""
    last_tag = run_command("git describe --tags --abbrev=0", check=False)
    if not last_tag:
        # If there are no tags yet, get all commits
        return run_command("git log --pretty=format:'%h %s' --no-merges")

    return run_command(
        f"git log {last_tag}..HEAD --pretty=format:'%h %s' --no-merges"
    )


def categorize_changes(changes):
    """Categorize changes into features, fixes, etc. based on commit messages."""
    features = []
    fixes = []
    security = []
    other = []

    for line in changes.split("\n"):
        if not line.strip():
            continue

        if re.search(r"\b(feat|feature|add|improve)\b", line, re.IGNORECASE):
            features.append(line)
        elif re.search(r"\b(fix|bug|issue)\b", line, re.IGNORECASE):
            fixes.append(line)
        elif re.search(r"\b(security|vuln|cve)\b", line, re.IGNORECASE):
            security.append(line)
        else:
            other.append(line)

    return {
        "features": features,
        "fixes": fixes,
        "security": security,
        "other": other,
    }


def update_changelog(version, categorized_changes, dry_run=False):
    """Update the CHANGES.md file with the new version and changes."""
    changelog_path = Path("CHANGES.md")
    today = datetime.now().strftime("%Y-%m-%d")

    # Create the new changelog entry
    new_entry = f"## Version {version} ({today})\n\n"

    if categorized_changes["features"]:
        new_entry += "### Features\n"
        for feature in categorized_changes["features"]:
            new_entry += f"- {feature}\n"
        new_entry += "\n"

    if categorized_changes["fixes"]:
        new_entry += "### Bug Fixes\n"
        for fix in categorized_changes["fixes"]:
            new_entry += f"- {fix}\n"
        new_entry += "\n"

    if categorized_changes["security"]:
        new_entry += "### Security\n"
        for item in categorized_changes["security"]:
            new_entry += f"- {item}\n"
        new_entry += "\n"

    if categorized_changes["other"]:
        new_entry += "### Other Changes\n"
        for item in categorized_changes["other"]:
            new_entry += f"- {item}\n"
        new_entry += "\n"

    # Read the current changelog
    with open(changelog_path, "r") as f:
        current_changelog = f.read()

    # Insert the new entry after the title
    title_match = re.search(r"^# Changelog\n", current_changelog, re.MULTILINE)
    if title_match:
        insert_pos = title_match.end()
        new_changelog = (
            current_changelog[:insert_pos]
            + "\n"
            + new_entry
            + current_changelog[insert_pos:]
        )
    else:
        # If no title found, prepend the title and new entry
        new_changelog = f"# Changelog\n\n{new_entry}{current_changelog}"

    if dry_run:
        print(
            f"Would update {changelog_path} with new entry for version {version}"
        )
        print("New entry:")
        print(new_entry)
    else:
        with open(changelog_path, "w") as f:
            f.write(new_changelog)
        print(f"Updated {changelog_path} with new entry for version {version}")

    return new_entry


def create_git_tag(version, dry_run=False):
    """Create and push a git tag for the release."""
    tag_name = f"v{version}"
    tag_message = f"Release {version}"

    if dry_run:
        print(f"Would create git tag: {tag_name}")
        print(f"Would push git tag: {tag_name}")
    else:
        run_command(f'git tag -a {tag_name} -m "{tag_message}"')
        print(f"Created git tag: {tag_name}")

        # Push the tag
        run_command(f"git push origin {tag_name}")
        print(f"Pushed git tag: {tag_name}")


def create_github_release(version, changelog_entry, dry_run=False):
    """Create a GitHub release using the GitHub CLI."""
    tag_name = f"v{version}"
    title = f"Release {version}"

    # Check if GitHub CLI is installed
    try:
        run_command("gh --version", check=True)
    except subprocess.CalledProcessError:
        print(
            "GitHub CLI (gh) is not installed. Skipping GitHub release creation."
        )
        print("Install it from: https://cli.github.com/")
        return

    # Create the release
    if dry_run:
        print(f"Would create GitHub release: {title}")
        print(f"Release notes would be:\n{changelog_entry}")
    else:
        # Create a temporary file for the release notes
        notes_file = Path("release_notes_temp.md")
        with open(notes_file, "w") as f:
            f.write(changelog_entry)

        # Create the release
        run_command(
            f'gh release create {tag_name} --title "{title}" --notes-file {notes_file}'
        )

        # Clean up
        notes_file.unlink()
        print(f"Created GitHub release: {title}")


def build_and_publish(dry_run=False, publish=True):
    """Build and publish the package to PyPI."""
    # Build the package
    if dry_run:
        print("Would build the package")
    else:
        run_command("python -m build")
        print("Built the package")

    # Publish to PyPI if requested
    if publish:
        if dry_run:
            print("Would publish to PyPI")
        else:
            run_command("python -m twine upload dist/*")
            print("Published to PyPI")


def bump_dev_version(version, dry_run=False):
    """Bump the version for development after a release."""
    # Parse the current version
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        print(f"Error: Could not parse version '{version}'")
        return None

    major, minor, patch = match.groups()

    # Increment the minor version and add .dev0
    new_minor = int(minor) + 1
    new_version = f"{major}.{new_minor}.0.dev0"

    # Update the version in __init__.py
    init_path = Path("src/network_discovery/__init__.py")
    with open(init_path, "r") as f:
        content = f.read()

    new_content = re.sub(
        r'__version__\s*=\s*["\']([^"\']+)["\']',
        f'__version__ = "{new_version}"',
        content,
    )

    if dry_run:
        print(
            f"Would update {init_path} with development version {new_version}"
        )
    else:
        with open(init_path, "w") as f:
            f.write(new_content)
        print(f"Updated {init_path} with development version {new_version}")

    # Commit the change
    if not dry_run:
        run_command(f"git add {init_path}")
        run_command(
            f'git commit -m "chore: bump version to {new_version} for development"'
        )
        run_command(f"git push origin HEAD")
        print(f"Committed and pushed development version bump to {new_version}")
    else:
        print(f"Would commit development version bump to {new_version}")

    return new_version


def main():
    parser = argparse.ArgumentParser(
        description="Release script for network-discovery"
    )
    parser.add_argument("version", help="The version to release (e.g., 0.3.0)")
    parser.add_argument(
        "--dry-run", action="store_true", help="Run without making changes"
    )
    parser.add_argument(
        "--no-publish", action="store_true", help="Skip publishing to PyPI"
    )
    parser.add_argument(
        "--bump-dev",
        action="store_true",
        help="Bump version for development after release",
    )
    args = parser.parse_args()

    # Validate the version
    version = validate_version(args.version)
    current_version = get_current_version()

    print(f"Current version: {current_version}")
    print(f"New version: {version}")

    # Confirm with the user
    if not args.dry_run:
        confirm = input(f"Release version {version}? [y/N] ")
        if confirm.lower() != "y":
            print("Aborting release.")
            sys.exit(0)

    # Run tests
    if not run_tests(args.dry_run):
        sys.exit(1)

    # Update version
    update_version(version, args.dry_run)

    # Get changes since last tag
    changes = get_changes_since_last_tag()
    categorized_changes = categorize_changes(changes)

    # Update changelog
    changelog_entry = update_changelog(
        version, categorized_changes, args.dry_run
    )

    # Commit changes
    if not args.dry_run:
        run_command(f"git add src/network_discovery/__init__.py CHANGES.md")
        run_command(f'git commit -m "chore: bump version to {version}"')
        print("Committed version bump")
    else:
        print("Would commit version bump")

    # Create git tag
    create_git_tag(version, args.dry_run)

    # Create GitHub release
    create_github_release(version, changelog_entry, args.dry_run)

    # Build and publish
    build_and_publish(args.dry_run, not args.no_publish)

    print(
        f"Release {version} {'would be' if args.dry_run else 'has been'} completed!"
    )

    # Bump version for development if requested
    if args.bump_dev:
        print("\nBumping version for development...")
        dev_version = bump_dev_version(version, args.dry_run)
        print(f"Development version bumped to {dev_version}")


if __name__ == "__main__":
    main()
