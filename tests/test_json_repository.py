"""Tests for the improved JsonFileRepository class."""

import json
import os
import tempfile
import pytest
from unittest.mock import patch, mock_open

from network_discovery.domain.device import Device
from improvements.json_repository_improved import JsonFileRepository


class TestJsonFileRepository:
    """Tests for the JsonFileRepository class."""

    @pytest.fixture
    def temp_file(self):
        """Create a temporary file for testing."""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(b"{}")
            temp_path = temp.name
        yield temp_path
        os.unlink(temp_path)

    @pytest.fixture
    def sample_device(self):
        """Create a sample device for testing."""
        return Device(
            id=1,
            host="example.com",
            ip="192.168.1.1",
            snmp_group="public",
            alive=True,
            snmp=True,
            ssh=True,
            mysql=False,
            mysql_user="user",
            mysql_password="password",
            uname="Linux",
            errors=["Error 1"],
            scanned=True,
        )

    def test_init_file_exists(self, temp_file):
        """Test that a JsonFileRepository can be initialized with an existing file."""
        repo = JsonFileRepository(temp_file)
        assert repo.file_path == temp_file

    def test_init_file_not_exists(self):
        """Test that a JsonFileRepository creates a file if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "nonexistent.json")
            repo = JsonFileRepository(file_path)
            assert os.path.exists(file_path)
            with open(file_path, "r", encoding="utf-8") as f:
                assert f.read() == "{}"

    def test_init_file_invalid_json(self):
        """Test that a JsonFileRepository handles invalid JSON."""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(b"invalid json")
            temp_path = temp.name

        try:
            repo = JsonFileRepository(temp_path)
            with open(temp_path, "r", encoding="utf-8") as f:
                assert f.read() == "{}"
        finally:
            os.unlink(temp_path)

    def test_save_and_get(self, temp_file, sample_device):
        """Test that a device can be saved and retrieved."""
        repo = JsonFileRepository(temp_file)
        repo.save(sample_device)

        # Check that the device was saved to the file
        with open(temp_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert f"device:{sample_device.id}" in data
            assert data[f"device:{sample_device.id}"] == sample_device.to_dict()

        # Check that the device can be retrieved
        retrieved_device = repo.get(sample_device.id)
        assert retrieved_device is not None
        assert retrieved_device.id == sample_device.id
        assert retrieved_device.host == sample_device.host
        assert retrieved_device.ip == sample_device.ip
        assert retrieved_device.alive == sample_device.alive
        assert retrieved_device.snmp == sample_device.snmp
        assert retrieved_device.ssh == sample_device.ssh
        assert retrieved_device.mysql == sample_device.mysql
        assert retrieved_device.errors == sample_device.errors

    def test_get_not_found(self, temp_file):
        """Test that None is returned when a device is not found."""
        repo = JsonFileRepository(temp_file)
        device = repo.get(999)
        assert device is None

    def test_get_fallback(self, temp_file, sample_device):
        """Test that the fallback method works when ijson fails."""
        repo = JsonFileRepository(temp_file)
        repo.save(sample_device)

        # Mock ijson.parse to raise an exception
        with patch("ijson.parse", side_effect=Exception("Test error")):
            retrieved_device = repo.get(sample_device.id)
            assert retrieved_device is not None
            assert retrieved_device.id == sample_device.id

    def test_get_all(self, temp_file):
        """Test that all devices can be retrieved."""
        repo = JsonFileRepository(temp_file)
        device1 = Device(id=1, host="example1.com", ip="192.168.1.1")
        device2 = Device(id=2, host="example2.com", ip="192.168.1.2")
        repo.save(device1)
        repo.save(device2)

        devices = repo.get_all()
        assert len(devices) == 2
        assert any(d.id == 1 for d in devices)
        assert any(d.id == 2 for d in devices)

    def test_get_all_fallback(self, temp_file):
        """Test that the fallback method works when ijson fails."""
        repo = JsonFileRepository(temp_file)
        device1 = Device(id=1, host="example1.com", ip="192.168.1.1")
        device2 = Device(id=2, host="example2.com", ip="192.168.1.2")
        repo.save(device1)
        repo.save(device2)

        # Mock ijson.parse to raise an exception
        with patch("ijson.parse", side_effect=Exception("Test error")):
            devices = repo.get_all()
            assert len(devices) == 2
            assert any(d.id == 1 for d in devices)
            assert any(d.id == 2 for d in devices)

    def test_delete(self, temp_file, sample_device):
        """Test that a device can be deleted."""
        repo = JsonFileRepository(temp_file)
        repo.save(sample_device)

        # Check that the device exists
        assert repo.get(sample_device.id) is not None

        # Delete the device
        repo.delete(sample_device.id)

        # Check that the device was deleted
        assert repo.get(sample_device.id) is None

        # Check that the device was deleted from the file
        with open(temp_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert f"device:{sample_device.id}" not in data

    def test_delete_not_found(self, temp_file):
        """Test that deleting a nonexistent device doesn't raise an error."""
        repo = JsonFileRepository(temp_file)
        repo.delete(999)  # Should not raise an error

    def test_clear_all(self, temp_file, sample_device):
        """Test that all devices can be cleared."""
        repo = JsonFileRepository(temp_file)
        repo.save(sample_device)

        # Check that the device exists
        assert repo.get(sample_device.id) is not None

        # Clear all devices
        repo.clear_all()

        # Check that the device was deleted
        assert repo.get(sample_device.id) is None

        # Check that the file contains an empty JSON object
        with open(temp_file, "r", encoding="utf-8") as f:
            assert f.read() == "{}"

    def test_save_io_error(self, sample_device):
        """Test that an IOError is handled when saving a device."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "test.json")
            repo = JsonFileRepository(file_path)

            # Make the file read-only
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("{}")
            os.chmod(file_path, 0o444)  # Read-only

            # Try to save a device
            with pytest.raises(IOError):
                repo.save(sample_device)

            # Restore permissions for cleanup
            os.chmod(file_path, 0o644)

    def test_get_io_error(self):
        """Test that an IOError is handled when retrieving a device."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "nonexistent.json")
            repo = JsonFileRepository(file_path)

            # Remove the file to simulate an IOError
            os.unlink(file_path)

            # Try to get a device
            device = repo.get(1)
            assert device is None

    def test_get_all_io_error(self):
        """Test that an IOError is handled when retrieving all devices."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "nonexistent.json")
            repo = JsonFileRepository(file_path)

            # Remove the file to simulate an IOError
            os.unlink(file_path)

            # Try to get all devices
            devices = repo.get_all()
            assert devices == []

    def test_delete_io_error(self):
        """Test that an IOError is handled when deleting a device."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "test.json")
            repo = JsonFileRepository(file_path)

            # Make the file read-only
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("{}")
            os.chmod(file_path, 0o444)  # Read-only

            # Try to delete a device
            with pytest.raises(IOError):
                repo.delete(1)

            # Restore permissions for cleanup
            os.chmod(file_path, 0o644)

    def test_clear_all_io_error(self):
        """Test that an IOError is handled when clearing all devices."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "test.json")
            repo = JsonFileRepository(file_path)

            # Make the file read-only
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("{}")
            os.chmod(file_path, 0o444)  # Read-only

            # Try to clear all devices
            with pytest.raises(IOError):
                repo.clear_all()

            # Restore permissions for cleanup
            os.chmod(file_path, 0o644)
