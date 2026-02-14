"""Tests for the DeviceManager class."""

# pytest is implicitly used for assertions
from network_discovery.domain.device import Device
from network_discovery.domain.device_manager import DeviceManager


class TestDeviceManager:
    """Tests for the DeviceManager class."""

    def test_init(self):
        """Test initializing a device manager."""
        manager = DeviceManager()
        assert len(manager) == 0
        assert manager.get_all_devices() == []

    def test_add_device(self):
        """Test adding a device to the manager."""
        manager = DeviceManager()
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        manager.add_device(device)
        assert len(manager) == 1
        assert manager.get_device(1) == device

    def test_remove_device(self):
        """Test removing a device from the manager."""
        manager = DeviceManager()
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        manager.add_device(device)
        assert len(manager) == 1
        manager.remove_device(1)
        assert len(manager) == 0
        assert manager.get_device(1) is None

    def test_get_device(self):
        """Test getting a device by ID."""
        manager = DeviceManager()
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        manager.add_device(device)
        assert manager.get_device(1) == device
        assert manager.get_device(2) is None

    def test_get_all_devices(self):
        """Test getting all devices."""
        manager = DeviceManager()
        device1 = Device(id=1, host="example1.com", ip="192.168.1.1")
        device2 = Device(id=2, host="example2.com", ip="192.168.1.2")
        manager.add_device(device1)
        manager.add_device(device2)
        devices = manager.get_all_devices()
        assert len(devices) == 2
        assert device1 in devices
        assert device2 in devices

    def test_devices_property(self):
        """Test the devices property."""
        manager = DeviceManager()
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        manager.add_device(device)
        assert manager.devices == [device]

    def test_iter(self):
        """Test iterating over devices."""
        manager = DeviceManager()
        device1 = Device(id=1, host="example1.com", ip="192.168.1.1")
        device2 = Device(id=2, host="example2.com", ip="192.168.1.2")
        manager.add_device(device1)
        manager.add_device(device2)
        devices = list(manager)
        assert len(devices) == 2
        assert device1 in devices
        assert device2 in devices

    def test_to_dict(self):
        """Test converting to a list of dictionaries."""
        manager = DeviceManager()
        device1 = Device(id=1, host="example1.com", ip="192.168.1.1")
        device2 = Device(id=2, host="example2.com", ip="192.168.1.2")
        manager.add_device(device1)
        manager.add_device(device2)
        dict_list = manager.to_dict()
        assert len(dict_list) == 2
        assert any(d["id"] == 1 and d["host"] == "example1.com" for d in dict_list)
        assert any(d["id"] == 2 and d["host"] == "example2.com" for d in dict_list)

    def test_from_dict(self):
        """Test creating from a list of dictionaries."""
        dict_list = [
            {
                "id": 1,
                "host": "example1.com",
                "ip": "192.168.1.1",
                "alive": True,
                "snmp": True,
                "ssh": False,
                "mysql": True,
                "scanned": True,
            },
            {
                "id": 2,
                "host": "example2.com",
                "ip": "192.168.1.2",
                "alive": False,
                "snmp": False,
                "ssh": False,
                "mysql": False,
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
        assert device2.errors == ["Error"]
        assert device2.scanned
