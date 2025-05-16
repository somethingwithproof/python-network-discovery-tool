"""Device discovery service for network scanning.

This module provides the core functionality for discovering devices on a network.
It orchestrates the use of scanner, repository, notification, and report services
to scan networks, store results, and generate reports.
"""

import asyncio
import ipaddress
import logging
from typing import Dict, List, Optional, Union

from network_discovery.application.interfaces import (
    DeviceRepositoryService,
    DeviceScannerService,
    NotificationService,
    ReportService,
)
from network_discovery.domain.device import Device
from network_discovery.domain.device_manager import DeviceManager

# Setup module logger
logger = logging.getLogger(__name__)


class DeviceDiscoveryService:
    """Service for discovering and managing network devices.
    
    This service coordinates the discovery of devices on a network by using
    various services to scan devices, store device information, send notifications,
    and generate reports.
    """

    def __init__(
        self,
        scanner: DeviceScannerService,
        repository: Optional[DeviceRepositoryService] = None,
        notification_service: Optional[NotificationService] = None,
        report_service: Optional[ReportService] = None,
    ) -> None:
        """Initialize a new DeviceDiscoveryService.

        Args:
            scanner: The service to use for scanning devices and detecting services.
            repository: Optional service to use for storing and retrieving device
                information. If None, devices will only be stored in memory.
            notification_service: Optional service to use for sending notifications
                about discovery results. If None, no notifications will be sent.
            report_service: Optional service to use for generating reports of
                discovery results. If None, no reports will be generated.
        """
        self.scanner = scanner
        self.repository = repository
        self.notification_service = notification_service
        self.report_service = report_service
        self.device_manager = DeviceManager()

    async def discover_network(self, network: str) -> List[Device]:
        """Discover and scan all devices on a network.

        Parses the network CIDR, creates a Device instance for each IP in the
        network, scans them concurrently, and processes the results.

        Args:
            network: The network to scan, in CIDR notation (e.g., "192.168.1.0/24").

        Returns:
            A list of discovered devices with scan results.
            
        Raises:
            ValueError: If the network string is not a valid CIDR notation.
            Exception: If an error occurs during the discovery process.
        """
        try:
            # Parse network string to an ipaddress.IPv4Network or IPv6Network object
            network_obj = ipaddress.ip_network(network)
            logger.info("Starting discovery on network %s", network)

            # Create a device for each IP in the network
            device_id = 1
            for ip in network_obj.hosts():
                ip_str = str(ip)
                device = Device(id=device_id, host=ip_str, ip=ip_str)
                self.device_manager.add_device(device)
                device_id += 1

            # Scan all devices concurrently
            tasks = []

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
                # Replace the device in the manager with updated version
                self.device_manager.add_device(device)

                # Save the updated device if repository is configured
                if self.repository:
                    self.repository.save(device)

            # Send notification if notification service is configured
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

            # Generate report if report service is configured
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
        """Discover and scan a single device.

        Creates a Device instance for the specified host, scans it, and optionally
        saves the results to the repository.

        Args:
            host: The hostname or IP address of the device to scan.
            device_id: The ID to assign to the device (default: 1).

        Returns:
            The discovered device with scan results.
            
        Raises:
            Exception: If an error occurs during the discovery process.
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

        Retrieves devices from the repository if available, otherwise returns
        devices from the in-memory device manager.

        Returns:
            A list of all discovered devices.
        """
        if self.repository:
            return self.repository.get_all()
        return self.device_manager.devices

    def generate_report(self, format_type: str = "html") -> Optional[str]:
        """Generate a report of discovered devices.

        Generates a report of all discovered devices using the configured
        report service, if available.

        Args:
            format_type: The format of the report (e.g., "html", "csv", "xlsx", "json").

        Returns:
            The path to the generated report file, or None if no report service is set.
        """
        if self.report_service:
            devices = self.device_manager.devices
            return self.report_service.generate_report(devices, format_type)
        return None
