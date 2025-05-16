#!/usr/bin/env python3
"""
Bare minimum script to test importing the scanner module.
"""

import sys


def log(message):
    """Print a message and flush stdout."""
    print(message)
    sys.stdout.flush()  # Ensure output is printed immediately


# Start test
log("Starting bare import test")

try:
    # Import device module
    log("Importing Device class...")
    from network_discovery.domain.device import Device
    log("Device class imported successfully")
    # Import scanner module
    log("Importing NmapDeviceScanner class...")
    from network_discovery.infrastructure.scanner import NmapDeviceScanner
    log("NmapDeviceScanner class imported successfully")
    # Create bare objects
    log("Creating test objects...")
    device = Device(id=1, host="example.com", ip="192.168.1.1")
    scanner = NmapDeviceScanner()
    log("Test objects created successfully")
    # Exit successfully
    log("All imports and object creation successful")
    sys.exit(0)
except Exception as e:
    log(f"ERROR: {e}")
    sys.exit(1)
