"""Domain layer for the network discovery tool.

This package contains the core domain models and business logic.
"""

from .device import Device
from .device_manager import DeviceManager

__all__ = ["Device", "DeviceManager"]
