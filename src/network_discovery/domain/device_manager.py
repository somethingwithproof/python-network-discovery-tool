"""Improved device manager domain model.

This module defines an improved DeviceManager entity, which manages a collection of Device entities
using a dictionary for faster lookups.
"""

from typing import Dict, Iterator, List, Optional

from network_discovery.domain.device import Device


class DeviceManager:
    """Manages a collection of Device entities.

    This class provides methods to add, remove, and retrieve devices from a collection.
    It uses a dictionary for faster lookups by device ID.
    """

    def __init__(self) -> None:
        """Initialize a new DeviceManager with an empty dictionary of devices."""
        self.devices_dict: Dict[int, Device] = {}

    def add_device(self, device: Device) -> None:
        """Add a device to the collection.

        Args:
            device: The Device entity to add.
        """
        self.devices_dict[device.id] = device

    def remove_device(self, device_id: int) -> None:
        """Remove a device from the collection by its ID.

        Args:
            device_id: The ID of the device to remove.
        """
        if device_id in self.devices_dict:
            del self.devices_dict[device_id]

    def get_device(self, device_id: int) -> Optional[Device]:
        """Get a device by its ID.

        Args:
            device_id: The ID of the device to retrieve.

        Returns:
            The Device entity if found, None otherwise.
        """
        return self.devices_dict.get(device_id)

    def get_all_devices(self) -> List[Device]:
        """Get all devices in the collection.

        Returns:
            A list of all Device entities.
        """
        return list(self.devices_dict.values())

    @property
    def devices(self) -> List[Device]:
        """Get all devices in the collection.

        This property is provided for backward compatibility with the original DeviceManager.

        Returns:
            A list of all Device entities.
        """
        return self.get_all_devices()

    def __iter__(self) -> Iterator[Device]:
        """Iterate over all devices in the collection.

        Returns:
            An iterator over all Device entities.
        """
        return iter(self.devices_dict.values())

    def __len__(self) -> int:
        """Get the number of devices in the collection.

        Returns:
            The number of Device entities.
        """
        return len(self.devices_dict)

    def to_dict(self) -> List[Dict]:
        """Convert the collection of devices to a list of dictionaries.

        Returns:
            A list of dictionary representations of the devices.
        """
        return [device.to_dict() for device in self.devices_dict.values()]

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
