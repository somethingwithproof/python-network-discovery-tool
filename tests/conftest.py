"""Pytest configuration file."""

# pylint: disable=redefined-outer-name

import os
import tempfile
from typing import Generator, Dict, Any

import pytest

from network_discovery.domain.device import Device
from network_discovery.domain.device_manager import DeviceManager
from network_discovery.infrastructure.repository import JsonFileRepository


@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture
def temp_file() -> Generator[str, None, None]:
    """Create a temporary file for tests."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file_path = tmp_file.name
        yield tmp_file_path
        os.unlink(tmp_file_path)


@pytest.fixture
def device_dict() -> Dict[str, Any]:
    """Return a dictionary representation of a device."""
    return {
        "id": 1,
        "host": "example.com",
        "ip": "192.168.1.1",
        "snmp_group": "public",
        "alive": True,
        "snmp": True,
        "ssh": True,
        "mysql": True,
        "mysql_user": "user",
        "mysql_password": "password",
        "uname": "Linux",
        "errors": ["Error 1", "Error 2"],
        "scanned": True,
    }


@pytest.fixture
def device(device_dict: Dict[str, Any]) -> Device:
    """Return a device instance."""
    return Device.from_dict(device_dict.copy())


@pytest.fixture
def device_manager(device: Device) -> DeviceManager:
    """Return a device manager instance with a device."""
    manager = DeviceManager()
    manager.add_device(device)
    return manager


@pytest.fixture
def json_repository(temp_file: str) -> JsonFileRepository:
    """Return a JSON file repository instance."""
    return JsonFileRepository(temp_file)
