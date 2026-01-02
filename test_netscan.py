"""Tests for netscan - Modern network scanner."""

import asyncio
from pathlib import Path
import pytest
from netscan import Device, NetworkScanner, save_json, save_csv


def test_device_creation():
    """Test Device dataclass creation."""
    device = Device(ip="192.168.1.1")
    assert device.ip == "192.168.1.1"
    assert not device.alive
    assert not device.ssh
    assert device.errors == []


def test_device_with_services():
    """Test Device with services enabled."""
    device = Device(
        ip="192.168.1.10",
        alive=True,
        ssh=True,
        snmp=True,
        mysql=False,
        hostname="server.local"
    )
    assert device.alive
    assert device.ssh
    assert device.snmp
    assert not device.mysql
    assert device.hostname == "server.local"


@pytest.mark.asyncio
async def test_scanner_initialization():
    """Test NetworkScanner initialization."""
    scanner = NetworkScanner()
    assert scanner.nm is not None


@pytest.mark.asyncio
async def test_check_alive_localhost():
    """Test alive check on localhost."""
    scanner = NetworkScanner()
    # Localhost should always be up
    alive = await asyncio.to_thread(scanner._check_alive, "127.0.0.1")
    assert alive is True


@pytest.mark.asyncio
async def test_scan_localhost():
    """Test scanning localhost."""
    scanner = NetworkScanner()
    device = await scanner.scan_device("127.0.0.1")

    assert device.ip == "127.0.0.1"
    assert device.alive is True
    # SSH might or might not be running locally
    assert isinstance(device.ssh, bool)


@pytest.mark.asyncio
async def test_scan_invalid_ip():
    """Test scanning invalid IP gracefully handles errors."""
    scanner = NetworkScanner()
    device = await scanner.scan_device("999.999.999.999")

    assert device.ip == "999.999.999.999"
    assert not device.alive


def test_save_json(tmp_path):
    """Test JSON export."""
    devices = [
        Device(ip="192.168.1.1", alive=True, ssh=True),
        Device(ip="192.168.1.2", alive=False),
    ]

    output_file = tmp_path / "test.json"
    save_json(devices, output_file)

    assert output_file.exists()
    import json
    data = json.loads(output_file.read_text())
    assert len(data) == 2
    assert data[0]["ip"] == "192.168.1.1"
    assert data[0]["ssh"] is True


def test_save_csv(tmp_path):
    """Test CSV export."""
    devices = [
        Device(ip="192.168.1.1", alive=True, ssh=True, hostname="server"),
        Device(ip="192.168.1.2", alive=False),
    ]

    output_file = tmp_path / "test.csv"
    save_csv(devices, output_file)

    assert output_file.exists()
    content = output_file.read_text()
    assert "192.168.1.1" in content
    assert "192.168.1.2" in content
    assert "server" in content


@pytest.mark.asyncio
async def test_scan_network_single_ip():
    """Test scanning a single IP address."""
    scanner = NetworkScanner()
    devices = await scanner.scan_network("127.0.0.1")

    assert len(devices) == 1
    assert devices[0].ip == "127.0.0.1"
    assert devices[0].alive is True


@pytest.mark.asyncio
async def test_scan_network_invalid():
    """Test scanning with invalid network raises error."""
    scanner = NetworkScanner()

    with pytest.raises(ValueError, match="Invalid network format"):
        await scanner.scan_network("999.999.999.999/24")


@pytest.mark.asyncio
async def test_concurrent_scanning():
    """Test that multiple hosts can be scanned concurrently."""
    scanner = NetworkScanner()
    # Scan a small range including localhost
    devices = await scanner.scan_network("127.0.0.0/30")

    # Should return 2 hosts (127.0.0.1 and 127.0.0.2)
    assert len(devices) == 2
    # At least localhost should be alive
    alive_count = sum(1 for d in devices if d.alive)
    assert alive_count >= 1
