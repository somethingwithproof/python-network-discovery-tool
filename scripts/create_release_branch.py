#!/usr/bin/env python3
"""
Script to create and manage release branches.

This script helps with creating release branches from the develop branch,
which is a common practice in GitFlow and similar workflows.

Usage:
    python scripts/create_release_branch.py <version>

Arguments:
    version     The version to release (e.g., 0.3.0)
"""

import argparse
from pathlib import Path
import re
import subprocess
import sys


def run_command(command, check=True):
    """Run a shell command and return its output."""
    print(f"Running: {command}")
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


def check_git_status():
    """Check if the git working directory is clean."""
    status = run_command("git status --porcelain")
    if status:
        print(
            "Error: Working directory is not clean. Please commit or stash your changes."
        )
        sys.exit(1)


def update_version_in_branch(version):
    """Update the version in __init__.py in the current branch."""
    init_path = Path("src/network_discovery/__init__.py")
    with open(init_path, "r") as f:
        content = f.read()

    new_content = re.sub(
        r'__version__\s*=\s*["\']([^"\']+)["\']',
        f'__version__ = "{version}"',
        content,
    )

    with open(init_path, "w") as f:
        f.write(new_content)

    print(f"Updated {init_path} with version {version}")

    # Commit the change
    run_command(f"git add {init_path}")
    run_command(f'git commit -m "chore: bump version to {version}"')


def create_release_branch(version):
    """Create a release branch from the develop branch."""
    # Make sure we're on the develop branch
    current_branch = run_command("git rev-parse --abbrev-ref HEAD")
    if current_branch != "develop":
        print(f"Warning: You are on branch '{current_branch}', not 'develop'.")
        confirm = input("Continue anyway? [y/N] ")
        if confirm.lower() != "y":
            print("Aborting.")
            sys.exit(0)

    # Create the release branch
    branch_name = f"release/{version}"
    run_command(f"git checkout -b {branch_name}")
    print(f"Created branch {branch_name}")

    # Update the version in the release branch
    update_version_in_branch(version)

    # Push the branch
    run_command(f"git push -u origin {branch_name}")
    print(f"Pushed branch {branch_name} to origin")

    print(f"\nRelease branch {branch_name} has been created and pushed.")
    print("\nNext steps:")
    print(
        f"1. Make any final adjustments to the release in the {branch_name} branch"
    )
    print("2. When ready, merge the release branch into main:")
    print(f"   git checkout main && git merge --no-ff {branch_name}")
    print("3. Then merge the release branch back into develop:")
    print(f"   git checkout develop && git merge --no-ff {branch_name}")
    print("4. Finally, delete the release branch:")
    print(f"   git branch -d {branch_name}")
    print("   git push origin --delete {branch_name}")


def main():
    parser = argparse.ArgumentParser(description="Create a release branch")
    parser.add_argument("version", help="The version to release (e.g., 0.3.0)")
    args = parser.parse_args()

    # Validate the version
    version = validate_version(args.version)

    # Check if the working directory is clean
    check_git_status()

    # Confirm with the user
    confirm = input(f"Create release branch for version {version}? [y/N] ")
    if confirm.lower() != "y":
        print("Aborting.")
        sys.exit(0)

    # Create the release branch
    create_release_branch(version)


if __name__ == "__main__":
    main()
