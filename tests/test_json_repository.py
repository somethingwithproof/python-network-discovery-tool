"""Tests for the JsonFileRepository class."""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import ijson
import pytest

from network_discovery.domain.device import Device
from network_discovery.infrastructure.repository import JsonFileRepository


class TestJsonFileRepository:
    """Tests for the JsonFileRepository class."""

    @pytest.fixture
    def temp_file(self):
        """Create a temporary file for testing."""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(b"{}")
            temp_path = temp.name
        yield temp_path
        Path(temp_path).unlink()

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
            errors=("Error 1",),
            scanned=True,
        )

    def test_init_file_exists(self, temp_file):
        """Test that a JsonFileRepository can be initialized with an existing file."""
        repo = JsonFileRepository(temp_file)
        assert repo.file_path == temp_file

    def test_init_file_not_exists(self):
        """Test that a JsonFileRepository creates a file if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = str(Path(temp_dir) / "nonexistent.json")
            JsonFileRepository(file_path)
            p = Path(file_path)
            assert p.exists()
            assert p.read_text(encoding="utf-8") == "{}"

    def test_init_file_invalid_json(self):
        """Test that a JsonFileRepository handles invalid JSON."""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(b"invalid json")
            temp_path = temp.name

        try:
            JsonFileRepository(temp_path)
            assert Path(temp_path).read_text(encoding="utf-8") == "{}"
        finally:
            Path(temp_path).unlink()

    def test_save_and_get(self, temp_file, sample_device):
        """Test that a device can be saved and retrieved."""
        repo = JsonFileRepository(temp_file)
        repo.save(sample_device)

        with Path(temp_file).open(encoding="utf-8") as f:
            data = json.load(f)
            assert f"device:{sample_device.id}" in data
            assert data[f"device:{sample_device.id}"] == sample_device.to_dict()

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
        result = repo.get(999)
        assert result is None

    def test_get_fallback(self, temp_file, sample_device):
        """Test that the fallback method works when ijson fails."""
        repo = JsonFileRepository(temp_file)
        repo.save(sample_device)

        with patch(
            "network_discovery.infrastructure.repository.ijson.parse",
            side_effect=ijson.JSONError("Test error"),
        ):
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

        with patch(
            "network_discovery.infrastructure.repository.ijson.parse",
            side_effect=ijson.JSONError("Test error"),
        ):
            devices = repo.get_all()
            assert len(devices) == 2
            assert any(d.id == 1 for d in devices)
            assert any(d.id == 2 for d in devices)

    def test_delete(self, temp_file, sample_device):
        """Test that a device can be deleted."""
        repo = JsonFileRepository(temp_file)
        repo.save(sample_device)

        assert repo.get(sample_device.id) is not None

        repo.delete(sample_device.id)

        assert repo.get(sample_device.id) is None

        with Path(temp_file).open(encoding="utf-8") as f:
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

        assert repo.get(sample_device.id) is not None

        repo.clear_all()

        assert repo.get(sample_device.id) is None
        assert Path(temp_file).read_text(encoding="utf-8") == "{}"

    @pytest.mark.skipif(os.geteuid() == 0, reason="Root can write to read-only files")
    def test_save_io_error(self, sample_device):
        """Test that an IOError is handled when saving a device."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = str(Path(temp_dir) / "test.json")
            repo = JsonFileRepository(file_path)

            p = Path(file_path)
            p.write_text("{}", encoding="utf-8")
            p.chmod(0o444)  # Read-only

            with pytest.raises(IOError):
                repo.save(sample_device)

            p.chmod(0o644)

    def test_get_io_error(self):
        """Test that an IOError is handled when retrieving a device."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = str(Path(temp_dir) / "nonexistent.json")
            repo = JsonFileRepository(file_path)

            Path(file_path).unlink()

            device = repo.get(1)
            assert device is None

    def test_get_all_io_error(self):
        """Test that an IOError is handled when retrieving all devices."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = str(Path(temp_dir) / "nonexistent.json")
            repo = JsonFileRepository(file_path)

            Path(file_path).unlink()

            devices = repo.get_all()
            assert devices == []

    @pytest.mark.skipif(os.geteuid() == 0, reason="Root can write to read-only files")
    def test_delete_io_error(self, sample_device):
        """Test that an IOError is handled when deleting a device."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = str(Path(temp_dir) / "test.json")
            repo = JsonFileRepository(file_path)

            repo.save(sample_device)

            Path(file_path).chmod(0o444)

            with pytest.raises(OSError):
                repo.delete(sample_device.id)

            Path(file_path).chmod(0o644)

    @pytest.mark.skipif(os.geteuid() == 0, reason="Root can write to read-only files")
    def test_clear_all_io_error(self):
        """Test that an IOError is handled when clearing all devices."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = str(Path(temp_dir) / "test.json")
            repo = JsonFileRepository(file_path)

            p = Path(file_path)
            p.write_text("{}", encoding="utf-8")
            p.chmod(0o444)

            with pytest.raises(IOError):
                repo.clear_all()

            p.chmod(0o644)
