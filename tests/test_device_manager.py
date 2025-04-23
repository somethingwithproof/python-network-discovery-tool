"""Tests for the DeviceManager class."""

import pytest
from network_discovery.domain.device import Device
from network_discovery.domain.device_manager import DeviceManager


class TestDeviceManager:
    """Tests for the DeviceManager class."""

    @pytest.fixture
    def device1(self):
        """Create a test device."""
        return Device(id=1, host="example1.com", ip="192.168.1.1")

    @pytest.fixture
    def device2(self):
        """Create another test device."""
        return Device(id=2, host="example2.com", ip="192.168.1.2")

    def test_init(self):
        """Test that a DeviceManager can be initialized."""
        manager = DeviceManager()
        assert manager.devices_dict == {}
        assert manager.devices == []
        assert len(manager) == 0

    def test_add_device(self, device1):
        """Test that a device can be added to the manager."""
        manager = DeviceManager()
        manager.add_device(device1)
        assert manager.devices_dict[device1.id] == device1
        assert manager.devices == [device1]
        assert len(manager) == 1

    def test_add_multiple_devices(self, device1, device2):
        """Test that multiple devices can be added to the manager."""
        manager = DeviceManager()
        manager.add_device(device1)
        manager.add_device(device2)
        assert manager.devices_dict[device1.id] == device1
        assert manager.devices_dict[device2.id] == device2
        assert set(manager.devices) == {device1, device2}
        assert len(manager) == 2

    def test_remove_device(self, device1, device2):
        """Test that a device can be removed from the manager."""
        manager = DeviceManager()
        manager.add_device(device1)
        manager.add_device(device2)
        assert len(manager) == 2

        manager.remove_device(device1.id)
        assert device1.id not in manager.devices_dict
        assert device2.id in manager.devices_dict
        assert manager.devices == [device2]
        assert len(manager) == 1

    def test_remove_nonexistent_device(self):
        """Test that removing a nonexistent device doesn't raise an error."""
        manager = DeviceManager()
        manager.remove_device(999)  # Should not raise an error
        assert len(manager) == 0

    def test_get_device(self, device1, device2):
        """Test that a device can be retrieved by ID."""
        manager = DeviceManager()
        manager.add_device(device1)
        manager.add_device(device2)

        retrieved_device = manager.get_device(device1.id)
        assert retrieved_device == device1

        retrieved_device = manager.get_device(device2.id)
        assert retrieved_device == device2

        retrieved_device = manager.get_device(999)
        assert retrieved_device is None

    def test_get_all_devices(self, device1, device2):
        """Test that all devices can be retrieved."""
        manager = DeviceManager()
        manager.add_device(device1)
        manager.add_device(device2)

        all_devices = manager.get_all_devices()
        assert set(all_devices) == {device1, device2}
        assert len(all_devices) == 2

    def test_devices_property(self, device1, device2):
        """Test that the devices property returns all devices."""
        manager = DeviceManager()
        manager.add_device(device1)
        manager.add_device(device2)

        devices = manager.devices
        assert set(devices) == {device1, device2}
        assert len(devices) == 2

    def test_iteration(self, device1, device2):
        """Test that the manager can be iterated over."""
        manager = DeviceManager()
        manager.add_device(device1)
        manager.add_device(device2)

        devices = set()
        for device in manager:
            devices.add(device)

        assert devices == {device1, device2}

    def test_to_dict(self, device1, device2):
        """Test that the manager can be converted to a list of dictionaries."""
        manager = DeviceManager()
        manager.add_device(device1)
        manager.add_device(device2)

        dict_list = manager.to_dict()
        assert len(dict_list) == 2
        assert device1.to_dict() in dict_list
        assert device2.to_dict() in dict_list

    def test_from_dict(self):
        """Test that a manager can be created from a list of dictionaries."""
        dict_list = [
            {
                "id": 1,
                "host": "example1.com",
                "ip": "192.168.1.1",
                "snmp_group": "public",
                "alive": True,
                "snmp": True,
                "ssh": False,
                "mysql": True,
                "mysql_user": "",
                "mysql_password": "",
                "uname": "",
                "errors": [],
                "scanned": True,
            },
            {
                "id": 2,
                "host": "example2.com",
                "ip": "192.168.1.2",
                "snmp_group": "public",
                "alive": False,
                "snmp": False,
                "ssh": False,
                "mysql": False,
                "mysql_user": "",
                "mysql_password": "",
                "uname": "",
                "errors": ["Error"],
                "scanned": True,
            },
        ]

        manager = DeviceManager.from_dict(dict_list)
        assert len(manager) == 2

        device1 = manager.get_device(1)
        assert device1 is not None
        assert device1.id == 1
        assert device1.host == "example1.com"
        assert device1.ip == "192.168.1.1"
        assert device1.alive
        assert device1.snmp
        assert not device1.ssh
        assert device1.mysql
        assert device1.scanned

        device2 = manager.get_device(2)
        assert device2 is not None
        assert device2.id == 2
        assert device2.host == "example2.com"
        assert device2.ip == "192.168.1.2"
        assert not device2.alive
        assert not device2.snmp
        assert not device2.ssh
        assert not device2.mysql
        assert tuple(device2.errors) == ("Error",)
        assert device2.scanned
