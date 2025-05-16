"""Minimal test for NmapDeviceScanner initialization."""

import gc
import pytest
from unittest.mock import MagicMock, patch

from network_discovery.domain.device import Device
from network_discovery.infrastructure.scanner import NmapDeviceScanner


class TestMinimalScanner:
    """Test basic scanner initialization to isolate memory issues."""

    def test_scanner_init(self):
        """Test that a scanner can be instantiated."""
        scanner = NmapDeviceScanner()
        assert isinstance(scanner, NmapDeviceScanner)

    @pytest.mark.asyncio
    async def test_is_alive_basic_mock(self):
        """Test is_alive with a minimal mock setup."""
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        scanner = NmapDeviceScanner()

        mock_scanner = MagicMock()
        mock_scanner.all_hosts.return_value = [device.ip]
        mock_host = MagicMock()
        mock_host.state.return_value = "up"
        mock_scanner.__getitem__.return_value = mock_host

        with patch("nmap.PortScanner", return_value=mock_scanner):
            result = await scanner.is_alive(device)
            assert result is True

        gc.collect()