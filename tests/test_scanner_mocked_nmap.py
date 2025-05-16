"""Test scanner with completely mocked nmap module."""

import sys
import gc
import pytest
from unittest.mock import MagicMock

# Import modules that depend on the mocked 'nmap'
# These imports must be placed after the mock setup below
# We'll avoid the E402 by using a different import approach

# Mock the nmap module before importing scanner code
mock_nmap = MagicMock()


class MockPortScanner:
    """Mock implementation of nmap.PortScanner."""

    def __init__(self):
        self.last_scan_hosts = None
        self.last_scan_args = None
        self.hosts_data = {}

    def scan(self, hosts=None, arguments=None):
        self.last_scan_hosts = hosts
        self.last_scan_args = arguments
        return {}

    def all_hosts(self):
        return list(self.hosts_data.keys())

    def __getitem__(self, key):
        if key in self.hosts_data:
            return self.hosts_data[key]
        host_mock = MagicMock()
        host_mock.state.return_value = "down"
        return host_mock


# Set up the mock before importing the modules that use nmap
mock_nmap.PortScanner = MockPortScanner
sys.modules["nmap"] = mock_nmap

# Now we can import the modules that depend on the mocked 'nmap'
from network_discovery.domain.device import Device  # noqa: E402
from network_discovery.infrastructure.scanner import NmapDeviceScanner  # noqa: E402


@pytest.fixture
def setup_scanner():
    """Set up a scanner instance and a device with mocked scan results."""
    mock_scanner = MockPortScanner()
    device = Device(id=1, host="example.com", ip="192.168.1.1")

    host_state = MagicMock()
    host_state.state.return_value = "up"
    mock_scanner.hosts_data[device.ip] = host_state

    return {
        "scanner": NmapDeviceScanner(),
        "device": device,
        "mock_scanner": mock_scanner
    }


class TestMockedNmapScanner:
    """Test scanner with a fully mocked nmap module."""

    def test_scanner_init(self):
        """Ensure NmapDeviceScanner initializes properly."""
        scanner = NmapDeviceScanner()
        assert isinstance(scanner, NmapDeviceScanner)
        gc.collect()

    @pytest.mark.asyncio
    async def test_is_alive(self, setup_scanner):
        """Test is_alive against a mocked-up host marked as 'up'."""
        scanner = setup_scanner["scanner"]
        device = setup_scanner["device"]

        result = await scanner.is_alive(device)

        assert result is True
        gc.collect()