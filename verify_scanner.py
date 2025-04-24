#!/usr/bin/env python3
"""
Standalone script to verify scanner functionality without pytest.
This will help isolate if the memory issue is with pytest or with the scanner.
"""

import sys
import gc
import time
import logging
import asyncio
from unittest.mock import MagicMock

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("verify_scanner")

# First step: Mock nmap module before any other imports
logger.info("Setting up mock nmap module")
mock_nmap = MagicMock()

# Create a mock PortScanner class
class MockPortScanner:
    """Mock implementation of nmap.PortScanner."""
    
    def __init__(self):
        """Initialize the mock scanner."""
        self.last_scan_hosts = None
        self.last_scan_args = None
        self.hosts_data = {}
        logger.debug("Created MockPortScanner instance")
        
    def scan(self, hosts=None, arguments=None):
        """Mock the scan method."""
        self.last_scan_hosts = hosts
        self.last_scan_args = arguments
        logger.debug(f"Mock scan called with hosts={hosts}, args={arguments}")
        return {}
        
    def all_hosts(self):
        """Return configured hosts."""
        logger.debug(f"all_hosts called, returning: {list(self.hosts_data.keys())}")
        return list(self.hosts_data.keys())
        
    def __getitem__(self, key):
        """Return data for a host."""
        logger.debug(f"__getitem__ called with key: {key}")
        if key in self.hosts_data:
            return self.hosts_data[key]
        # Return a default mock for missing hosts
        host_mock = MagicMock()
        host_mock.state.return_value = "down"
        logger.debug(f"Host {key} not found, returning default mock")
        return host_mock

# Attach our mock PortScanner to the mock nmap module
mock_nmap.PortScanner = MockPortScanner

# Install the mock as the real nmap module
sys.modules['nmap'] = mock_nmap
logger.info("Installed mock nmap module")

# Now import the scanner-related modules
try:
    logger.info("Importing scanner modules")
    from network_discovery.domain.device import Device
    from network_discovery.infrastructure.scanner import NmapDeviceScanner
    logger.info("Successfully imported scanner modules")
except Exception as e:
    logger.error(f"Error importing scanner modules: {e}")
    sys.exit(1)

async def test_scanner():
    """Run a basic test of scanner functionality."""
    logger.info("Creating test device and scanner")
    
    try:
        # Create a device for testing
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        logger.info(f"Created test device: {device}")
        
        # Create the scanner
        scanner = NmapDeviceScanner()
        logger.info("Created scanner instance")
        
        # Configure mock scanner
        port_scanner = MockPortScanner()
        port_scanner.hosts_data["192.168.1.1"] = MagicMock()
        port_scanner.hosts_data["192.168.1.1"].state.return_value = "up"
        logger.info("Configured mock scanner data")
        
        # Override how PortScanner is created
        def get_mock_scanner(*args, **kwargs):
            logger.debug("Returning pre-configured mock scanner")
            return port_scanner
            
        mock_nmap.PortScanner = get_mock_scanner
        
        # Run the test
        logger.info("Testing is_alive method")
        result = await scanner.is_alive(device)
        logger.info(f"is_alive result: {result}")
        
        # Verify the result
        assert result is True, f"Expected True but got {result}"
        logger.info("Test passed!")
        
        # Clean up
        logger.info("Running garbage collection")
        gc.collect()
        
        return True
    except Exception as e:
        logger.error(f"Error during test: {e}", exc_info=True)
        return False

def main():
    """Run the test and report results."""
    logger.info("Starting scanner verification")
    
    try:
        # Run the async test
        success = asyncio.run(test_scanner())
        
        if success:
            logger.info("All tests completed successfully")
            return 0
        else:
            logger.error("Tests failed")
            return 1
    except Exception as e:
        logger.error(f"Error running tests: {e}", exc_info=True)
        return 1
    finally:
        # Final cleanup
        logger.info("Final cleanup")
        gc.collect()

if __name__ == "__main__":
    # Set Python's process memory debug flags
    import resource
    # Set a soft memory limit (4GB)
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024 * 1024 * 1024, -1))
    
    # Exit with the result of main
    sys.exit(main())

