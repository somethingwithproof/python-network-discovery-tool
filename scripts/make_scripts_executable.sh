#!/bin/bash
# Make all Python scripts in the scripts directory executable

# Change to the scripts directory
cd "$(dirname "$0")" || exit

# Make all Python scripts executable
chmod +x *.py

echo "All Python scripts in the scripts directory are now executable."
