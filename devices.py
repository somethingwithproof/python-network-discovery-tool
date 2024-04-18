from typing import List, Dict
from device import Device

class DeviceManager:
    """Manages a list of devices."""

    def __init__(self):
        self.devices: List[Device] = []

    def add_device(self, device: Device) -> None:
        """Adds a device to the list."""
        self.devices.append(device)

    def remove_device(self, device_id: int) -> None:
        """Removes a device from the list by its ID."""
        self.devices = [device for device in self.devices if device.id != device_id]

    def get_device(self, device_id: int) -> Device:
        """Gets a device by its ID."""
        for device in self.devices:
            if device.id == device_id:
                return device
        return None

    def to_dict(self) -> List[Dict]:
        """Converts the list of devices to a list of dictionaries."""
        return [device.to_dict() for device in self.devices]

    @staticmethod
    def from_dict(devices_list: List[Dict]) -> 'DeviceManager':
        """Creates a DeviceManager from a list of dictionaries."""
        manager = DeviceManager()
        for device_dict in devices_list:
            manager.add_device(Device.from_dict(device_dict))
        return manager
