"""Tests for repository implementations."""

import contextlib
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


try:
    from redis.exceptions import RedisError

    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False
    RedisError = Exception  # type: ignore[assignment,misc]

from network_discovery.domain.device import Device
from network_discovery.infrastructure.repository import (
    JsonFileRepository,
    RedisRepository,
)


@pytest.fixture
def temp_file():
    """Create a temporary file for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file_path = tmp_file.name
        tmp_file.write(b"{}")
        tmp_file.flush()
        yield tmp_file_path
        Path(tmp_file_path).unlink()


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
            file_path = str(Path(tmp_dir) / "nonexistent" / "test.json")
            JsonFileRepository(file_path)

            p = Path(file_path)
            assert p.parent.exists()
            assert p.exists()
            assert p.read_text() == "{}"

    def test_init_with_invalid_json(self):
        """Test initializing with an invalid JSON file."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"invalid json content")
            tmp_file.flush()

            JsonFileRepository(tmp_file.name)

            assert Path(tmp_file.name).read_text() == "{}"

            Path(tmp_file.name).unlink()

    def test_save_device(self, json_repository, device):
        """Test saving a device to the repository."""
        json_repository.save(device)

        saved_device = json_repository.get(device.id)
        assert saved_device is not None
        assert saved_device.id == device.id
        assert saved_device.host == device.host
        assert saved_device.ip == device.ip
        assert saved_device.alive == device.alive

    def test_get_device(self, json_repository, device):
        """Test getting a device from the repository."""
        json_repository.save(device)

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
        device2 = device.replace(id=2, host="example2.com", ip="192.168.1.2")
        json_repository.save(device)
        json_repository.save(device2)

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
        json_repository.save(device)

        json_repository.delete(device.id)

        assert json_repository.get(device.id) is None

    def test_delete_nonexistent_device(self, json_repository):
        """Test deleting a device that doesn't exist."""
        json_repository.delete(999)

    def test_clear_all(self, json_repository, device):
        """Test clearing all devices from the repository."""
        device2 = device.replace(id=2, host="example2.com", ip="192.168.1.2")
        json_repository.save(device)
        json_repository.save(device2)

        json_repository.clear_all()

        devices = json_repository.get_all()
        assert len(devices) == 0

    def test_save_with_file_error(self, device, temp_file):
        """Test saving a device with a file error."""
        repository = JsonFileRepository(temp_file)
        with (
            patch.object(Path, "open", side_effect=OSError("Test IO Error")),
            pytest.raises(OSError),
        ):
            repository.save(device)

    def test_get_with_file_error(self, json_repository, device):
        """Test getting a device with a file error."""
        json_repository.save(device)

        with (
            patch.object(Path, "open", side_effect=OSError("Test IO Error")),
            patch.object(
                json_repository,
                "_get_fallback",
                return_value=None,
            ),
        ):
            retrieved_device = json_repository.get(device.id)
            assert retrieved_device is None

    def test_fallback_methods(self, json_repository, device):
        """Test fallback methods for get and get_all."""
        import ijson

        json_repository.save(device)

        with patch(
            "network_discovery.infrastructure.repository.ijson.parse",
            side_effect=ijson.JSONError("ijson error"),
        ):
            retrieved_device = json_repository.get(device.id)
            assert retrieved_device is not None
            assert retrieved_device.id == device.id

        with patch(
            "network_discovery.infrastructure.repository.ijson.parse",
            side_effect=ijson.JSONError("ijson error"),
        ):
            devices = json_repository.get_all()
            assert len(devices) == 1
            assert devices[0].id == device.id


@pytest.mark.skipif(not HAS_REDIS, reason="redis not installed")
class TestRedisRepository:
    """Tests for the RedisRepository class."""

    def test_init(self, mock_redis):
        """Test initializing the repository."""
        from redis import Redis

        RedisRepository(host="testhost", port=1234, db=2)
        Redis.assert_called_once_with(
            host="testhost", port=1234, db=2, decode_responses=True
        )

    def test_save_device(self, redis_repository, device, mock_redis):
        """Test saving a device to the repository."""
        redis_repository.save(device)

        mock_redis.set.assert_called_once()
        assert mock_redis.set.call_args[0][0] == f"device:{device.id}"
        assert isinstance(mock_redis.set.call_args[0][1], str)

        mock_redis.sadd.assert_called_once_with(
            redis_repository.device_set_key, device.id
        )

    def test_get_device(self, redis_repository, device, mock_redis):
        """Test getting a device from the repository."""
        device_data = json.dumps(device.to_dict())
        mock_redis.get.return_value = device_data

        retrieved_device = redis_repository.get(device.id)

        mock_redis.get.assert_called_once_with(f"device:{device.id}")

        assert retrieved_device is not None
        assert retrieved_device.id == device.id
        assert retrieved_device.host == device.host

    def test_get_nonexistent_device(self, redis_repository, mock_redis):
        """Test getting a device that doesn't exist."""
        mock_redis.get.return_value = None

        retrieved_device = redis_repository.get(999)

        mock_redis.get.assert_called_once_with("device:999")

        assert retrieved_device is None

    def test_get_all_devices(self, redis_repository, device, mock_redis):
        """Test getting all devices from the repository."""
        mock_redis.smembers.return_value = {"1", "2"}

        device_data = json.dumps(device.to_dict())
        mock_redis.get.side_effect = [
            device_data,
            None,
        ]

        devices = redis_repository.get_all()

        mock_redis.smembers.assert_called_once_with(redis_repository.device_set_key)
        assert mock_redis.get.call_count == 2

        assert len(devices) == 1
        assert devices[0].id == device.id

    def test_delete_device(self, redis_repository, mock_redis):
        """Test deleting a device from the repository."""
        redis_repository.delete(1)

        mock_redis.delete.assert_called_once_with("device:1")
        mock_redis.srem.assert_called_once_with(redis_repository.device_set_key, 1)

    def test_clear_all(self, redis_repository, mock_redis):
        """Test clearing all devices from the repository."""
        mock_redis.smembers.return_value = {"1", "2"}

        redis_repository.clear_all()

        mock_redis.smembers.assert_called_once_with(redis_repository.device_set_key)
        assert mock_redis.delete.call_count == 3

    def test_redis_error_handling(self, redis_repository, device, mock_redis):
        """Test error handling for Redis operations."""
        mock_redis.set.side_effect = RedisError("Test Redis Error")
        with pytest.raises(RedisError):
            redis_repository.save(device)

        mock_redis.set.side_effect = None
        mock_redis.get.side_effect = RedisError("Test Redis Error")
        with pytest.raises(RedisError):
            redis_repository.get(device.id)

        mock_redis.get.side_effect = None
        mock_redis.get.return_value = "invalid json"
        retrieved_device = redis_repository.get(device.id)
        assert retrieved_device is None

        mock_redis.smembers.side_effect = RedisError("Test Redis Error")
        with pytest.raises(RedisError):
            redis_repository.get_all()


class TestRepositoryIntegration:
    """Integration tests for repository implementations."""

    def test_json_repository_with_realistic_data(self, temp_file):
        """Test the JSON repository with realistic data volume."""
        repository = JsonFileRepository(temp_file)

        devices = []
        for i in range(1, 11):
            dev = Device(
                id=i,
                host=f"host{i}.example.com",
                ip=f"192.168.1.{i}",
                alive=i % 2 == 0,
                ssh=i % 3 == 0,
                snmp=i % 4 == 0,
                mysql=i % 5 == 0,
                errors=((f"Error {i}",) if i % 2 == 1 else ()),
                scanned=True,
            )
            devices.append(dev)
            repository.save(dev)

        saved_devices = repository.get_all()
        assert len(saved_devices) == 10

        for i in range(1, 6):
            dev = repository.get(i)
            if dev:
                updated_device = dev.replace(alive=not dev.alive)
                repository.save(updated_device)

        for i in range(6, 9):
            repository.delete(i)

        remaining_devices = repository.get_all()
        assert len(remaining_devices) == 7


class TestJsonFileRepositoryExtended:
    """Extended tests for the JsonFileRepository class."""

    def test_init(self):
        """Test repository initialization with a file path."""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            file_path = temp.name
        try:
            repo = JsonFileRepository(file_path)
            assert repo.file_path == file_path
            assert len(repo.get_all()) == 0
        finally:
            Path(file_path).unlink()

    def test_save_and_get(self):
        """Test saving and retrieving a device."""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            file_path = temp.name
        try:
            repo = JsonFileRepository(file_path)
            dev = Device(id=1, host="example.com", ip="192.168.1.1")
            repo.save(dev)

            retrieved = repo.get(dev.id)
            assert retrieved is not None
            assert retrieved.id == dev.id

            with Path(file_path).open(encoding="utf-8") as f:
                data = json.load(f)
                assert f"device:{dev.id}" in data
                assert data[f"device:{dev.id}"] == dev.to_dict()

            retrieved = repo.get(dev.id)
            assert retrieved is not None
            assert retrieved.id == dev.id
            assert retrieved.host == dev.host
            assert retrieved.ip == dev.ip
        finally:
            Path(file_path).unlink()

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
            Path(file_path).unlink()

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

            with Path(file_path).open(encoding="utf-8") as f:
                data = json.load(f)
                assert "device:1" not in data
                assert "device:2" in data
        finally:
            Path(file_path).unlink()

    def test_load_data_file_not_exists(self):
        """Test repo behavior when backing file is missing."""
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            file_path = temp.name

        repo = JsonFileRepository(file_path)
        assert len(repo.get_all()) == 0

        with contextlib.suppress(FileNotFoundError):
            Path(file_path).unlink()

    def test_load_data_invalid_json(self):
        """Test fallback to empty data on corrupted JSON file."""
        with tempfile.NamedTemporaryFile(delete=False, mode="wb") as temp:
            file_path = temp.name
            temp.write(b"invalid json")

        try:
            repo = JsonFileRepository(file_path)
            assert len(repo.get_all()) == 0
        finally:
            Path(file_path).unlink()
