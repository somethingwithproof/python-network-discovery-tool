"""Improved Redis repository implementation.

This module provides an improved implementation of the RedisRepository class.
"""

import json
import logging
from typing import List, Optional, Set

import redis

from network_discovery.domain.device import Device
from network_discovery.application.interfaces import DeviceRepositoryService

# Setup logging
logger = logging.getLogger(__name__)


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
        """
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.device_set_key = "devices:all"  # Key for the set containing all device IDs

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
            logger.error("Error retrieving device %s from Redis: %s", device_id, e)
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
            logger.error("Error deleting device %s from Redis: %s", device_id, e)
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
