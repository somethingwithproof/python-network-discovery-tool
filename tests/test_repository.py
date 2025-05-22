"""Tests for repository implementations."""

import json
import os
import tempfile
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch

import pytest
import redis
from redis.exceptions import RedisError

from network_discovery.domain.device import Device
from network_discovery.infrastructure.repository import JsonFileRepository
from network_discovery.infrastructure.repository import RedisRepository


@pytest.fixture
def temp_file():
    """Create a temporary file for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file_path = tmp_file.name
        # Write empty JSON object
        tmp_file.write(b"{}")
        tmp_file.flush()
        yield tmp_file_path
        os.unlink(tmp_file_path)


@pytest.fixture
def json_repository(temp_file):
    """Create a JsonFileRepository with a temporary file."""
    return JsonFileRepository(temp_file)


@pytest.fixture
def device():
    """Create a test device."""
    return Device(
        id=1,
        host="example.com",
        ip="192.168.1.1",
        snmp_group="public",
        alive=True,
        snmp=True,
        ssh=True,
        mysql=False,
        mysql_user="",
        mysql_password="",
        uname="Linux test 5.4.0-42-generic",
        errors=("Test error",),
        scanned=True,
    )


@pytest.fixture
def mock_redis():
    """Mock Redis client for testing."""
    with patch("redis.Redis") as mock_redis_cls:
        mock_instance = MagicMock()
        mock_redis_cls.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def redis_repository(mock_redis):
    """Create a RedisRepository with a mocked Redis client."""
    return RedisRepository(host="localhost", port=6379, db=0)


class TestJsonFileRepository:
    """Tests for the JsonFileRepository class."""

    def test_init_with_new_file(self):
        """Test initializing with a new file path."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = os.path.join(tmp_dir, "nonexistent", "test.json")
            repository = JsonFileRepository(file_path)

            # Check if the directory was created
            assert os.path.exists(os.path.dirname(file_path))
            # Check if the file was created with empty JSON object
            assert os.path.exists(file_path)
            with open(file_path, "r") as f:
                content = f.read()
                assert content == "{}"

    def test_init_with_invalid_json(self):
        """Test initializing with an invalid JSON file."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"invalid json content")
            tmp_file.flush()

            # Initialize repository, which should fix the invalid file
            repository = JsonFileRepository(tmp_file.name)

            # Check if the file was rewritten with empty JSON object
            with open(tmp_file.name, "r") as f:
                content = f.read()
                assert content == "{}"

            os.unlink(tmp_file.name)

    def test_save_device(self, json_repository, device):
        """Test saving a device to the repository."""
        json_repository.save(device)

        # Verify the device was saved correctly
        saved_device = json_repository.get(device.id)
        assert saved_device is not None
        assert saved_device.id == device.id
        assert saved_device.host == device.host
        assert saved_device.ip == device.ip
        assert saved_device.alive == device.alive

    def test_get_device(self, json_repository, device):
        """Test getting a device from the repository."""
        # Save a device first
        json_repository.save(device)

        # Get the device and verify it matches
        retrieved_device = json_repository.get(device.id)
        assert retrieved_device is not None
        assert retrieved_device.id == device.id
        assert retrieved_device.host == device.host

    def test_get_nonexistent_device(self, json_repository):
        """Test getting a device that doesn't exist."""
        retrieved_device = json_repository.get(999)
        assert retrieved_device is None

    def test_get_all_devices(self, json_repository, device):
        """Test getting all devices from the repository."""
        # Save multiple devices
        device2 = device.replace(id=2, host="example2.com", ip="192.168.1.2")
        json_repository.save(device)
        json_repository.save(device2)

        # Get all devices and verify they match
        devices = json_repository.get_all()
        assert len(devices) == 2
        device_ids = [d.id for d in devices]
        assert 1 in device_ids
        assert 2 in device_ids

    def test_get_all_empty(self, json_repository):
        """Test getting all devices from an empty repository."""
        devices = json_repository.get_all()
        assert len(devices) == 0

    def test_delete_device(self, json_repository, device):
        """Test deleting a device from the repository."""
        # Save a device first
        json_repository.save(device)

        # Delete the device
        json_repository.delete(device.id)

        # Verify the device was deleted
        assert json_repository.get(device.id) is None

    def test_delete_nonexistent_device(self, json_repository):
        """Test deleting a device that doesn't exist."""
        # Should not raise an exception
        json_repository.delete(999)

    def test_clear_all(self, json_repository, device):
        """Test clearing all devices from the repository."""
        # Save multiple devices
        device2 = device.replace(id=2, host="example2.com", ip="192.168.1.2")
        json_repository.save(device)
        json_repository.save(device2)

        # Clear all devices
        json_repository.clear_all()

        # Verify all devices were deleted
        devices = json_repository.get_all()
        assert len(devices) == 0

    def test_save_with_file_error(self, device):
        """Test saving a device with a file error."""
        with patch("builtins.open", side_effect=IOError("Test IO Error")):
            repository = JsonFileRepository("test.json")
            with pytest.raises(IOError):
                repository.save(device)

    def test_get_with_file_error(self, json_repository, device):
        """Test getting a device with a file error."""
        # Save a device first to ensure the file exists
        json_repository.save(device)

        # Patch the open function to raise an error
        with patch("builtins.open", side_effect=IOError("Test IO Error")):
            # Should return None when encountering an error in both primary and fallback methods
            with patch.object(
                json_repository,
                "_get_fallback",
                side_effect=IOError("Fallback error"),
            ):
                retrieved_device = json_repository.get(device.id)
                assert retrieved_device is None

    def test_fallback_methods(self, json_repository, device):
        """Test fallback methods for get and get_all."""
        # Save a device first
        json_repository.save(device)

        # Test _get_fallback
        with patch("ijson.parse", side_effect=Exception("ijson error")):
            retrieved_device = json_repository.get(device.id)
            assert retrieved_device is not None
            assert retrieved_device.id == device.id

        # Test _get_all_fallback
        with patch("ijson.parse", side_effect=Exception("ijson error")):
            devices = json_repository.get_all()
            assert len(devices) == 1
            assert devices[0].id == device.id


class TestRedisRepository:
    """Tests for the RedisRepository class."""

    def test_init(self, mock_redis):
        """Test initializing the repository."""
        repository = RedisRepository(host="testhost", port=1234, db=2)
        # Verify Redis client was initialized with correct parameters
        from redis import Redis

        Redis.assert_called_once_with(
            host="testhost", port=1234, db=2, decode_responses=True
        )

    def test_save_device(self, redis_repository, device, mock_redis):
        """Test saving a device to the repository."""
        redis_repository.save(device)

        # Verify the Redis client was called with correct commands
        mock_redis.set.assert_called_once()
        # First arg should be the key
        assert mock_redis.set.call_args[0][0] == f"device:{device.id}"
        # Second arg should be the JSON-encoded device data
        assert isinstance(mock_redis.set.call_args[0][1], str)

        # Verify the device ID was added to the set
        mock_redis.sadd.assert_called_once_with(
            redis_repository.device_set_key, device.id
        )

    def test_get_device(self, redis_repository, device, mock_redis):
        """Test getting a device from the repository."""
        # Mock Redis get to return device data
        device_data = json.dumps(device.to_dict())
        mock_redis.get.return_value = device_data

        # Get the device
        retrieved_device = redis_repository.get(device.id)

        # Verify Redis client was called correctly
        mock_redis.get.assert_called_once_with(f"device:{device.id}")

        # Verify the retrieved device matches
        assert retrieved_device is not None
        assert retrieved_device.id == device.id
        assert retrieved_device.host == device.host

    def test_get_nonexistent_device(self, redis_repository, mock_redis):
        """Test getting a device that doesn't exist."""
        # Mock Redis get to return None
        mock_redis.get.return_value = None

        # Get a nonexistent device
        retrieved_device = redis_repository.get(999)

        # Verify Redis client was called correctly
        mock_redis.get.assert_called_once_with("device:999")

        # Verify None was returned
        assert retrieved_device is None

    def test_get_all_devices(self, redis_repository, device, mock_redis):
        """Test getting all devices from the repository."""
        # Mock Redis smembers to return device IDs
        mock_redis.smembers.return_value = {"1", "2"}

        # Mock Redis get to return device data for device 1
        device_data = json.dumps(device.to_dict())
        mock_redis.get.side_effect = [
            device_data,
            None,
        ]  # Return data for ID 1, None for ID 2

        # Get all devices
        devices = redis_repository.get_all()

        # Verify Redis client was called correctly
        mock_redis.smembers.assert_called_once_with(
            redis_repository.device_set_key
        )
        assert mock_redis.get.call_count == 2

        # Verify the right number of devices was returned (one valid, one invalid)
        assert len(devices) == 1
        assert devices[0].id == device.id

    def test_delete_device(self, redis_repository, mock_redis):
        """Test deleting a device from the repository."""
        # Delete a device
        redis_repository.delete(1)

        # Verify Redis client was called correctly
        mock_redis.delete.assert_called_once_with("device:1")
        mock_redis.srem.assert_called_once_with(
            redis_repository.device_set_key, 1
        )

    def test_clear_all(self, redis_repository, mock_redis):
        """Test clearing all devices from the repository."""
        # Mock Redis smembers to return device IDs
        mock_redis.smembers.return_value = {"1", "2"}

        # Clear all devices
        redis_repository.clear_all()

        # Verify Redis client was called correctly
        mock_redis.smembers.assert_called_once_with(
            redis_repository.device_set_key
        )
        assert mock_redis.delete.call_count == 3  # Two devices + the set itself

    def test_redis_error_handling(self, redis_repository, device, mock_redis):
        """Test error handling for Redis operations."""
        # Test save with Redis error
        mock_redis.set.side_effect = RedisError("Test Redis Error")
        with pytest.raises(RedisError):
            redis_repository.save(device)

        # Test get with Redis error
        mock_redis.set.side_effect = None  # Reset mock
        mock_redis.get.side_effect = RedisError("Test Redis Error")
        with pytest.raises(RedisError):
            redis_repository.get(device.id)

        # Test get with JSON decode error
        mock_redis.get.side_effect = None  # Reset mock
        mock_redis.get.return_value = "invalid json"
        retrieved_device = redis_repository.get(device.id)
        assert retrieved_device is None

        # Test get_all with Redis error
        mock_redis.smembers.side_effect = RedisError("Test Redis Error")
        with pytest.raises(RedisError):
            redis_repository.get_all()


class TestRepositoryIntegration:
    """Integration tests for repository implementations."""

    def test_json_repository_with_realistic_data(self, temp_file):
        """Test the JSON repository with realistic data volume."""
        # Create a repository
        repository = JsonFileRepository(temp_file)

        # Create and save multiple devices
        devices = []
        for i in range(1, 11):
            device = Device(
                id=i,
                host=f"host{i}.example.com",
                ip=f"192.168.1.{i}",
                alive=i % 2 == 0,  # Even IDs are alive
                ssh=i % 3 == 0,  # Every third device has SSH
                snmp=i % 4 == 0,  # Every fourth device has SNMP
                mysql=i % 5 == 0,  # Every fifth device has MySQL
                errors=(
                    (f"Error {i}",) if i % 2 == 1 else ()
                ),  # Odd IDs have errors
                scanned=True,
            )
            devices.append(device)
            repository.save(device)

        # Verify all devices were saved
        saved_devices = repository.get_all()
        assert len(saved_devices) == 10

        # Update some devices
        for i in range(1, 6):
            device = repository.get(i)
            if device:
                updated_device = device.replace(alive=not device.alive)
                repository.save(updated_device)

        # Delete some devices
        for i in range(6, 9):
            repository.delete(i)

        # Verify the updated state
        remaining_devices = repository.get_all()
        assert len(remaining_devices) == 7  # 10


"""Tests for the repository implementations."""

import json
import os
import tempfile

from network_discovery.domain.device import Device
from network_discovery.infrastructure.repository import JsonFileRepository


class TestJsonFileRepository:
    """Tests for the JsonFileRepository class."""

    def test_init(self):
        """Test repository initialization with a file path."""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            file_path = temp.name
        try:
            repo = JsonFileRepository(file_path)
            assert repo.file_path == file_path
            assert repo.data == {}
        finally:
            os.unlink(file_path)

    def test_save_and_get(self):
        """Test saving and retrieving a device."""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            file_path = temp.name
        try:
            repo = JsonFileRepository(file_path)
            device = Device(id=1, host="example.com", ip="192.168.1.1")
            repo.save(device)

            assert f"device:{device.id}" in repo.data
            assert repo.data[f"device:{device.id}"] == device.to_dict()

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert f"device:{device.id}" in data
                assert data[f"device:{device.id}"] == device.to_dict()

            retrieved = repo.get(device.id)
            assert retrieved is not None
            assert retrieved.id == device.id
            assert retrieved.host == device.host
            assert retrieved.ip == device.ip
        finally:
            os.unlink(file_path)

    def test_get_all(self):
        """Test retrieving all stored devices."""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            file_path = temp.name
        try:
            repo = JsonFileRepository(file_path)
            repo.save(Device(id=1, host="example1.com", ip="192.168.1.1"))
            repo.save(Device(id=2, host="example2.com", ip="192.168.1.2"))

            devices = repo.get_all()
            assert len(devices) == 2
            assert {d.id for d in devices} == {1, 2}
        finally:
            os.unlink(file_path)

    def test_delete(self):
        """Test deleting a device from the repository."""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            file_path = temp.name
        try:
            repo = JsonFileRepository(file_path)
            repo.save(Device(id=1, host="example1.com", ip="192.168.1.1"))
            repo.save(Device(id=2, host="example2.com", ip="192.168.1.2"))
            assert len(repo.get_all()) == 2

            repo.delete(1)
            devices = repo.get_all()
            assert len(devices) == 1
            assert devices[0].id == 2

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert "device:1" not in data
                assert "device:2" in data
        finally:
            os.unlink(file_path)

    def test_load_data_file_not_exists(self):
        """Test repo behavior when backing file is missing."""
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            file_path = temp.name

        repo = JsonFileRepository(file_path)
        assert repo.data == {}

        try:
            os.unlink(file_path)
        except FileNotFoundError:
            pass

    def test_load_data_invalid_json(self):
        """Test fallback to empty data on corrupted JSON file."""
        with tempfile.NamedTemporaryFile(delete=False, mode="wb") as temp:
            file_path = temp.name
            temp.write(b"invalid json")

        try:
            repo = JsonFileRepository(file_path)
            assert repo.data == {}
        finally:
            os.unlink(file_path)
