"""Repository implementations.

This module provides implementations of the DeviceRepositoryService interface.
"""

import json
import logging
import os
from typing import List, Optional, Dict, Any

import redis

from network_discovery.domain.device import Device
from network_discovery.application.interfaces import DeviceRepositoryService

# Setup logging
logger = logging.getLogger(__name__)


class JsonFileRepository(DeviceRepositoryService):
    """Implementation of DeviceRepositoryService using a JSON file."""

    def __init__(self, file_path: str) -> None:
        """Initialize a new JsonFileRepository.

        Args:
            file_path: The path to the JSON file.
        """
        self.file_path = file_path
        self.data: Dict[str, Any] = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """Load data from the JSON file.

        Returns:
            The data loaded from the file.
        """
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as file:
                    return json.load(file)
            return {}
        except json.JSONDecodeError as e:
            logger.error("Error decoding JSON: %s", e)
            return {}

    def _save_data(self) -> None:
        """Save data to the JSON file."""
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

    def save(self, device: Device) -> None:
        """Save a device to the repository.

        Args:
            device: The device to save.
        """
        self.data[f"device:{device.id}"] = device.to_dict()
        self._save_data()

    def get(self, device_id: int) -> Optional[Device]:
        """Get a device from the repository by its ID.

        Args:
            device_id: The ID of the device to retrieve.

        Returns:
            The device if found, None otherwise.
        """
        device_data = self.data.get(f"device:{device_id}")
        if device_data:
            return Device.from_dict(device_data)
        return None

    def get_all(self) -> List[Device]:
        """Get all devices from the repository.

        Returns:
            A list of all devices.
        """
        devices = []
        for key, value in self.data.items():
            if key.startswith("device:"):
                devices.append(Device.from_dict(value))
        return devices

    def delete(self, device_id: int) -> None:
        """Delete a device from the repository by its ID.

        Args:
            device_id: The ID of the device to delete.
        """
        key = f"device:{device_id}"
        if key in self.data:
            del self.data[key]
            self._save_data()


class RedisRepository(DeviceRepositoryService):
    """Implementation of DeviceRepositoryService using Redis."""

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0) -> None:
        """Initialize a new RedisRepository.

        Args:
            host: The Redis host.
            port: The Redis port.
            db: The Redis database number.
        """
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def save(self, device: Device) -> None:
        """Save a device to the repository.

        Args:
            device: The device to save.
        """
        key = f"device:{device.id}"
        self.redis.set(key, json.dumps(device.to_dict()))

    def get(self, device_id: int) -> Optional[Device]:
        """Get a device from the repository by its ID.

        Args:
            device_id: The ID of the device to retrieve.

        Returns:
            The device if found, None otherwise.
        """
        key = f"device:{device_id}"
        device_data = self.redis.get(key)
        if device_data:
            return Device.from_dict(json.loads(device_data))
        return None

    def get_all(self) -> List[Device]:
        """Get all devices from the repository.

        Returns:
            A list of all devices.
        """
        devices = []
        for key in self.redis.keys("device:*"):
            device_data = self.redis.get(key)
            if device_data:
                devices.append(Device.from_dict(json.loads(device_data)))
        return devices

    def delete(self, device_id: int) -> None:
        """Delete a device from the repository by its ID.

        Args:
            device_id: The ID of the device to delete.
        """
        key = f"device:{device_id}"
        self.redis.delete(key)
