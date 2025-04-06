"""Device scanner implementation.

This module provides the implementation of the DeviceScannerService interface.
"""

import logging
import os

from paramiko import SSHClient, RejectPolicy
from paramiko.ssh_exception import AuthenticationException, SSHException
import MySQLdb
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
from snimpy.manager import Manager as SnimpyManager, load as snimpy_load

from network_discovery.domain.device import Device
from network_discovery.application.interfaces import DeviceScannerService

# Setup logging
logger = logging.getLogger(__name__)

# Environment variables
SSH_USER = os.getenv("SSH_USER", "zenossmon")
SSH_KEY_FILE = os.getenv("SSH_KEY_FILE", os.path.expanduser("~/.ssh/id_rsa.pub"))
MYSQL_USER = os.getenv("MYSQL_USER", "")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")


class NmapDeviceScanner(DeviceScannerService):
    """Implementation of DeviceScannerService using Nmap."""

    async def scan_device(self, device: Device) -> None:
        """Scan a device to check its status.

        Args:
            device: The device to scan.
        """
        try:
            device.alive = await self.is_alive(device)

            # Only check services if the device is alive
            if device.alive:
                # Run service checks in parallel
                ssh_result = await self.check_ssh(device)
                snmp_result = await self.check_snmp(device)
                mysql_result = await self.check_mysql(device)

                device.ssh = ssh_result
                device.snmp = snmp_result
                device.mysql = mysql_result
            else:
                device.reset_services()
                device.add_error("(alive) Host is down")

            device.scanned = True
        except Exception as e:
            device.add_error(f"(scan) Exception: {e}")
            logger.error("Error scanning device %s: %s", device.host, e)

    async def is_alive(self, device: Device) -> bool:
        """Check if a device is alive using an Nmap ping scan.

        Args:
            device: The device to check.

        Returns:
            True if the device is alive, False otherwise.
        """
        try:
            nmproc = NmapProcess(str(device.ip), "-sn")
            rc = nmproc.run()
            if rc != 0:
                device.add_error(f"(alive) {nmproc.stderr}")
                return False

            nmap_report = NmapParser.parse(nmproc.stdout)
            return nmap_report.hosts[0].status == "up"
        except NmapParserException as e:
            device.add_error(f"(alive) NmapParserException: {e}")
            logger.error("Error checking if device %s is alive: %s", device.host, e)
            return False
        except Exception as e:
            device.add_error(f"(alive) Exception: {e}")
            logger.error("Error checking if device %s is alive: %s", device.host, e)
            return False

    async def is_port_open(self, device: Device, port: int) -> bool:
        """Check if a specific port on a device is open.

        Args:
            device: The device to check.
            port: The port number to check.

        Returns:
            True if the port is open, False otherwise.
        """
        try:
            nmproc = NmapProcess(str(device.ip), f"-p {port}")
            rc = nmproc.run()
            if rc != 0:
                device.add_error(f"(port {port}) {nmproc.stderr}")
                return False

            nmap_report = NmapParser.parse(nmproc.stdout)
            if nmap_report.hosts[0].status == "up":
                return nmap_report.hosts[0].services[0].state == "open"
            return False
        except NmapParserException as e:
            device.add_error(f"(port {port}) NmapParserException: {e}")
            logger.error("Error checking if port %s is open on %s: %s", port, device.host, e)
            return False
        except Exception as e:
            device.add_error(f"(port {port}) Exception: {e}")
            logger.error("Error checking if port %s is open on %s: %s", port, device.host, e)
            return False

    async def check_ssh(self, device: Device) -> bool:
        """Check if SSH is available on a device.

        Args:
            device: The device to check.

        Returns:
            True if SSH is available, False otherwise.
        """
        device.uname = "unknown"
        port_open = await self.is_port_open(device, 22)
        if not port_open:
            device.add_error("(ssh) Port closed")
            return False

        try:
            ssh = SSHClient()
            ssh.load_host_keys(SSH_KEY_FILE)
            # Use RejectPolicy instead of AutoAddPolicy for security
            ssh.set_missing_host_key_policy(RejectPolicy())
            ssh.connect(device.host, username=SSH_USER, timeout=3)
            _, stdout, _ = ssh.exec_command("uname -a")
            device.uname = stdout.read().decode().strip()
            ssh.close()
            return True
        except (AuthenticationException, SSHException) as e:
            device.add_error(f"(ssh) {str(e)}")
            logger.error("SSH error on %s: %s", device.host, e)
            return False
        except Exception as e:
            device.add_error(f"(ssh) {str(e)}")
            logger.error("Error checking SSH on %s: %s", device.host, e)
            return False

    async def check_snmp(self, device: Device) -> bool:
        """Check if SNMP is available on a device.

        Args:
            device: The device to check.

        Returns:
            True if SNMP is available, False otherwise.
        """
        try:
            snimpy_load("SNMPv2-MIB")
            m = SnimpyManager(
                host=device.host, community=device.snmp_group, version=2, timeout=2
            )
            return m.sysName is not None
        except Exception as e:
            device.add_error(f"(snmp) {str(e)}")
            logger.error("Error checking SNMP on %s: %s", device.host, e)
            return False

    async def check_mysql(self, device: Device) -> bool:
        """Check if MySQL is available on a device.

        Args:
            device: The device to check.

        Returns:
            True if MySQL is available, False otherwise.
        """
        port_open = await self.is_port_open(device, 3306)
        if not port_open:
            device.add_error("(mysql) Port closed")
            return False

        mysql_user = device.mysql_user or MYSQL_USER
        mysql_password = device.mysql_password or MYSQL_PASSWORD

        if not mysql_user:
            device.add_error("(mysql) No MySQL user provided")
            return False

        try:
            db = MySQLdb.connect(
                host=device.host,
                user=mysql_user,
                passwd=mysql_password,
                db="mysql",
                connect_timeout=3,
            )
            cursor = db.cursor()
            cursor.execute("SELECT VERSION()")
            cursor.fetchone()
            db.close()
            return True
        except MySQLdb.OperationalError as e:
            device.add_error(f"(mysql) {str(e)}")
            logger.error("MySQL error on %s: %s", device.host, e)
            return False
        except Exception as e:
            device.add_error(f"(mysql) {str(e)}")
            logger.error("Error checking MySQL on %s: %s", device.host, e)
            return False
