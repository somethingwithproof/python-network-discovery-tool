import importlib.util
import logging
import os
import asyncio
import nmap
from paramiko import RejectPolicy, SSHClient
from paramiko.ssh_exception import AuthenticationException, SSHException

from network_discovery.application.interfaces import DeviceScannerService
from network_discovery.domain.device import Device

logger = logging.getLogger(__name__)

SSH_USER = os.getenv("SSH_USER", "")
SSH_KNOWN_HOSTS_FILE = os.getenv("SSH_KNOWN_HOSTS_FILE", os.path.expanduser("~/.ssh/known_hosts"))
MYSQL_USER = os.getenv("MYSQL_USER", "")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

MYSQL_AVAILABLE = importlib.util.find_spec("pymysql") is not None
if MYSQL_AVAILABLE:
    import pymysql
else:
    logger.warning("pymysql not available. MySQL checks will be disabled.")

SNMP_AVAILABLE = importlib.util.find_spec("snimpy") is not None
if SNMP_AVAILABLE:
    from snimpy.manager import load as snimpy_load, Manager as SnimpyManager
else:
    logger.warning("snimpy not available. SNMP checks will be disabled.")


class NmapDeviceScanner(DeviceScannerService):
    """Implementation of DeviceScannerService using Nmap."""

    def __init__(self):
        """Initializes the Nmap PortScanner instance."""
        self._nm = nmap.PortScanner()

    async def scan_device(self, device: Device) -> Device:
        """Scans a device and updates its status.

        Args:
            device: The device to scan.

        Returns:
            Updated Device instance.
        """
        device.alive = await self.is_alive(device)

        if device.alive:
            results = await asyncio.gather(
                self.check_ssh(device),
                self.check_snmp(device),
                self.check_mysql(device)
            )

            device.ssh, ssh_errors = results[0]
            device.snmp, snmp_errors = results[1]
            device.mysql, mysql_errors = results[2]

            for error in ssh_errors + snmp_errors + mysql_errors:
                device.add_error(error)
        else:
            device.reset_services()
            device.add_error("(alive) Host is down")

        device.scanned = True
        return device

    async def is_alive(self, device: Device) -> bool:
        """Checks if a device is alive using Nmap.

        Args:
            device: The device to check.

        Returns:
            True if the device is alive, False otherwise.
        """
        try:
            self._nm.scan(hosts=str(device.ip), arguments="-sn")
            return device.ip in self._nm.all_hosts() and self._nm[device.ip].state() == "up"
        except Exception as e:
            logger.error("Error checking if device %s is alive: %s", device.host, e)
            return False

    async def is_port_open(self, device: Device, port: int) -> tuple[bool, list[str]]:
        """Checks if a specific port is open on a device.

        Args:
            device: The device to check.
            port: Port number to check.

        Returns:
            Tuple containing port open status and list of errors.
        """
        errors = []
        try:
            self._nm.scan(hosts=str(device.ip), arguments=f"-p {port}")
            tcp_ports = self._nm[device.ip].get("tcp", {})
            return tcp_ports.get(port, {}).get("state") == "open", errors
        except Exception as e:
            error_msg = f"(port {port}) Exception: {e}"
            errors.append(error_msg)
            logger.error("Port scan error on %s:%d - %s", device.host, port, e)
            return False, errors
