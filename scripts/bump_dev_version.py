#!/usr/bin/env python3
"""
Script to bump the version number for development after a release.

This script increments the minor version and adds a ".dev0" suffix to indicate
that this is a development version. For example, if the current version is 0.3.0,
it will be bumped to 0.4.0.dev0.

Usage:
    python scripts/bump_dev_version.py [--dry-run]

Options:
    --dry-run   Run without making any changes
"""

import argparse
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


def get_current_version():
    """Get the current version from __init__.py."""
    init_path = Path("src/network_discovery/__init__.py")
    with open(init_path, "r") as f:
        content = f.read()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    return None


def bump_version(current_version, dry_run=False):
    """Bump the version for development."""
    # Parse the current version
    match = re.match(r"(\d+)\.(\d+)\.(\d+)(.*)", current_version)
    if not match:
        print(f"Error: Could not parse version '{current_version}'")
        sys.exit(1)

    major, minor, patch, suffix = match.groups()

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
        print(f"Would update {init_path} with version {new_version}")
    else:
        with open(init_path, "w") as f:
            f.write(new_content)
        print(f"Updated {init_path} with version {new_version}")

    return new_version


def commit_changes(new_version, dry_run=False):
    """Commit the version bump."""
    if dry_run:
        print(f"Would commit version bump to {new_version}")
    else:
        run_command(f"git add src/network_discovery/__init__.py")
        run_command(
            f'git commit -m "chore: bump version to {new_version} for development"'
        )
        print(f"Committed version bump to {new_version}")


def main():
    parser = argparse.ArgumentParser(description="Bump version for development")
    parser.add_argument(
        "--dry-run", action="store_true", help="Run without making changes"
    )
    args = parser.parse_args()

    # Get the current version
    current_version = get_current_version()
    if not current_version:
        print("Error: Could not determine current version")
        sys.exit(1)

    print(f"Current version: {current_version}")

    # Bump the version
    new_version = bump_version(current_version, args.dry_run)
    print(f"New version: {new_version}")

    # Commit the changes
    commit_changes(new_version, args.dry_run)

    print(
        f"Version bumped from {current_version} to {new_version} {'(dry run)' if args.dry_run else ''}"
    )


if __name__ == "__main__":
    main()
