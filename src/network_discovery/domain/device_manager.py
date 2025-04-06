"""Device manager domain model.

This module defines the DeviceManager entity, which manages a collection of Device entities.
"""

from typing import List, Dict, Optional
from .device import Device


class DeviceManager:
    """Manages a collection of Device entities.

    This class provides methods to add, remove, and retrieve devices from a collection.
    """

    def __init__(self) -> None:
        """Initialize a new DeviceManager with an empty list of devices."""
        self.devices: List[Device] = []

    def add_device(self, device: Device) -> None:
        """Add a device to the collection.

        Args:
            device: The Device entity to add.
        """
        self.devices.append(device)

    def remove_device(self, device_id: int) -> None:
        """Remove a device from the collection by its ID.

        Args:
            device_id: The ID of the device to remove.
        """
        self.devices = [device for device in self.devices if device.id != device_id]

    def get_device(self, device_id: int) -> Optional[Device]:
        """Get a device by its ID.

        Args:
            device_id: The ID of the device to retrieve.

        Returns:
            The Device entity if found, None otherwise.
        """
        for device in self.devices:
            if device.id == device_id:
                return device
        return None

    def to_dict(self) -> List[Dict]:
        """Convert the list of devices to a list of dictionaries.

        Returns:
            A list of dictionary representations of the devices.
        """
        return [device.to_dict() for device in self.devices]

    @classmethod
    def from_dict(cls, devices_list: List[Dict]) -> "DeviceManager":
        """Create a DeviceManager from a list of dictionaries.

        Args:
            devices_list: A list of dictionaries containing device attributes.

        Returns:
            A new DeviceManager instance with devices created from the dictionaries.
        """
        manager = cls()
        for device_dict in devices_list:
            manager.add_device(Device.from_dict(device_dict))
        return manager
