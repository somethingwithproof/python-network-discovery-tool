"""Tests for the improved RedisRepository class."""

import json
import pytest
import redis
from unittest.mock import MagicMock, patch

from network_discovery.domain.device import Device
from improvements.redis_repository_improved import RedisRepository


class TestRedisRepository:
    """Tests for the RedisRepository class."""

    @pytest.fixture
    def mock_redis(self, mock_redis):
        """Create a mock Redis client."""
        with patch("redis.Redis") as mock_redis:
            mock_instance = MagicMock()
            mock_redis.return_value = mock_instance
            yield mock_instance

    @pytest.fixture
    def repository(self, mock_redis):
        """Create a RedisRepository with a mock Redis client."""
        return RedisRepository(host="localhost", port=6379, db=0)

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

    def test_init(self, mock_redis):
        """Test that a RedisRepository can be initialized."""
        repo = RedisRepository(host="testhost", port=1234, db=5)
        mock_redis.assert_called_once_with(
            host="testhost", port=1234, db=5, decode_responses=True
        )
        assert repo.device_set_key == "devices:all"

    def test_save(self, repository, mock_redis, sample_device):
        """Test that a device can be saved to the repository."""
        repository.save(sample_device)

        # Check that the device was saved to Redis
        mock_redis.set.assert_called_once_with(
            f"device:{sample_device.id}", json.dumps(sample_device.to_dict())
        )
        # Check that the device ID was added to the set of all devices
        mock_redis.sadd.assert_called_once_with(
            repository.device_set_key, sample_device.id
        )

    def test_save_redis_error(self, repository, mock_redis, sample_device):
        """Test that a RedisError is handled when saving a device."""
        mock_redis.set.side_effect = redis.RedisError("Test error")

        with pytest.raises(redis.RedisError):
            repository.save(sample_device)

    def test_get(self, repository, mock_redis, sample_device, device, device, device, device, device, device, device,
                 device, device):
        """Test that a device can be retrieved from the repository."""
        # Setup mock to return device data
        mock_redis.get.return_value = json.dumps(sample_device.to_dict())

        # Get the device
        device = repository.get(sample_device.id)

        # Check that Redis.get was called with the correct key
        mock_redis.get.assert_called_once_with(f"device:{sample_device.id}")

        # Check that the device was retrieved correctly
        assert device is not None
        assert device.id == sample_device.id
        assert device.host == sample_device.host
        assert device.ip == sample_device.ip
        assert device.alive == sample_device.alive
        assert device.snmp == sample_device.snmp
        assert device.ssh == sample_device.ssh
        assert device.mysql == sample_device.mysql
        assert device.errors == sample_device.errors

    def test_get_not_found(self, repository, mock_redis, device):
        """Test that None is returned when a device is not found."""
        # Setup mock to return None
        mock_redis.get.return_value = None

        # Get the device
        device = repository.get(1)

        # Check that Redis.get was called with the correct key
        mock_redis.get.assert_called_once_with("device:1")

        # Check that None was returned
        assert device is None

    def test_get_redis_error(self, repository, mock_redis):
        """Test that a RedisError is handled when retrieving a device."""
        mock_redis.get.side_effect = redis.RedisError("Test error")

        with pytest.raises(redis.RedisError):
            repository.get(1)

    def test_get_json_error(self, repository, mock_redis, device):
        """Test that a JSONDecodeError is handled when retrieving a device."""
        # Setup mock to return invalid JSON
        mock_redis.get.return_value = "invalid json"

        # Get the device
        device = repository.get(1)

        # Check that None was returned
        assert device is None

    def test_get_all(self, repository, mock_redis, sample_device):
        """Test that all devices can be retrieved from the repository."""
        # Setup mock to return device IDs
        mock_redis.smembers.return_value = {str(sample_device.id)}
        # Setup mock to return device data
        mock_redis.get.return_value = json.dumps(sample_device.to_dict())

        # Get all devices
        devices = repository.get_all()

        # Check that Redis.smembers was called with the correct key
        mock_redis.smembers.assert_called_once_with(repository.device_set_key)
        # Check that Redis.get was called with the correct key
        mock_redis.get.assert_called_once_with(f"device:{sample_device.id}")

        # Check that the devices were retrieved correctly
        assert len(devices) == 1
        assert devices[0].id == sample_device.id
        assert devices[0].host == sample_device.host
        assert devices[0].ip == sample_device.ip

    def test_get_all_redis_error(self, repository, mock_redis):
        """Test that a RedisError is handled when retrieving all devices."""
        mock_redis.smembers.side_effect = redis.RedisError("Test error")

        with pytest.raises(redis.RedisError):
            repository.get_all()

    def test_delete(self, repository, mock_redis):
        """Test that a device can be deleted from the repository."""
        repository.delete(1)

        # Check that Redis.delete was called with the correct key
        mock_redis.delete.assert_called_once_with("device:1")
        # Check that Redis.srem was called with the correct key and value
        mock_redis.srem.assert_called_once_with(repository.device_set_key, 1)

    def test_delete_redis_error(self, repository, mock_redis):
        """Test that a RedisError is handled when deleting a device."""
        mock_redis.delete.side_effect = redis.RedisError("Test error")

        with pytest.raises(redis.RedisError):
            repository.delete(1)

    def test_clear_all(self, repository, mock_redis):
        """Test that all devices can be cleared from the repository."""
        # Setup mock to return device IDs
        mock_redis.smembers.return_value = {"1", "2", "3"}

        repository.clear_all()

        # Check that Redis.smembers was called with the correct key
        mock_redis.smembers.assert_called_once_with(repository.device_set_key)
        # Check that Redis.delete was called for each device
        assert mock_redis.delete.call_count == 4  # 3 devices + 1 set
        # Check that the set of all devices was deleted
        mock_redis.delete.assert_any_call(repository.device_set_key)

    def test_clear_all_redis_error(self, repository, mock_redis):
        """Test that a RedisError is handled when clearing all devices."""
        mock_redis.smembers.side_effect = redis.RedisError("Test error")

        with pytest.raises(redis.RedisError):
            repository.clear_all()
