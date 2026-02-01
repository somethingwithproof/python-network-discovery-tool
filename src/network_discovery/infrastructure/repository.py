"""Repository implementations.

This module provides implementations of the DeviceRepositoryService interface.
"""

from __future__ import annotations

import importlib.util
import json
import logging
from pathlib import Path

import ijson

from network_discovery.application.interfaces import DeviceRepositoryService
from network_discovery.domain.device import Device


# Setup logging
logger = logging.getLogger(__name__)

# Check for optional redis dependency
REDIS_AVAILABLE = importlib.util.find_spec("redis") is not None
if REDIS_AVAILABLE:
    import redis
else:
    redis = None  # type: ignore[assignment]
    logger.debug("redis not available. RedisRepository will be disabled.")


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
        path = Path(self.file_path)
        if path.parent.name and not path.parent.exists():
            path.parent.mkdir(parents=True)

        if not path.exists():
            path.write_text("{}", encoding="utf-8")
        else:
            try:
                with path.open(encoding="utf-8") as file:
                    json.load(file)
            except (OSError, json.JSONDecodeError) as e:
                logger.error(
                    "Error reading JSON file: %s. Initializing with empty object.",
                    e,
                )
                path.write_text("{}", encoding="utf-8")

    def save(self, device: Device) -> None:
        """Save a device to the repository.

        Args:
            device: The device to save.
        """
        key = f"device:{device.id}"
        device_data = device.to_dict()
        path = Path(self.file_path)

        try:
            with path.open(encoding="utf-8") as file:
                data = json.load(file)

            data[key] = device_data

            with path.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            logger.debug("Device %s saved to JSON file", device.id)
        except (OSError, json.JSONDecodeError) as e:
            logger.error("Error saving device %s to JSON file: %s", device.id, e)
            raise

    def get(self, device_id: int) -> Device | None:
        """Get a device from the repository by its ID.

        Args:
            device_id: The ID of the device to retrieve.

        Returns:
            The device if found, None otherwise.
        """
        key = f"device:{device_id}"

        try:
            with Path(self.file_path).open("rb") as file:
                for prefix, event, _value in ijson.parse(file):
                    if prefix == key and event == "start_map":
                        device_data: dict = {}
                        current_key: str | None = None

                        for p, e, v in ijson.parse(file):
                            if p == key and e == "end_map":
                                break
                            elif e == "map_key":
                                current_key = v
                            elif current_key is not None:
                                device_data[current_key] = v
                                current_key = None

                        return Device.from_dict(device_data)

            return None
        except (OSError, ijson.JSONError) as e:
            logger.error("Error retrieving device %s from JSON file: %s", device_id, e)
            return self._get_fallback(device_id)

    def _get_fallback(self, device_id: int) -> Device | None:
        """Fallback method to get a device by loading the entire file.

        Args:
            device_id: The ID of the device to retrieve.

        Returns:
            The device if found, None otherwise.
        """
        key = f"device:{device_id}"

        try:
            with Path(self.file_path).open(encoding="utf-8") as file:
                data = json.load(file)

            device_data = data.get(key)
            if device_data:
                return Device.from_dict(device_data)
            return None
        except (OSError, json.JSONDecodeError) as e:
            logger.error("Error in fallback retrieval of device %s: %s", device_id, e)
            return None

    def get_all(self) -> list[Device]:
        """Get all devices from the repository.

        Returns:
            A list of all devices.
        """
        devices = []

        try:
            with Path(self.file_path).open("rb") as file:
                device_keys = []
                for _prefix, event, value in ijson.parse(file):
                    if event == "map_key" and value.startswith("device:"):
                        device_keys.append(value)

            for key in device_keys:
                device_id = int(key.split(":")[1])
                device = self.get(device_id)
                if device:
                    devices.append(device)

            return devices
        except (OSError, ijson.JSONError) as e:
            logger.error("Error retrieving all devices from JSON file: %s", e)
            return self._get_all_fallback()

    def _get_all_fallback(self) -> list[Device]:
        """Fallback method to get all devices by loading the entire file.

        Returns:
            A list of all devices.
        """
        devices = []

        try:
            with Path(self.file_path).open(encoding="utf-8") as file:
                data = json.load(file)

            for key, value in data.items():
                if key.startswith("device:"):
                    try:
                        devices.append(Device.from_dict(value))
                    except Exception as e:
                        logger.error("Error creating device from data: %s", e)

            return devices
        except (OSError, json.JSONDecodeError) as e:
            logger.error("Error in fallback retrieval of all devices: %s", e)
            return []

    def delete(self, device_id: int) -> None:
        """Delete a device from the repository by its ID.

        Args:
            device_id: The ID of the device to delete.
        """
        key = f"device:{device_id}"
        path = Path(self.file_path)

        try:
            with path.open(encoding="utf-8") as file:
                data = json.load(file)

            if key in data:
                del data[key]

                with path.open("w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4)

                logger.debug("Device %s deleted from JSON file", device_id)
        except (OSError, json.JSONDecodeError) as e:
            logger.error("Error deleting device %s from JSON file: %s", device_id, e)
            raise

    def clear_all(self) -> None:
        """Clear all devices from the repository.

        This is useful for testing and initialization.
        """
        try:
            Path(self.file_path).write_text("{}", encoding="utf-8")
            logger.debug("All devices cleared from JSON file")
        except OSError as e:
            logger.error("Error clearing all devices from JSON file: %s", e)
            raise


class RedisRepository(DeviceRepositoryService):
    """Implementation of DeviceRepositoryService using Redis.

    This implementation uses Redis Sets to track device IDs, avoiding the use of the KEYS command
    which can be problematic in production environments with large datasets.
    """

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0) -> None:
        """Initialize a new RedisRepository.

        Args:
            host: The Redis host.
            port: The Redis port.
            db: The Redis database number.

        Raises:
            ImportError: If redis is not installed.
        """
        if not REDIS_AVAILABLE:
            raise ImportError(
                "RedisRepository requires redis. Install with: pip install redis"
            )
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.device_set_key = "devices:all"  # Key for the set containing all device IDs

    def save(self, device: Device) -> None:
        """Save a device to the repository.

        Args:
            device: The device to save.
        """
        key = f"device:{device.id}"
        try:
            self.redis.set(key, json.dumps(device.to_dict()))
            self.redis.sadd(self.device_set_key, device.id)
            logger.debug("Device %s saved to Redis", device.id)
        except redis.RedisError as e:
            logger.error("Error saving device %s to Redis: %s", device.id, e)
            raise

    def get(self, device_id: int) -> Device | None:
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
            logger.error("Error retrieving device %s from Redis: %s", device_id, e)
            raise
        except json.JSONDecodeError as e:
            logger.error("Error decoding device %s data: %s", device_id, e)
            return None

    def get_all(self) -> list[Device]:
        """Get all devices from the repository.

        Returns:
            A list of all devices.
        """
        devices = []
        try:
            device_ids = self.redis.smembers(self.device_set_key)

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
            self.redis.delete(key)
            self.redis.srem(self.device_set_key, device_id)
            logger.debug("Device %s deleted from Redis", device_id)
        except redis.RedisError as e:
            logger.error("Error deleting device %s from Redis: %s", device_id, e)
            raise

    def clear_all(self) -> None:
        """Clear all devices from the repository.

        This is useful for testing and initialization.
        """
        try:
            device_ids = self.redis.smembers(self.device_set_key)

            for device_id in device_ids:
                self.redis.delete(f"device:{device_id}")

            self.redis.delete(self.device_set_key)

            logger.debug("All devices cleared from Redis")
        except redis.RedisError as e:
            logger.error("Error clearing all devices from Redis: %s", e)
            raise

    def clear(self) -> None:
        """Alias for clear_all() for API compatibility."""
        self.clear_all()

    def count(self) -> int:
        """Count the number of devices in the repository.

        Returns:
            The number of devices stored.
        """
        try:
            return self.redis.scard(self.device_set_key)
        except redis.RedisError as e:
            logger.error("Error counting devices in Redis: %s", e)
            raise
