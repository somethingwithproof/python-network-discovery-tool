"""Test scanner with completely mocked nmap module."""

import gc
from unittest.mock import MagicMock, patch

import pytest

from network_discovery.domain.device import Device
from network_discovery.infrastructure.scanner import NmapDeviceScanner


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


class TestMockedNmapScanner:
    """Test scanner with a fully mocked nmap module."""

    def test_scanner_init(self):
        """Ensure NmapDeviceScanner initializes properly."""
        scanner = NmapDeviceScanner()
        assert isinstance(scanner, NmapDeviceScanner)
        gc.collect()

    @pytest.mark.asyncio
    async def test_is_alive(self):
        """Test is_alive against a mocked-up host marked as 'up'."""
        device = Device(id=1, host="example.com", ip="192.168.1.1")

        # Create the mock scanner
        mock_scanner = MockPortScanner()

        # Set up mock data
        host_state = MagicMock()
        host_state.state.return_value = "up"
        mock_scanner.hosts_data[device.ip] = host_state

        # Patch before creating the scanner so it uses our mock
        with patch("nmap.PortScanner", return_value=mock_scanner):
            scanner = NmapDeviceScanner()
            result, errors = await scanner.is_alive(device)

            assert result is True
            assert errors == []

        gc.collect()
