"""Device scanner implementation.

This module provides the implementation of the DeviceScannerService interface.
"""

import logging
import os
import importlib.util

from paramiko import SSHClient, RejectPolicy
from paramiko.ssh_exception import AuthenticationException, SSHException
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException

from network_discovery.domain.device import Device
from network_discovery.application.interfaces import DeviceScannerService

# Setup logging
logger = logging.getLogger(__name__)

# Environment variables
SSH_USER = os.getenv("SSH_USER", "zenossmon")
SSH_KEY_FILE = os.getenv("SSH_KEY_FILE", os.path.expanduser("~/.ssh/id_rsa.pub"))
MYSQL_USER = os.getenv("MYSQL_USER", "")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

# Check if optional dependencies are available
MYSQL_AVAILABLE = importlib.util.find_spec("MySQLdb") is not None
if MYSQL_AVAILABLE:
    import MySQLdb
else:
    logger.warning("MySQLdb not available. MySQL checks will be disabled.")

SNMP_AVAILABLE = importlib.util.find_spec("snimpy") is not None
if SNMP_AVAILABLE:
    from snimpy.manager import Manager as SnimpyManager, load as snimpy_load
else:
    logger.warning("snimpy not available. SNMP checks will be disabled.")


class NmapDeviceScanner(DeviceScannerService):
    """Implementation of DeviceScannerService using Nmap."""

    async def scan_device(self, device: Device) -> Device:
        """Scan a device to check its status.

        Args:
            device: The device to scan.
            
        Returns:
            An updated Device instance with scan results.
        """
        try:
            is_alive = await self.is_alive(device)
            device = device.replace(alive=is_alive)

            # Only check services if the device is alive
            if is_alive:
                # Run service checks in parallel
                ssh_result = await self.check_ssh(device)
                snmp_result = await self.check_snmp(device)
                mysql_result = await self.check_mysql(device)

                device = device.replace(
                    ssh=ssh_result[0],
                    snmp=snmp_result[0],
                    mysql=mysql_result[0],
                    scanned=True
                )
                
                # Add any errors from the service checks
                for error in ssh_result[1] + snmp_result[1] + mysql_result[1]:
                    device = device.add_error(error)
            else:
                device = device.reset_services()
                device = device.add_error("(alive) Host is down")
                device = device.replace(scanned=True)

            return device
        except Exception as e:
            error_msg = f"(scan) Exception: {e}"
            logger.error("Error scanning device %s: %s", device.host, e)
            return device.add_error(error_msg).replace(scanned=True)

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
                return False

            nmap_report = NmapParser.parse(nmproc.stdout)
            return nmap_report.hosts[0].status == "up"
        except NmapParserException as e:
            logger.error("Error checking if device %s is alive: %s", device.host, e)
            return False
        except Exception as e:
            logger.error("Error checking if device %s is alive: %s", device.host, e)
            return False

    async def is_port_open(self, device: Device, port: int) -> tuple[bool, list[str]]:
        """Check if a specific port on a device is open.

        Args:
            device: The device to check.
            port: The port number to check.

        Returns:
            A tuple containing:
            - A boolean indicating if the port is open
            - A list of error messages, if any
        """
        errors = []
        try:
            nmproc = NmapProcess(str(device.ip), f"-p {port}")
            rc = nmproc.run()
            if rc != 0:
                errors.append(f"(port {port}) {nmproc.stderr}")
                return False, errors

            nmap_report = NmapParser.parse(nmproc.stdout)
            if nmap_report.hosts[0].status == "up":
                return nmap_report.hosts[0].services[0].state == "open", errors
            return False, errors
        except NmapParserException as e:
            error_msg = f"(port {port}) NmapParserException: {e}"
            logger.error("Error checking if port %s is open on %s: %s", port, device.host, e)
            errors.append(error_msg)
            return False, errors
        except Exception as e:
            error_msg = f"(port {port}) Exception: {e}"
            logger.error("Error checking if port %s is open on %s: %s", port, device.host, e)
            errors.append(error_msg)
            return False, errors

    async def check_ssh(self, device: Device) -> tuple[bool, list[str]]:
        """Check if SSH is available on a device.

        Args:
            device: The device to check.

        Returns:
            A tuple containing:
            - A boolean indicating if SSH is available
            - A list of error messages, if any
        """
        errors = []
        device = device.replace(uname="unknown")
        port_open, port_errors = await self.is_port_open(device, 22)
        errors.extend(port_errors)
        
        if not port_open:
            errors.append("(ssh) Port closed")
            return False, errors

        try:
            ssh = SSHClient()
            ssh.load_host_keys(SSH_KEY_FILE)
            # Use RejectPolicy instead of AutoAddPolicy for security
            ssh.set_missing_host_key_policy(RejectPolicy())
            ssh.connect(device.host, username=SSH_USER, timeout=3)
            _, stdout, _ = ssh.exec_command("uname -a")
            uname = stdout.read().decode().strip()
            ssh.close()
            
            # Return success and the uname
            return True, errors
        except (AuthenticationException, SSHException) as e:
            error_msg = f"(ssh) {str(e)}"
            logger.error("SSH error on %s: %s", device.host, e)
            errors.append(error_msg)
            return False, errors
        except Exception as e:
            error_msg = f"(ssh) {str(e)}"
            logger.error("Error checking SSH on %s: %s", device.host, e)
            errors.append(error_msg)
            return False, errors

    async def check_snmp(self, device: Device) -> tuple[bool, list[str]]:
        """Check if SNMP is available on a device.

        Args:
            device: The device to check.

        Returns:
            A tuple containing:
            - A boolean indicating if SNMP is available
            - A list of error messages, if any
        """
        errors = []
        if not SNMP_AVAILABLE:
            errors.append("(snmp) SNMP support not available")
            return False, errors

        try:
            snimpy_load("SNMPv2-MIB")
            m = SnimpyManager(
                host=device.host, community=device.snmp_group, version=2, timeout=2
            )
            return m.sysName is not None, errors
        except Exception as e:
            error_msg = f"(snmp) {str(e)}"
            logger.error("Error checking SNMP on %s: %s", device.host, e)
            errors.append(error_msg)
            return False, errors

    async def check_mysql(self, device: Device) -> tuple[bool, list[str]]:
        """Check if MySQL is available on a device.

        Args:
            device: The device to check.

        Returns:
            A tuple containing:
            - A boolean indicating if MySQL is available
            - A list of error messages, if any
        """
        errors = []
        if not MYSQL_AVAILABLE:
            errors.append("(mysql) MySQL support not available")
            return False, errors

        port_open, port_errors = await self.is_port_open(device, 3306)
        errors.extend(port_errors)
        
        if not port_open:
            errors.append("(mysql) Port closed")
            return False, errors

        mysql_user = device.mysql_user or MYSQL_USER
        mysql_password = device.mysql_password or MYSQL_PASSWORD

        if not mysql_user:
            errors.append("(mysql) No MySQL user provided")
            return False, errors

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
            return True, errors
        except MySQLdb.OperationalError as e:
            error_msg = f"(mysql) {str(e)}"
            logger.error("MySQL error on %s: %s", device.host, e)
            errors.append(error_msg)
            return False, errors
        except Exception as e:
            error_msg = f"(mysql) {str(e)}"
            logger.error("Error checking MySQL on %s: %s", device.host, e)
            errors.append(error_msg)
            return False, errors
