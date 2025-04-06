"""Tests for the repository implementations."""

import json
import os
import tempfile

from network_discovery.domain.device import Device
from network_discovery.infrastructure.repository import JsonFileRepository


class TestJsonFileRepository:
    """Tests for the JsonFileRepository class."""

    def test_init(self):
        """Test that a JsonFileRepository can be initialized."""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            try:
                repo = JsonFileRepository(temp.name)
                assert repo.file_path == temp.name
                assert repo.data == {}
            finally:
                os.unlink(temp.name)

    def test_save_and_get(self):
        """Test that a device can be saved and retrieved."""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            try:
                repo = JsonFileRepository(temp.name)
                device = Device(id=1, host="example.com", ip="192.168.1.1")
                repo.save(device)

                # Check that the device was saved to the repository's data
                assert f"device:{device.id}" in repo.data
                assert repo.data[f"device:{device.id}"] == device.to_dict()

                # Check that the device was saved to the file
                with open(temp.name, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    assert f"device:{device.id}" in data
                    assert data[f"device:{device.id}"] == device.to_dict()

                # Check that the device can be retrieved
                retrieved_device = repo.get(device.id)
                assert retrieved_device is not None
                assert retrieved_device.id == device.id
                assert retrieved_device.host == device.host
                assert retrieved_device.ip == device.ip
            finally:
                os.unlink(temp.name)

    def test_get_all(self):
        """Test that all devices can be retrieved."""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            try:
                repo = JsonFileRepository(temp.name)
                device1 = Device(id=1, host="example1.com", ip="192.168.1.1")
                device2 = Device(id=2, host="example2.com", ip="192.168.1.2")
                repo.save(device1)
                repo.save(device2)

                devices = repo.get_all()
                assert len(devices) == 2
                assert any(d.id == 1 for d in devices)
                assert any(d.id == 2 for d in devices)
            finally:
                os.unlink(temp.name)

    def test_delete(self):
        """Test that a device can be deleted."""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            try:
                repo = JsonFileRepository(temp.name)
                device1 = Device(id=1, host="example1.com", ip="192.168.1.1")
                device2 = Device(id=2, host="example2.com", ip="192.168.1.2")
                repo.save(device1)
                repo.save(device2)

                # Check that both devices are in the repository
                assert len(repo.get_all()) == 2

                # Delete one device
                repo.delete(1)

                # Check that only one device remains
                devices = repo.get_all()
                assert len(devices) == 1
                assert devices[0].id == 2

                # Check that the device was deleted from the file
                with open(temp.name, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    assert "device:1" not in data
                    assert "device:2" in data
            finally:
                os.unlink(temp.name)

    def test_load_data_file_not_exists(self):
        """Test that an empty dictionary is returned when the file doesn't exist."""
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            # The file is deleted when the context manager exits
            pass

        # Now the file doesn't exist
        repo = JsonFileRepository(temp.name)
        assert repo.data == {}

        try:
            os.unlink(temp.name)
        except FileNotFoundError:
            pass

    def test_load_data_invalid_json(self):
        """Test that an empty dictionary is returned when the file contains invalid JSON."""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            try:
                temp.write(b"invalid json")
                temp.flush()

                repo = JsonFileRepository(temp.name)
                assert repo.data == {}
            finally:
                os.unlink(temp.name)
