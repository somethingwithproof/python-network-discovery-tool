"""Tests for the DeviceManager class."""

from network_discovery.domain.device import Device
from network_discovery.domain.device_manager import DeviceManager


class TestDeviceManager:
    """Tests for the DeviceManager class."""

    def test_init(self):
        """Test that a DeviceManager can be initialized."""
        manager = DeviceManager()
        assert manager.devices == []

    def test_add_device(self):
        """Test that a device can be added to the manager."""
        manager = DeviceManager()
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        manager.add_device(device)
        assert len(manager.devices) == 1
        assert manager.devices[0] == device

    def test_remove_device(self):
        """Test that a device can be removed from the manager."""
        manager = DeviceManager()
        device1 = Device(id=1, host="example1.com", ip="192.168.1.1")
        device2 = Device(id=2, host="example2.com", ip="192.168.1.2")
        manager.add_device(device1)
        manager.add_device(device2)
        assert len(manager.devices) == 2

        manager.remove_device(1)
        assert len(manager.devices) == 1
        assert manager.devices[0] == device2

    def test_get_device(self):
        """Test that a device can be retrieved by ID."""
        manager = DeviceManager()
        device1 = Device(id=1, host="example1.com", ip="192.168.1.1")
        device2 = Device(id=2, host="example2.com", ip="192.168.1.2")
        manager.add_device(device1)
        manager.add_device(device2)

        retrieved_device = manager.get_device(1)
        assert retrieved_device == device1

        retrieved_device = manager.get_device(2)
        assert retrieved_device == device2

        retrieved_device = manager.get_device(3)
        assert retrieved_device is None

    def test_to_dict(self):
        """Test that the manager can be converted to a list of dictionaries."""
        manager = DeviceManager()
        device1 = Device(id=1, host="example1.com", ip="192.168.1.1")
        device2 = Device(id=2, host="example2.com", ip="192.168.1.2")
        manager.add_device(device1)
        manager.add_device(device2)

        dict_list = manager.to_dict()
        assert len(dict_list) == 2
        assert dict_list[0] == device1.to_dict()
        assert dict_list[1] == device2.to_dict()

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
        assert len(manager.devices) == 2
        assert manager.devices[0].id == 1
        assert manager.devices[0].host == "example1.com"
        assert manager.devices[0].ip == "192.168.1.1"
        assert manager.devices[0].alive
        assert manager.devices[0].snmp
        assert not manager.devices[0].ssh
        assert manager.devices[0].mysql
        assert manager.devices[0].scanned

        assert manager.devices[1].id == 2
        assert manager.devices[1].host == "example2.com"
        assert manager.devices[1].ip == "192.168.1.2"
        assert not manager.devices[1].alive
        assert not manager.devices[1].snmp
        assert not manager.devices[1].ssh
        assert not manager.devices[1].mysql
        assert manager.devices[1].errors == ["Error"]
        assert manager.devices[1].scanned
