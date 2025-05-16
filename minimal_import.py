#!/usr/bin/env python3
"""
Minimal script to identify memory issues during import of scanner module.
This script isolates each import step and reports memory usage.
"""

import os
import sys
import gc
# import resource  # Not used
import psutil  # If not available, comment this out or install with pip


def get_memory_usage():
    """Get current memory usage in a readable format."""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return f"RSS: {memory_info.rss / 1024 / 1024:.2f} MB, VMS: {memory_info.vms / 1024 / 1024:.2f} MB"


def log_step(step_name):
    """Log a step with current memory usage."""
    memory = get_memory_usage()
    print(f"STEP: {step_name} - Memory: {memory}")
    sys.stdout.flush()  # Ensure output is printed immediately


# Start tracking memory
print("=" * 80)
print("Starting minimal import test")
print("=" * 80)
log_step("Initial state")

try:
    # Import fundamental dependencies first
    print("\nImporting fundamental dependencies...")
    log_step("Before importing logging")
    import logging
    log_step("After importing logging")
    
    log_step("Before importing asyncio")
    # import asyncio  # Not used
    log_step("After importing asyncio")
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger("minimal_import")
    
    # Import each scanner-related dependency individually
    print("\nImporting core dependencies...")
    
    log_step("Before importing nmap")
    try:
        import nmap
        log_step("After importing nmap")
        logger.info(f"Imported nmap version: {getattr(nmap, '__version__', 'unknown')}")
    except ImportError as e:
        logger.error(f"Failed to import nmap: {e}")
        
    # Import scanner components individually
    print("\nImporting scanner components...")
    
    log_step("Before importing Device")
    # Only importing for checking memory usage - not directly used
    from network_discovery.domain.device import Device  # noqa: F401
    log_step("After importing Device")
    
    # Run garbage collection to see if it helps
    gc.collect()
    log_step("After garbage collection")
    
    log_step("Before importing NmapDeviceScanner")
    from network_discovery.infrastructure.scanner import NmapDeviceScanner
    log_step("After importing NmapDeviceScanner")
    
    # Create scanner instance but don't use it
    print("\nCreating scanner instance...")
    log_step("Before creating scanner")
    scanner = NmapDeviceScanner()
    log_step("After creating scanner")
    
    # Final garbage collection
    gc.collect()
    log_step("Final state after garbage collection")
    
    print("\nAll imports completed successfully")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    print("=" * 80)
    print("Test completed")
    print("=" * 80)