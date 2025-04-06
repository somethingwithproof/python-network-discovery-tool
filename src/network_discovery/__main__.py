"""Main entry point for the network discovery tool.

This module provides the main entry point for the application when run as a module.
"""

from network_discovery.interfaces.cli import cli

if __name__ == "__main__":
    cli()
