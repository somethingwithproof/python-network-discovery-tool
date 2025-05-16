"""Main entry point for the network discovery tool.

This module provides the main entry point for the application when run as a module
using 'python -m network_discovery' or when installed and run from the command line.
"""

import sys

from network_discovery.interfaces.cli import cli

if __name__ == "__main__":
    """Execute the CLI when this module is run directly."""
    sys.exit(cli())
