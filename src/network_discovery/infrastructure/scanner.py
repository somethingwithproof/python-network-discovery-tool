"""Device scanner implementation.

This module provides the implementation of the DeviceScannerService interface.
"""

import logging
import os
import importlib.util

import nmap
from paramiko import SSHClient, RejectPolicy
from paramiko.ssh_exception import AuthenticationException, SSHException

from network_discovery.domain.device import Device
from network_discovery.application.interfaces import DeviceScannerService

# Setup logging
logger = logging.getLogger(__name__)

# Environment variables
SSH_USER = os.getenv("SSH_USER", "")
SSH_KNOWN_HOSTS_FILE = os.getenv("SSH_KNOWN_HOSTS_FILE", os.path.expanduser("~/.ssh/known_hosts"))
MYSQL_USER = os.getenv("MYSQL_USER", "")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

# Check if optional dependencies are available
MYSQL_AVAILABLE = importlib.util.find_spec("pymysql") is not None
if MYSQL_AVAILABLE:
    import pymysql
else:
    logger.warning("pymysql not available. MySQL checks will be disabled.")

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
            device.alive = await self.is_alive(device)

            # Only check services if the device is alive
            if device.alive:
                # Run service checks in parallel
                ssh_result, ssh_errors = await self.check_ssh(device)
                snmp_result, snmp_errors = await self.check_snmp(device)
                mysql_result, mysql_errors = await self.check_mysql(device)

                device.ssh = ssh_result
                device.snmp = snmp_result
                device.mysql = mysql_result

                # Add any errors from the service checks
                for error in ssh_errors + snmp_errors + mysql_errors:
                    device.add_error(error)
            else:
                device.reset_services()
                device.add_error("(alive) Host is down")

            device.scanned = True
            return device
        except Exception as e:
            error_msg = f"(scan) Exception: {e}"
            device.add_error(error_msg)
            logger.error("Error scanning device %s: %s", device.host, e)
            device.scanned = True
            return device

    async def is_alive(self, device: Device) -> bool:
        """Check if a device is alive using an Nmap ping scan.

        Args:
            device: The device to check.

        Returns:
            True if the device is alive, False otherwise.
        """
        try:
            nm = nmap.PortScanner()
            nm.scan(hosts=str(device.ip), arguments="-sn")

            # Check if the host is up
            if str(device.ip) in nm.all_hosts():
                return nm[str(device.ip)].state() == "up"
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
            nm = nmap.PortScanner()
            nm.scan(hosts=str(device.ip), arguments=f"-p {port}")

            # Check if the port is open
            if str(device.ip) in nm.all_hosts():
                if "tcp" in nm[str(device.ip)] and port in nm[str(device.ip)]["tcp"]:
                    return nm[str(device.ip)]["tcp"][port]["state"] == "open", errors
            return False, errors
        except Exception as e:
            error_msg = f"(port {port}) Exception: {e}"
            errors.append(error_msg)
            logger.error(
                "Error checking if port %s is open on %s: %s", port, device.host, e
            )
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
        device.uname = "unknown"
        port_open, port_errors = await self.is_port_open(device, 22)
        errors.extend(port_errors)

        if not port_open:
            error_msg = "(ssh) Port closed"
            errors.append(error_msg)
            return False, errors

        try:
            ssh = SSHClient()
            ssh.load_host_keys(SSH_KNOWN_HOSTS_FILE)
            # Use RejectPolicy instead of AutoAddPolicy for security
            ssh.set_missing_host_key_policy(RejectPolicy())

            # Connect to the SSH server
            try:
                ssh.connect(device.host, username=SSH_USER, timeout=3)
            except AuthenticationException as e:
                error_msg = f"(ssh) Authentication failed: {str(e)}"
                errors.append(error_msg)
                logger.error("SSH authentication error on %s: %s", device.host, e)
                return False, errors
            except SSHException as e:
                error_msg = f"(ssh) SSH protocol error: {str(e)}"
                errors.append(error_msg)
                logger.error("SSH protocol error on %s: %s", device.host, e)
                return False, errors
            except TimeoutError as e:
                error_msg = f"(ssh) Connection timeout: {str(e)}"
                errors.append(error_msg)
                logger.error("SSH connection timeout on %s: %s", device.host, e)
                return False, errors
            except ConnectionRefusedError as e:
                error_msg = f"(ssh) Connection refused: {str(e)}"
                errors.append(error_msg)
                logger.error("SSH connection refused on %s: %s", device.host, e)
                return False, errors
            except Exception as e:
                error_msg = f"(ssh) Connection error: {str(e)}"
                errors.append(error_msg)
                logger.error("SSH connection error on %s: %s", device.host, e)
                return False, errors

            # Execute command
            try:
                _, stdout, stderr = ssh.exec_command("uname -a")
                device.uname = stdout.read().decode().strip()
                error_output = stderr.read().decode().strip()
                if error_output:
                    logger.warning(
                        "SSH command produced error output on %s: %s",
                        device.host,
                        error_output,
                    )
            except Exception as e:
                error_msg = f"(ssh) Command execution error: {str(e)}"
                errors.append(error_msg)
                logger.error("SSH command execution error on %s: %s", device.host, e)
                ssh.close()
                return False, errors

            # Close the connection
            ssh.close()
            return True, errors
        except Exception as e:
            error_msg = f"(ssh) Unexpected error: {str(e)}"
            errors.append(error_msg)
            logger.error("Unexpected error checking SSH on %s: %s", device.host, e)
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
            error_msg = "(snmp) SNMP checks disabled - snimpy not available"
            errors.append(error_msg)
            return False, errors

        # Check if port 161 (SNMP) is open
        port_open, port_errors = await self.is_port_open(device, 161)
        errors.extend(port_errors)

        if not port_open:
            error_msg = "(snmp) Port 161 closed"
            errors.append(error_msg)
            return False, errors

        try:
            # Load SNMP MIB
            try:
                snimpy_load("SNMPv2-MIB")
            except Exception as e:
                error_msg = f"(snmp) Failed to load MIB: {str(e)}"
                errors.append(error_msg)
                logger.error("SNMP MIB loading error: %s", e)
                return False, errors

            # Create SNMP manager and query device
            try:
                m = SnimpyManager(
                    host=device.host, community=device.snmp_group, version=2, timeout=2
                )

                # Try to get system name
                try:
                    system_name = m.sysName
                    if system_name is not None:
                        logger.debug(
                            "SNMP system name on %s: %s", device.host, system_name
                        )
                        return True, errors
                    else:
                        error_msg = "(snmp) No system name returned"
                        errors.append(error_msg)
                        return False, errors
                except Exception as e:
                    error_msg = f"(snmp) Failed to query sysName: {str(e)}"
                    errors.append(error_msg)
                    logger.error("SNMP query error on %s: %s", device.host, e)
                    return False, errors

            except TimeoutError as e:
                error_msg = f"(snmp) Connection timeout: {str(e)}"
                errors.append(error_msg)
                logger.error("SNMP timeout on %s: %s", device.host, e)
                return False, errors
            except ConnectionRefusedError as e:
                error_msg = f"(snmp) Connection refused: {str(e)}"
                errors.append(error_msg)
                logger.error("SNMP connection refused on %s: %s", device.host, e)
                return False, errors
            except Exception as e:
                error_msg = f"(snmp) Connection error: {str(e)}"
                errors.append(error_msg)
                logger.error("SNMP connection error on %s: %s", device.host, e)
                return False, errors

        except Exception as e:
            error_msg = f"(snmp) Unexpected error: {str(e)}"
            errors.append(error_msg)
            logger.error("Unexpected error checking SNMP on %s: %s", device.host, e)
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
            error_msg = "(mysql) MySQL support not available"
            errors.append(error_msg)
            return False, errors

        port_open, port_errors = await self.is_port_open(device, 3306)
        errors.extend(port_errors)

        if not port_open:
            error_msg = "(mysql) Port closed"
            errors.append(error_msg)
            return False, errors

        mysql_user = device.mysql_user or MYSQL_USER
        mysql_password = device.mysql_password or MYSQL_PASSWORD

        if not mysql_user:
            error_msg = "(mysql) No MySQL user provided"
            errors.append(error_msg)
            return False, errors

        try:
            # Attempt to connect to MySQL
            try:
                db = pymysql.connect(
                    host=device.host,
                    user=mysql_user,
                    password=mysql_password,
                    database="mysql",
                    connect_timeout=3,
                )
            except pymysql.err.OperationalError as e:
                error_code = e.args[0]
                if error_code == 1045:  # Access denied
                    error_msg = f"(mysql) Authentication failed: {str(e)}"
                    errors.append(error_msg)
                    logger.error("MySQL authentication error on %s: %s", device.host, e)
                elif error_code == 2003:  # Can't connect
                    error_msg = f"(mysql) Connection failed: {str(e)}"
                    errors.append(error_msg)
                    logger.error("MySQL connection error on %s: %s", device.host, e)
                elif error_code == 1049:  # Unknown database
                    error_msg = f"(mysql) Database not found: {str(e)}"
                    errors.append(error_msg)
                    logger.error("MySQL database error on %s: %s", device.host, e)
                else:
                    error_msg = f"(mysql) Operational error: {str(e)}"
                    errors.append(error_msg)
                    logger.error("MySQL operational error on %s: %s", device.host, e)
                return False, errors
            except TimeoutError as e:
                error_msg = f"(mysql) Connection timeout: {str(e)}"
                errors.append(error_msg)
                logger.error("MySQL connection timeout on %s: %s", device.host, e)
                return False, errors
            except ConnectionRefusedError as e:
                error_msg = f"(mysql) Connection refused: {str(e)}"
                errors.append(error_msg)
                logger.error("MySQL connection refused on %s: %s", device.host, e)
                return False, errors
            except Exception as e:
                error_msg = f"(mysql) Connection error: {str(e)}"
                errors.append(error_msg)
                logger.error("MySQL connection error on %s: %s", device.host, e)
                return False, errors

            # Execute query
            try:
                cursor = db.cursor()
                cursor.execute("SELECT VERSION()")
                result = cursor.fetchone()
                if result:
                    logger.debug("MySQL version on %s: %s", device.host, result[0])
            except pymysql.err.ProgrammingError as e:
                error_msg = f"(mysql) Query error: {str(e)}"
                errors.append(error_msg)
                logger.error("MySQL query error on %s: %s", device.host, e)
                db.close()
                return False, errors
            except Exception as e:
                error_msg = f"(mysql) Query execution error: {str(e)}"
                errors.append(error_msg)
                logger.error("MySQL query execution error on %s: %s", device.host, e)
                db.close()
                return False, errors

            # Close the connection
            db.close()
            return True, errors
        except Exception as e:
            error_msg = f"(mysql) Unexpected error: {str(e)}"
            errors.append(error_msg)
            logger.error("Unexpected error checking MySQL on %s: %s", device.host, e)
            return False, errors
