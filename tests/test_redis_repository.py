"""Tests for the RedisRepository class."""

import importlib.util
import json
from unittest.mock import MagicMock, patch

import pytest

from network_discovery.domain.device import Device
from network_discovery.infrastructure.repository import RedisRepository


pytestmark = pytest.mark.skipif(
    importlib.util.find_spec("redis") is None, reason="redis not installed"
)


class TestRedisRepository:
    """Tests for the RedisRepository class."""

    @pytest.fixture
    def mock_redis(self):
        """Create a mock Redis client."""
        with patch(
            "network_discovery.infrastructure.repository.redis.Redis"
        ) as mock_redis_class:
            mock_instance = MagicMock()
            mock_redis_class.return_value = mock_instance
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
            errors=("Error 1",),
            scanned=True,
        )

    def test_init(self):
        """Test that a RedisRepository can be initialized."""
        with patch(
            "network_discovery.infrastructure.repository.redis.Redis"
        ) as mock_redis_class:
            mock_instance = MagicMock()
            mock_redis_class.return_value = mock_instance

            repo = RedisRepository(host="testhost", port=1234, db=5)

            mock_redis_class.assert_called_once_with(
                host="testhost", port=1234, db=5, decode_responses=True
            )
            assert repo.device_set_key == "devices:all"

    def test_save(self, repository, sample_device, mock_redis):
        """Test that a device can be saved to Redis."""
        repository.save(sample_device)

        # Check that the device data was saved
        mock_redis.set.assert_called_once_with(
            "device:1", json.dumps(sample_device.to_dict())
        )
        # Check that the device ID was added to the set
        mock_redis.sadd.assert_called_once_with("devices:all", sample_device.id)

    def test_get(self, repository, sample_device, mock_redis):
        """Test that a device can be retrieved from Redis."""
        mock_redis.get.return_value = json.dumps(sample_device.to_dict())
        device = repository.get(1)

        assert device.id == sample_device.id
        assert device.host == sample_device.host
        assert device.ip == sample_device.ip
        assert device.snmp_group == sample_device.snmp_group
        assert device.alive == sample_device.alive
        assert device.snmp == sample_device.snmp
        assert device.ssh == sample_device.ssh
        assert device.mysql == sample_device.mysql
        assert device.mysql_user == sample_device.mysql_user
        assert device.mysql_password == sample_device.mysql_password
        assert device.uname == sample_device.uname
        assert list(device.errors) == list(sample_device.errors)
        assert device.scanned == sample_device.scanned
        mock_redis.get.assert_called_once_with("device:1")

    def test_get_not_found(self, repository, mock_redis):
        """Test that None is returned when a device is not found."""
        mock_redis.get.return_value = None
        device = repository.get(1)
        assert device is None
        mock_redis.get.assert_called_once_with("device:1")

    def test_get_all(self, repository, sample_device, mock_redis):
        """Test that all devices can be retrieved from Redis."""
        # Mock smembers to return device IDs (as strings, as Redis returns them)
        mock_redis.smembers.return_value = {"1", "2"}

        # Create a second device
        device2_data = sample_device.to_dict()
        device2_data["id"] = 2

        # Mock get to return device data based on the key
        def mock_get(key):
            if key == "device:1":
                return json.dumps(sample_device.to_dict())
            elif key == "device:2":
                return json.dumps(device2_data)
            return None

        mock_redis.get.side_effect = mock_get

        devices = repository.get_all()

        assert len(devices) == 2
        mock_redis.smembers.assert_called_once_with("devices:all")
        assert mock_redis.get.call_count == 2

    def test_delete(self, repository, mock_redis):
        """Test that a device can be deleted from Redis."""
        repository.delete(1)
        mock_redis.delete.assert_called_once_with("device:1")
        mock_redis.srem.assert_called_once_with("devices:all", 1)

    def test_clear(self, repository, mock_redis):
        """Test that all devices can be cleared from Redis."""
        mock_redis.smembers.return_value = {"1", "2"}

        repository.clear()

        mock_redis.smembers.assert_called_once_with("devices:all")
        # Should delete each device and the set
        assert mock_redis.delete.call_count == 3  # device:1, device:2, devices:all

    def test_clear_empty(self, repository, mock_redis):
        """Test that no error occurs when clearing with no devices."""
        mock_redis.smembers.return_value = set()

        repository.clear()

        mock_redis.smembers.assert_called_once_with("devices:all")
        mock_redis.delete.assert_called_once_with("devices:all")

    def test_count(self, repository, mock_redis):
        """Test that the number of devices can be counted."""
        mock_redis.scard.return_value = 5

        count = repository.count()

        assert count == 5
        mock_redis.scard.assert_called_once_with("devices:all")
