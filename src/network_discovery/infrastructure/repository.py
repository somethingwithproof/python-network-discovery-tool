"""Repository implementations.

This module provides implementations of the DeviceRepositoryService interface.
"""

import json
import logging
import os
from typing import List, Optional

import ijson
import redis

from network_discovery.application.interfaces import DeviceRepositoryService
from network_discovery.domain.device import Device

# Setup logging
logger = logging.getLogger(__name__)


class JsonFileRepository(DeviceRepositoryService):
    """Implementation of DeviceRepositoryService using a JSON file.

    This implementation is optimized for large datasets by using streaming JSON parsing
    and incremental updates to the file.
    """

    def __init__(self, file_path: str) -> None:
        """Initialize a new JsonFileRepository.

        Args:
            file_path: The path to the JSON file.
        """
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Ensure that the JSON file exists and is valid.

        If the file doesn't exist, create it with an empty JSON object.
        If the file exists but is empty or invalid, initialize it with an empty JSON object.
        """
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write("{}")
        else:
            try:
                with open(self.file_path, "r", encoding="utf-8") as file:
                    # Just try to load the file to check if it's valid JSON
                    json.load(file)
            except (json.JSONDecodeError, IOError) as e:
                logger.error(
                    "Error reading JSON file: %s. Initializing with empty object.",
                    e,
                )
                with open(self.file_path, "w", encoding="utf-8") as file:
                    file.write("{}")

    def save(self, device: Device) -> None:
        """Save a device to the repository.

        Args:
            device: The device to save.
        """
        key = f"device:{device.id}"
        device_data = device.to_dict()

        try:
            # Load the current data
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Update the device data
            data[key] = device_data

            # Write the updated data back to the file
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            logger.debug("Device %s saved to JSON file", device.id)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(
                "Error saving device %s to JSON file: %s", device.id, e
            )
            raise

    def get(self, device_id: int) -> Optional[Device]:
        """Get a device from the repository by its ID.

        Args:
            device_id: The ID of the device to retrieve.

        Returns:
            The device if found, None otherwise.
        """
        key = f"device:{device_id}"

        try:
            # Use ijson to stream the JSON file and find the specific device
            with open(self.file_path, "rb") as file:
                for prefix, event, value in ijson.parse(file):
                    if prefix == key and event == "start_map":
                        # Found the device, now parse its data
                        device_data = {}
                        current_key = None

                        # Continue parsing until we reach the end of the device object
                        for p, e, v in ijson.parse(file):
                            if p == key and e == "end_map":
                                # End of the device object
                                break
                            elif e == "map_key":
                                current_key = v
                            elif current_key is not None:
                                device_data[current_key] = v
                                current_key = None

                        return Device.from_dict(device_data)

            # Device not found
            return None
        except (ijson.JSONError, IOError) as e:
            logger.error(
                "Error retrieving device %s from JSON file: %s", device_id, e
            )
            # Fall back to loading the entire file
            return self._get_fallback(device_id)

    def _get_fallback(self, device_id: int) -> Optional[Device]:
        """Fallback method to get a device by loading the entire file.

        Args:
            device_id: The ID of the device to retrieve.

        Returns:
            The device if found, None otherwise.
        """
        key = f"device:{device_id}"

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            device_data = data.get(key)
            if device_data:
                return Device.from_dict(device_data)
            return None
        except (json.JSONDecodeError, IOError) as e:
            logger.error(
                "Error in fallback retrieval of device %s: %s", device_id, e
            )
            return None

    def get_all(self) -> List[Device]:
        """Get all devices from the repository.

        Returns:
            A list of all devices.
        """
        devices = []

        try:
            # Use ijson to stream the JSON file and find all devices
            with open(self.file_path, "rb") as file:
                # Get all keys that start with "device:"
                device_keys = []
                for prefix, event, value in ijson.parse(file):
                    if event == "map_key" and value.startswith("device:"):
                        device_keys.append(value)

            # Get each device by its ID
            for key in device_keys:
                device_id = int(key.split(":")[1])
                device = self.get(device_id)
                if device:
                    devices.append(device)

            return devices
        except (ijson.JSONError, IOError) as e:
            logger.error("Error retrieving all devices from JSON file: %s", e)
            # Fall back to loading the entire file
            return self._get_all_fallback()

    def _get_all_fallback(self) -> List[Device]:
        """Fallback method to get all devices by loading the entire file.

        Returns:
            A list of all devices.
        """
        devices = []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            for key, value in data.items():
                if key.startswith("device:"):
                    try:
                        devices.append(Device.from_dict(value))
                    except Exception as e:
                        logger.error("Error creating device from data: %s", e)

            return devices
        except (json.JSONDecodeError, IOError) as e:
            logger.error("Error in fallback retrieval of all devices: %s", e)
            return []

    def delete(self, device_id: int) -> None:
        """Delete a device from the repository by its ID.

        Args:
            device_id: The ID of the device to delete.
        """
        key = f"device:{device_id}"

        try:
            # Load the current data
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Remove the device if it exists
            if key in data:
                del data[key]

                # Write the updated data back to the file
                with open(self.file_path, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4)

                logger.debug("Device %s deleted from JSON file", device_id)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(
                "Error deleting device %s from JSON file: %s", device_id, e
            )
            raise

    def clear_all(self) -> None:
        """Clear all devices from the repository.

        This is useful for testing and initialization.
        """
        try:
            # Write an empty JSON object to the file
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write("{}")

            logger.debug("All devices cleared from JSON file")
        except IOError as e:
            logger.error("Error clearing all devices from JSON file: %s", e)
            raise


class RedisRepository(DeviceRepositoryService):
    """Implementation of DeviceRepositoryService using Redis.

    This implementation uses Redis Sets to track device IDs, avoiding the use of the KEYS command
    which can be problematic in production environments with large datasets.
    """

    def __init__(
        self, host: str = "localhost", port: int = 6379, db: int = 0
    ) -> None:
        """Initialize a new RedisRepository.

        Args:
            host: The Redis host.
            port: The Redis port.
            db: The Redis database number.
        """
        self.redis = redis.Redis(
            host=host, port=port, db=db, decode_responses=True
        )
        self.device_set_key = (
            "devices:all"  # Key for the set containing all device IDs
        )

    def save(self, device: Device) -> None:
        """Save a device to the repository.

        Args:
            device: The device to save.
        """
        key = f"device:{device.id}"
        try:
            # Save the device data
            self.redis.set(key, json.dumps(device.to_dict()))
            # Add the device ID to the set of all devices
            self.redis.sadd(self.device_set_key, device.id)
            logger.debug("Device %s saved to Redis", device.id)
        except redis.RedisError as e:
            logger.error("Error saving device %s to Redis: %s", device.id, e)
            raise

    def get(self, device_id: int) -> Optional[Device]:
        """Get a device from the repository by its ID.

        Args:
            device_id: The ID of the device to retrieve.

        Returns:
            The device if found, None otherwise.
        """
        key = f"device:{device_id}"
        try:
            device_data = self.redis.get(key)
            if device_data:
                return Device.from_dict(json.loads(device_data))
            return None
        except redis.RedisError as e:
            logger.error(
                "Error retrieving device %s from Redis: %s", device_id, e
            )
            raise
        except json.JSONDecodeError as e:
            logger.error("Error decoding device %s data: %s", device_id, e)
            return None

    def get_all(self) -> List[Device]:
        """Get all devices from the repository.

        Returns:
            A list of all devices.
        """
        devices = []
        try:
            # Get all device IDs from the set
            device_ids = self.redis.smembers(self.device_set_key)

            # Get each device by its ID
            for device_id in device_ids:
                device = self.get(int(device_id))
                if device:
                    devices.append(device)

            return devices
        except redis.RedisError as e:
            logger.error("Error retrieving all devices from Redis: %s", e)
            raise

    def delete(self, device_id: int) -> None:
        """Delete a device from the repository by its ID.

        Args:
            device_id: The ID of the device to delete.
        """
        key = f"device:{device_id}"
        try:
            # Remove the device data
            self.redis.delete(key)
            # Remove the device ID from the set of all devices
            self.redis.srem(self.device_set_key, device_id)
            logger.debug("Device %s deleted from Redis", device_id)
        except redis.RedisError as e:
            logger.error(
                "Error deleting device %s from Redis: %s", device_id, e
            )
            raise

    def clear_all(self) -> None:
        """Clear all devices from the repository.

        This is useful for testing and initialization.
        """
        try:
            # Get all device IDs
            device_ids = self.redis.smembers(self.device_set_key)

            # Delete each device
            for device_id in device_ids:
                self.redis.delete(f"device:{device_id}")

            # Clear the set of all devices
            self.redis.delete(self.device_set_key)

            logger.debug("All devices cleared from Redis")
        except redis.RedisError as e:
            logger.error("Error clearing all devices from Redis: %s", e)
            raise
