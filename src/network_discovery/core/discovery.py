"""Device discovery service.

This module provides the core functionality for discovering devices on a network.
"""

import asyncio
import ipaddress
import logging
from typing import List, Optional, Dict

from network_discovery.domain.device import Device
from network_discovery.domain.device_manager import DeviceManager
from network_discovery.application.interfaces import (
    DeviceScannerService,
    DeviceRepositoryService,
    NotificationService,
    ReportService,
)

# Setup logging
logger = logging.getLogger(__name__)


class DeviceDiscoveryService:
    """Service for discovering devices on a network."""

    def __init__(
        self,
        scanner: DeviceScannerService,
        repository: Optional[DeviceRepositoryService] = None,
        notification_service: Optional[NotificationService] = None,
        report_service: Optional[ReportService] = None,
    ) -> None:
        """Initialize a new DeviceDiscoveryService.

        Args:
            scanner: The service to use for scanning devices.
            repository: The service to use for storing device information.
            notification_service: The service to use for sending notifications.
            report_service: The service to use for generating reports.
        """
        self.scanner = scanner
        self.repository = repository
        self.notification_service = notification_service
        self.report_service = report_service
        self.device_manager = DeviceManager()

    async def discover_network(self, network: str) -> List[Device]:
        """Discover devices on a network.

        Args:
            network: The network to scan, in CIDR notation (e.g., "192.168.1.0/24").

        Returns:
            A list of discovered devices.
        """
        try:
            network_obj = ipaddress.ip_network(network)
            logger.info("Starting discovery on network %s", network)

            # Create a device for each IP in the network
            device_id = 1
            for ip in network_obj.hosts():
                ip_str = str(ip)
                device = Device(id=device_id, host=ip_str, ip=ip_str)
                self.device_manager.add_device(device)
                device_id += 1

            # Scan all devices
            tasks = []
            {}

            for device in self.device_manager.devices:
                # Create a task for each device scan
                task = asyncio.create_task(self.scanner.scan_device(device))
                tasks.append(task)

                # Save the initial device state if repository is configured
                if self.repository:
                    self.repository.save(device)

            # Wait for all scans to complete
            scanned_devices = await asyncio.gather(*tasks)

            # Update the device manager with the scanned devices
            for device in scanned_devices:
                # Replace the device in the manager
                self.device_manager.add_device(device)

                # Save the updated device if repository is configured
                if self.repository:
                    self.repository.save(device)

            # Send notification if configured
            if self.notification_service:
                alive_count = sum(1 for d in self.device_manager.devices if d.alive)
                message = (
                    f"Network discovery completed for {network}.\n"
                    f"Found {len(self.device_manager.devices)} devices, "
                    f"{alive_count} are alive."
                )
                self.notification_service.send_notification(
                    "admin", "Network Discovery Completed", message
                )

            # Generate report if configured
            if self.report_service:
                self.report_service.generate_report(self.device_manager.devices, "html")

            logger.info("Discovery completed on network %s", network)
            return self.device_manager.devices
        except ValueError as e:
            logger.error("Invalid network format: %s", e)
            raise
        except Exception as e:
            logger.error("Error during network discovery: %s", e)
            raise

    async def discover_device(self, host: str, device_id: int = 1) -> Device:
        """Discover a single device.

        Args:
            host: The hostname or IP address of the device.
            device_id: The ID to assign to the device.

        Returns:
            The discovered device.
        """
        try:
            logger.info("Starting discovery for device %s", host)
            device = Device(id=device_id, host=host, ip=host)

            # Scan the device
            scanned_device = await self.scanner.scan_device(device)

            # Save the device if repository is configured
            if self.repository:
                self.repository.save(scanned_device)

            logger.info("Discovery completed for device %s", host)
            return scanned_device
        except Exception as e:
            logger.error("Error during device discovery: %s", e)
            raise

    def get_devices(self) -> List[Device]:
        """Get all discovered devices.

        Returns:
            A list of all discovered devices.
        """
        if self.repository:
            return self.repository.get_all()
        return self.device_manager.devices

    def generate_report(self, format_type: str = "html") -> Optional[str]:
        """Generate a report of discovered devices.

        Args:
            format_type: The format of the report (e.g., "html", "csv", "xlsx", "json").

        Returns:
            The path to the generated report file, or None if no report service is configured.
        """
        if self.report_service:
            return self.report_service.generate_report(
                self.device_manager.devices, format_type
            )
        return None
