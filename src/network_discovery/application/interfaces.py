"""Application service interfaces.

This module defines the interfaces for the application services.
"""

from abc import ABC, abstractmethod
from typing import List, Any, Optional, Tuple

from network_discovery.domain.device import Device


class DeviceScannerService(ABC):
    """Interface for device scanning services."""

    @abstractmethod
    async def scan_device(self, device: Device) -> Device:
        """Scan a device to check its status.

        Args:
            device: The device to scan.

        Returns:
            An updated Device instance with scan results.
        """

    @abstractmethod
    async def is_alive(self, device: Device) -> bool:
        """Check if a device is alive.

        Args:
            device: The device to check.

        Returns:
            True if the device is alive, False otherwise.
        """

    @abstractmethod
    async def is_port_open(self, device: Device, port: int) -> Tuple[bool, List[str]]:
        """Check if a specific port on a device is open.

        Args:
            device: The device to check.
            port: The port number to check.

        Returns:
            A tuple containing:
            - A boolean indicating if the port is open
            - A list of error messages, if any
        """

    @abstractmethod
    async def check_ssh(self, device: Device) -> Tuple[bool, List[str]]:
        """Check if SSH is available on a device.

        Args:
            device: The device to check.

        Returns:
            A tuple containing:
            - A boolean indicating if SSH is available
            - A list of error messages, if any
        """

    @abstractmethod
    async def check_snmp(self, device: Device) -> Tuple[bool, List[str]]:
        """Check if SNMP is available on a device.

        Args:
            device: The device to check.

        Returns:
            A tuple containing:
            - A boolean indicating if SNMP is available
            - A list of error messages, if any
        """

    @abstractmethod
    async def check_mysql(self, device: Device) -> Tuple[bool, List[str]]:
        """Check if MySQL is available on a device.

        Args:
            device: The device to check.

        Returns:
            A tuple containing:
            - A boolean indicating if MySQL is available
            - A list of error messages, if any
        """


class DeviceRepositoryService(ABC):
    """Interface for device repository services."""

    @abstractmethod
    def save(self, device: Device) -> None:
        """Save a device to the repository.

        Args:
            device: The device to save.
        """

    @abstractmethod
    def get(self, device_id: int) -> Optional[Device]:
        """Get a device from the repository by its ID.

        Args:
            device_id: The ID of the device to retrieve.

        Returns:
            The device if found, None otherwise.
        """

    @abstractmethod
    def get_all(self) -> List[Device]:
        """Get all devices from the repository.

        Returns:
            A list of all devices.
        """

    @abstractmethod
    def delete(self, device_id: int) -> None:
        """Delete a device from the repository by its ID.

        Args:
            device_id: The ID of the device to delete.
        """


class NotificationService(ABC):
    """Interface for notification services."""

    @abstractmethod
    def send_notification(self, recipient: str, subject: str, message: str) -> None:
        """Send a notification.

        Args:
            recipient: The recipient of the notification.
            subject: The subject of the notification.
            message: The message content of the notification.
        """


class ReportService(ABC):
    """Interface for report generation services."""

    @abstractmethod
    def generate_report(self, devices: List[Device], format_type: str) -> Any:
        """Generate a report for a list of devices.

        Args:
            devices: The list of devices to include in the report.
            format_type: The format of the report (e.g., "html", "csv", "xlsx").

        Returns:
            The generated report in the specified format.
        """
