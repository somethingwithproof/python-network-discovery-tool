#!/usr/bin/env python3
"""
Script to generate release notes from the changelog.

This script extracts the latest release notes from the CHANGES.md file
and formats them for use in GitHub releases or other announcements.

Usage:
    python scripts/generate_release_notes.py [--version VERSION] [--output FILE]

Options:
    --version VERSION    Specific version to extract (default: latest)
    --output FILE        Output file (default: stdout)
"""

import argparse
import re
import sys
from pathlib import Path


def read_changelog():
    """Read the changelog file."""
    changelog_path = Path("CHANGES.md")
    if not changelog_path.exists():
        print(f"Error: Changelog file not found at {changelog_path}")
        sys.exit(1)
    
    with open(changelog_path, "r") as f:
        return f.read()


def extract_version_notes(changelog, version=None):
    """Extract notes for a specific version or the latest version."""
    # Find all version sections
    version_pattern = r"## Version (\d+\.\d+\.\d+) \(.*?\)(.*?)(?=## Version|\Z)"
    matches = re.findall(version_pattern, changelog, re.DOTALL)
    
    if not matches:
        print("Error: No version sections found in the changelog")
        sys.exit(1)
    
    if version:
        # Find the specified version
        for ver, notes in matches:
            if ver == version:
                return ver, notes.strip()
        
        print(f"Error: Version {version} not found in the changelog")
        sys.exit(1)
    else:
        # Return the latest version (first match)
        return matches[0][0], matches[0][1].strip()


def format_release_notes(version, notes):
    """Format the release notes for GitHub or other platforms."""
    # Add a title
    formatted_notes = f"# Release {version}\n\n"
    
    # Add the notes
    formatted_notes += notes
    
    return formatted_notes


def main():
    parser = argparse.ArgumentParser(description="Generate release notes from changelog")
    parser.add_argument("--version", help="Specific version to extract (default: latest)")
    parser.add_argument("--output", help="Output file (default: stdout)")
    args = parser.parse_args()
    
    # Read the changelog
    changelog = read_changelog()
    
    # Extract the version notes
    version, notes = extract_version_notes(changelog, args.version)
    
    # Format the release notes
    release_notes = format_release_notes(version, notes)
    
    # Output the release notes
    if args.output:
        with open(args.output, "w") as f:
            f.write(release_notes)
        print(f"Release notes for version {version} written to {args.output}")
    else:
        print(release_notes)


if __name__ == "__main__":
    main()
