"""Tests for the RedisRepository class."""

import json
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
import redis

from network_discovery.domain.device import Device
from network_discovery.infrastructure.repository import RedisRepository


class TestRedisRepository:
    """Tests for the RedisRepository class."""

    @pytest.fixture
    def mock_redis(self):
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

    def test_save(self, repository, sample_device, mock_redis):
        """Test that a device can be saved to Redis."""
        repository.save(sample_device)
        mock_redis.set.assert_called_once_with(
            "device:1", json.dumps(sample_device.to_dict())
        )

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
        mock_redis.keys.return_value = ["device:1", "device:2"]
        mock_redis.get.side_effect = [
            json.dumps(sample_device.to_dict()),
            json.dumps(sample_device.replace(id=2).to_dict()),
        ]
        devices = repository.get_all()
        assert len(devices) == 2
        assert devices[0].id == 1
        assert devices[1].id == 2
        mock_redis.keys.assert_called_once_with("device:*")
        assert mock_redis.get.call_count == 2

    def test_delete(self, repository, mock_redis):
        """Test that a device can be deleted from Redis."""
        repository.delete(1)
        mock_redis.delete.assert_called_once_with("device:1")

    def test_clear(self, repository, mock_redis):
        """Test that all devices can be cleared from Redis."""
        mock_redis.keys.return_value = ["device:1", "device:2"]
        repository.clear()
        mock_redis.delete.assert_called_once_with("device:1", "device:2")
        mock_redis.keys.assert_called_once_with("device:*")

    def test_clear_empty(self, repository, mock_redis):
        """Test that no error occurs when clearing with no devices."""
        mock_redis.keys.return_value = []
        repository.clear()
        mock_redis.delete.assert_not_called()
        mock_redis.keys.assert_called_once_with("device:*")

    def test_count(self, repository, mock_redis):
        """Test that the number of devices can be counted."""
        mock_redis.keys.return_value = ["device:1", "device:2"]
        count = repository.count()
        assert count == 2
        mock_redis.keys.assert_called_once_with("device:*")
