"""Scanner implementations for device discovery.

This module provides implementations of the DeviceScannerService interface
using Nmap for network scanning and various protocols for service detection.

Features:
- HTTP/HTTPS web service detection with header extraction
- OS fingerprinting using Nmap -O
- SNMPv3 support with authentication and privacy
- Rate limiting for controlled scanning
- Custom port configuration
"""

from __future__ import annotations

import asyncio
import contextlib
import importlib.util
import logging
import os
import socket
import ssl
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import nmap
from paramiko import SSHClient
from paramiko.ssh_exception import AuthenticationException, SSHException

from network_discovery.application.interfaces import DeviceScannerService


if TYPE_CHECKING:
    from network_discovery.domain.device import Device


logger = logging.getLogger(__name__)

# Environment configuration
SSH_USER = os.getenv("SSH_USER", "")
SSH_KNOWN_HOSTS_FILE = os.getenv(
    "SSH_KNOWN_HOSTS_FILE", str(Path.home() / ".ssh" / "known_hosts")
)
MYSQL_USER = os.getenv("MYSQL_USER", "")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

# Default ports for services
DEFAULT_PORTS = {
    "ssh": 22,
    "snmp": 161,
    "mysql": 3306,
    "postgres": 5432,
    "redis": 6379,
    "dns": 53,
    "http": 80,
    "https": 443,
}

# Check for optional dependencies
MYSQL_AVAILABLE = importlib.util.find_spec("pymysql") is not None
if MYSQL_AVAILABLE:
    import pymysql
else:
    pymysql = None  # type: ignore[assignment]
    logger.warning("pymysql not available. MySQL checks will be disabled.")

POSTGRES_AVAILABLE = importlib.util.find_spec("pg8000") is not None
if POSTGRES_AVAILABLE:
    import pg8000
else:
    pg8000 = None  # type: ignore[assignment]
    logger.info("pg8000 not available. PostgreSQL checks will be disabled.")

REDIS_AVAILABLE = importlib.util.find_spec("redis") is not None
if REDIS_AVAILABLE:
    import redis as redis_client
else:
    redis_client = None  # type: ignore[assignment]
    logger.info("redis not available. Redis checks will be disabled.")

DNS_AVAILABLE = importlib.util.find_spec("dns") is not None
if DNS_AVAILABLE:
    import dns.resolver
else:
    logger.info("dnspython not available. DNS checks will use basic socket.")

SNMP_AVAILABLE = importlib.util.find_spec("snimpy") is not None
if SNMP_AVAILABLE:
    from snimpy.manager import Manager as SnimpyManager
    from snimpy.manager import load as snimpy_load
else:
    logger.warning("snimpy not available. SNMP checks will be disabled.")

# Check for pysnmp for SNMPv3 (alternative to snimpy)
PYSNMP_AVAILABLE = importlib.util.find_spec("pysnmp") is not None
if PYSNMP_AVAILABLE:
    from pysnmp.hlapi import (
        ContextData,
        ObjectIdentity,
        ObjectType,
        SnmpEngine,
        UdpTransportTarget,
        UsmUserData,
        getCmd,
        usmAesCfb128Protocol,
        usmAesCfb192Protocol,
        usmAesCfb256Protocol,
        usmDESPrivProtocol,
        usmHMAC128SHA224AuthProtocol,
        usmHMAC192SHA256AuthProtocol,
        usmHMAC256SHA384AuthProtocol,
        usmHMAC384SHA512AuthProtocol,
        usmHMACMD5AuthProtocol,
        usmHMACSHAAuthProtocol,
    )

    SNMPV3_AUTH_PROTOCOLS = {
        "MD5": usmHMACMD5AuthProtocol,
        "SHA": usmHMACSHAAuthProtocol,
        "SHA224": usmHMAC128SHA224AuthProtocol,
        "SHA256": usmHMAC192SHA256AuthProtocol,
        "SHA384": usmHMAC256SHA384AuthProtocol,
        "SHA512": usmHMAC384SHA512AuthProtocol,
    }
    SNMPV3_PRIV_PROTOCOLS = {
        "DES": usmDESPrivProtocol,
        "AES": usmAesCfb128Protocol,
        "AES128": usmAesCfb128Protocol,
        "AES192": usmAesCfb192Protocol,
        "AES256": usmAesCfb256Protocol,
    }
else:
    logger.info("pysnmp not available. SNMPv3 will use snimpy if available.")

# HTTP client for web service detection
HTTP_AVAILABLE = True
try:
    import urllib.error
    import urllib.request
except ImportError:
    HTTP_AVAILABLE = False
    logger.warning("urllib not available. HTTP checks will be disabled.")


@dataclass
class RateLimiter:
    """Rate limiter for controlling scan frequency.

    Implements a token bucket algorithm for rate limiting.
    """

    max_concurrent: int = 10
    tokens_per_second: float = 5.0
    _tokens: float = field(init=False, default=0.0)
    _last_update: float = field(init=False, default=0.0)
    _semaphore: asyncio.Semaphore | None = field(init=False, default=None)

    def __post_init__(self) -> None:
        """Initialize rate limiter state."""
        self._tokens = float(self.max_concurrent)
        self._last_update = time.monotonic()
        self._semaphore = asyncio.Semaphore(self.max_concurrent)

    async def acquire(self) -> None:
        """Acquire a token for scanning."""
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self.max_concurrent)

        await self._semaphore.acquire()

        # Token bucket refill
        now = time.monotonic()
        elapsed = now - self._last_update
        self._tokens = min(
            float(self.max_concurrent), self._tokens + elapsed * self.tokens_per_second
        )
        self._last_update = now

        # Wait if no tokens available
        if self._tokens < 1.0:
            wait_time = (1.0 - self._tokens) / self.tokens_per_second
            await asyncio.sleep(wait_time)
            self._tokens = 1.0

        self._tokens -= 1.0

    def release(self) -> None:
        """Release a token after scanning."""
        if self._semaphore is not None:
            self._semaphore.release()


class NmapDeviceScanner(DeviceScannerService):
    """Implementation of DeviceScannerService using Nmap.

    This scanner uses Nmap for network discovery and port scanning,
    combined with protocol-specific checks for various infrastructure services.

    Supported protocols:
    - SSH (port 22)
    - SNMP v1/v2c/v3 (port 161)
    - MySQL (port 3306)
    - PostgreSQL (port 5432)
    - Redis (port 6379)
    - DNS (port 53)
    - HTTP (port 80)
    - HTTPS (port 443)

    Features:
    - Rate limiting to prevent network saturation
    - OS fingerprinting using Nmap -O
    - HTTP/HTTPS web service detection with header extraction
    - SNMPv3 support with authentication and privacy
    - Custom port configuration per service
    """

    def __init__(
        self,
        rate_limiter: RateLimiter | None = None,
        enable_os_detection: bool = False,
    ) -> None:
        """Initialize the Nmap PortScanner instance.

        Args:
            rate_limiter: Optional rate limiter for controlling scan frequency.
            enable_os_detection: Enable OS fingerprinting (requires root/sudo).
        """
        self._nm = nmap.PortScanner()
        self._rate_limiter = rate_limiter
        self._enable_os_detection = enable_os_detection

    def _get_port(self, device: Device, service: str) -> int:
        """Get the port for a service, checking custom ports first.

        Args:
            device: The device with optional custom port configuration.
            service: The service name (e.g., 'ssh', 'http').

        Returns:
            The port number for the service.
        """
        # Check custom ports
        for port_name, port_num in device.custom_ports:
            if port_name == service:
                return port_num
        # Return default
        return DEFAULT_PORTS.get(service, 0)

    async def scan_device(self, device: Device) -> Device:
        """Scan a device and return an updated device with scan results.

        Performs comprehensive scanning including:
        - Host alive check
        - SSH, SNMP, MySQL service detection
        - HTTP/HTTPS web service detection
        - OS fingerprinting (if enabled)

        Args:
            device: The device to scan.

        Returns:
            A new Device instance with updated scan results.
        """
        # Acquire rate limit token if limiter is configured
        if self._rate_limiter:
            await self._rate_limiter.acquire()

        try:
            alive, alive_errors = await self.is_alive(device)
            device = device.replace(alive=alive)

            # Add any errors from alive check
            for error in alive_errors:
                device = device.add_error(error)

            if alive:
                # Run all service checks concurrently
                results = await asyncio.gather(
                    self.check_ssh(device),
                    self.check_snmp(device),
                    self.check_mysql(device),
                    self.check_postgres(device),
                    self.check_redis(device),
                    self.check_dns(device),
                    self.check_http(device),
                    self.check_https(device),
                    self.detect_os(device)
                    if self._enable_os_detection
                    else self._no_os_detection(),
                )

                ssh_status, ssh_errors = results[0]
                snmp_status, snmp_errors = results[1]
                mysql_status, mysql_errors = results[2]
                postgres_status, postgres_errors = results[3]
                redis_status, redis_errors = results[4]
                dns_status, dns_errors = results[5]
                http_status, http_errors, server_headers = results[6]
                https_status, https_errors, ssl_info = results[7]
                os_fingerprint, os_errors = results[8]

                device = device.replace(
                    ssh=ssh_status,
                    snmp=snmp_status,
                    mysql=mysql_status,
                    postgres=postgres_status,
                    redis_service=redis_status,
                    dns=dns_status,
                    http=http_status,
                    https=https_status,
                    server_headers=server_headers,
                    ssl_info=ssl_info,
                    os_fingerprint=os_fingerprint,
                )

                all_errors = (
                    ssh_errors
                    + snmp_errors
                    + mysql_errors
                    + postgres_errors
                    + redis_errors
                    + dns_errors
                    + http_errors
                    + https_errors
                    + os_errors
                )
                for error in all_errors:
                    device = device.add_error(error)
            elif not alive_errors:
                # Only add "Host is down" if there were no errors explaining why
                device = device.reset_services()
                device = device.add_error("(alive) Host is down")

            device = device.replace(scanned=True)
            return device
        except Exception as e:
            error_msg = f"Exception: {e}"
            device = device.add_error(error_msg)
            device = device.replace(scanned=True)
            logger.error("Error scanning device %s: %s", device.host, e)
            return device
        finally:
            # Release rate limit token
            if self._rate_limiter:
                self._rate_limiter.release()

    async def _no_os_detection(self) -> tuple[str, list[str]]:
        """Return empty OS detection result when disabled."""
        return "", []

    async def is_alive(self, device: Device) -> tuple[bool, list[str]]:
        """Check if a device is alive using Nmap ping scan.

        Args:
            device: The device to check.

        Returns:
            A tuple containing:
            - True if the device is alive, False otherwise
            - A list of error messages, if any
        """
        errors: list[str] = []
        try:
            self._nm.scan(hosts=str(device.ip), arguments="-sn")
            if device.ip in self._nm.all_hosts():
                return self._nm[device.ip].state() == "up", errors
            return False, errors
        except Exception as e:
            error_msg = f"(alive) {e}"
            errors.append(error_msg)
            logger.error("Error checking if device %s is alive: %s", device.host, e)
            return False, errors

    async def is_port_open(self, device: Device, port: int) -> tuple[bool, list[str]]:
        """Check if a specific port is open on a device.

        Args:
            device: The device to check.
            port: The port number to check.

        Returns:
            A tuple containing:
            - A boolean indicating if the port is open
            - A list of error messages, if any
        """
        errors: list[str] = []
        try:
            self._nm.scan(hosts=str(device.ip), arguments=f"-p {port}")
            tcp_ports = self._nm[device.ip].get("tcp", {})
            is_open = tcp_ports.get(port, {}).get("state") == "open"
            return is_open, errors
        except Exception as e:
            error_msg = f"(port {port}) Exception: {e}"
            errors.append(error_msg)
            logger.error("Port scan error on %s:%d - %s", device.host, port, e)
            return False, errors

    async def check_ssh(self, device: Device) -> tuple[bool, list[str]]:
        """Check if SSH is available on a device.

        Attempts to connect to the device via SSH and execute a simple command
        to verify SSH connectivity.

        Args:
            device: The device to check.

        Returns:
            A tuple containing:
            - A boolean indicating if SSH is available
            - A list of error messages, if any
        """
        errors: list[str] = []
        port_open, port_errors = await self.is_port_open(device, 22)
        errors.extend(port_errors)

        if not port_open:
            errors.append("(ssh) Port closed")
            return False, errors

        client = SSHClient()
        try:
            client.load_host_keys(SSH_KNOWN_HOSTS_FILE)
            # Use system host keys if available
            client.load_system_host_keys()

            # Get username from environment or device
            username = SSH_USER or "root"

            client.connect(
                hostname=device.host,
                username=username,
                timeout=10,
                look_for_keys=True,
                allow_agent=True,
            )

            # Execute a simple command to verify connectivity
            _stdin, stdout, stderr = client.exec_command("uname -a")
            _uname_output = stdout.read().decode("utf-8").strip()
            _stderr_output = stderr.read().decode("utf-8").strip()

            return True, errors

        except AuthenticationException as e:
            error_msg = f"(ssh) Authentication failed: {e}"
            errors.append(error_msg)
            logger.warning("SSH auth failed on %s: %s", device.host, e)
            return False, errors

        except SSHException as e:
            error_msg = f"(ssh) SSH error: {e}"
            errors.append(error_msg)
            logger.warning("SSH error on %s: %s", device.host, e)
            return False, errors

        except TimeoutError:
            error_msg = "(ssh) Connection timeout"
            errors.append(error_msg)
            logger.warning("SSH timeout on %s", device.host)
            return False, errors

        except Exception as e:
            error_msg = f"(ssh) Command execution error: {e}"
            errors.append(error_msg)
            logger.error("SSH error on %s: %s", device.host, e)
            return False, errors

        finally:
            with contextlib.suppress(Exception):
                client.close()

    async def check_snmp(self, device: Device) -> tuple[bool, list[str]]:
        """Check if SNMP is available on a device.

        Attempts to query the device's sysName via SNMP to verify connectivity.

        Args:
            device: The device to check.

        Returns:
            A tuple containing:
            - A boolean indicating if SNMP is available
            - A list of error messages, if any
        """
        errors: list[str] = []

        if not SNMP_AVAILABLE:
            errors.append("(snmp) SNMP checks disabled - snimpy not available")
            return False, errors

        port_open, port_errors = await self.is_port_open(device, 161)
        errors.extend(port_errors)

        if not port_open:
            errors.append("(snmp) Port 161 closed")
            return False, errors

        try:
            # Load the SNMP MIB
            snimpy_load("SNMPv2-MIB")

            # Create SNMP manager and query sysName
            manager = SnimpyManager(
                device.ip,
                community=device.snmp_group,
                version=2,
            )

            # Try to access sysName - this will raise if SNMP fails
            _sys_name = manager.sysName

            return True, errors

        except Exception as e:
            error_msg = f"(snmp) {e}"
            errors.append(error_msg)
            logger.warning("SNMP error on %s: %s", device.host, e)
            return False, errors

    async def check_mysql(self, device: Device) -> tuple[bool, list[str]]:  # noqa: PLR0911
        """Check if MySQL is available on a device.

        Attempts to connect to MySQL and execute a version query.

        Args:
            device: The device to check.

        Returns:
            A tuple containing:
            - A boolean indicating if MySQL is available
            - A list of error messages, if any
        """
        errors: list[str] = []

        if not MYSQL_AVAILABLE:
            errors.append("(mysql) MySQL support not available - pymysql not installed")
            return False, errors

        port_open, port_errors = await self.is_port_open(device, 3306)
        errors.extend(port_errors)

        if not port_open:
            errors.append("(mysql) Port closed")
            return False, errors

        # Get MySQL credentials from device or environment
        mysql_user = device.mysql_user or MYSQL_USER
        mysql_password = device.mysql_password or MYSQL_PASSWORD

        if not mysql_user:
            errors.append("(mysql) No MySQL user provided")
            return False, errors

        connection = None
        try:
            connection = pymysql.connect(
                host=device.host,
                user=mysql_user,
                password=mysql_password,
                database="mysql",
                connect_timeout=3,
            )

            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            _version = cursor.fetchone()

            connection.close()
            return True, errors

        except pymysql.err.OperationalError as e:
            error_code = e.args[0] if e.args else 0
            if error_code == 1045:
                error_msg = f"(mysql) Authentication failed: {e}"
            else:
                error_msg = f"(mysql) Connection failed: {e}"
            errors.append(error_msg)
            logger.warning("MySQL error on %s: %s", device.host, e)
            return False, errors

        except pymysql.err.ProgrammingError as e:
            error_msg = f"(mysql) Query error: {e}"
            errors.append(error_msg)
            logger.warning("MySQL query error on %s: %s", device.host, e)
            if connection:
                connection.close()
            return False, errors

        except Exception as e:
            error_msg = f"(mysql) Error: {e}"
            errors.append(error_msg)
            logger.error("MySQL error on %s: %s", device.host, e)
            if connection:
                with contextlib.suppress(Exception):
                    connection.close()
            return False, errors

    async def check_http(  # noqa: PLR0911
        self, device: Device
    ) -> tuple[bool, list[str], str]:
        """Check if HTTP is available on a device.

        Attempts to connect to the device via HTTP and extract server headers.

        Args:
            device: The device to check.

        Returns:
            A tuple containing:
            - A boolean indicating if HTTP is available
            - A list of error messages, if any
            - Server headers string (Server, X-Powered-By, etc.)
        """
        errors: list[str] = []
        server_headers = ""

        if not HTTP_AVAILABLE:
            errors.append("(http) HTTP checks disabled - urllib not available")
            return False, errors, server_headers

        port = self._get_port(device, "http")
        port_open, port_errors = await self.is_port_open(device, port)
        errors.extend(port_errors)

        if not port_open:
            errors.append(f"(http) Port {port} closed")
            return False, errors, server_headers

        try:
            url = f"http://{device.ip}:{port}/"
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "NetworkDiscovery/1.0"},
                method="HEAD",
            )

            with urllib.request.urlopen(request, timeout=5) as response:
                # Extract interesting headers
                headers_dict = {}
                for header in [
                    "Server",
                    "X-Powered-By",
                    "X-AspNet-Version",
                    "X-Generator",
                ]:
                    value = response.headers.get(header)
                    if value:
                        headers_dict[header] = value

                server_headers = "; ".join(f"{k}: {v}" for k, v in headers_dict.items())

                return True, errors, server_headers

        except urllib.error.HTTPError as e:
            # HTTP error but service is responding
            server_headers = e.headers.get("Server", "") if e.headers else ""
            return True, errors, server_headers

        except urllib.error.URLError as e:
            error_msg = f"(http) Connection failed: {e.reason}"
            errors.append(error_msg)
            logger.warning("HTTP error on %s: %s", device.host, e)
            return False, errors, server_headers

        except TimeoutError:
            error_msg = "(http) Connection timeout"
            errors.append(error_msg)
            logger.warning("HTTP timeout on %s", device.host)
            return False, errors, server_headers

        except Exception as e:
            error_msg = f"(http) Error: {e}"
            errors.append(error_msg)
            logger.error("HTTP error on %s: %s", device.host, e)
            return False, errors, server_headers

    async def check_https(self, device: Device) -> tuple[bool, list[str], str]:
        """Check if HTTPS is available on a device.

        Attempts to connect to the device via HTTPS and extract SSL certificate info.

        Args:
            device: The device to check.

        Returns:
            A tuple containing:
            - A boolean indicating if HTTPS is available
            - A list of error messages, if any
            - SSL certificate information string
        """
        errors: list[str] = []
        ssl_info = ""

        port = self._get_port(device, "https")
        port_open, port_errors = await self.is_port_open(device, port)
        errors.extend(port_errors)

        if not port_open:
            errors.append(f"(https) Port {port} closed")
            return False, errors, ssl_info

        try:
            # Create SSL context that doesn't verify certificates
            # (we just want to check if HTTPS is available)
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            # Connect and get certificate
            with (
                socket.create_connection((device.ip, port), timeout=5) as sock,
                context.wrap_socket(sock, server_hostname=device.ip) as ssock,
            ):
                cert = ssock.getpeercert(binary_form=True)

                # Try to parse certificate for basic info
                try:
                    import ssl as ssl_module  # noqa: PLC0415

                    cert_dict = ssl_module._ssl._test_decode_cert(cert)  # type: ignore
                    subject = dict(x[0] for x in cert_dict.get("subject", []))
                    issuer = dict(x[0] for x in cert_dict.get("issuer", []))
                    ssl_info = (
                        f"Subject: {subject.get('commonName', 'N/A')}, "
                        f"Issuer: {issuer.get('commonName', 'N/A')}, "
                        f"Valid: {cert_dict.get('notBefore', 'N/A')} - {cert_dict.get('notAfter', 'N/A')}"
                    )
                except Exception:
                    ssl_info = "SSL certificate present (details unavailable)"

                return True, errors, ssl_info

        except ssl.SSLError as e:
            error_msg = f"(https) SSL error: {e}"
            errors.append(error_msg)
            logger.warning("HTTPS SSL error on %s: %s", device.host, e)
            return False, errors, ssl_info

        except TimeoutError:
            error_msg = "(https) Connection timeout"
            errors.append(error_msg)
            logger.warning("HTTPS timeout on %s", device.host)
            return False, errors, ssl_info

        except ConnectionRefusedError:
            error_msg = "(https) Connection refused"
            errors.append(error_msg)
            return False, errors, ssl_info

        except Exception as e:
            error_msg = f"(https) Error: {e}"
            errors.append(error_msg)
            logger.error("HTTPS error on %s: %s", device.host, e)
            return False, errors, ssl_info

    async def detect_os(self, device: Device) -> tuple[str, list[str]]:
        """Detect the operating system using Nmap OS fingerprinting.

        Uses Nmap's -O flag to perform OS detection. Requires root/sudo privileges.

        Args:
            device: The device to scan.

        Returns:
            A tuple containing:
            - OS fingerprint string (empty if detection failed)
            - A list of error messages, if any
        """
        errors: list[str] = []
        os_fingerprint = ""

        try:
            # Run Nmap with OS detection (-O flag requires root)
            self._nm.scan(hosts=str(device.ip), arguments="-O --osscan-guess")

            if device.ip in self._nm.all_hosts():
                host_info = self._nm[device.ip]

                # Try to get OS matches
                if "osmatch" in host_info:
                    os_matches = host_info["osmatch"]
                    if os_matches:
                        # Get the best match (highest accuracy)
                        best_match = os_matches[0]
                        os_fingerprint = (
                            f"{best_match.get('name', 'Unknown')} "
                            f"({best_match.get('accuracy', 0)}% accuracy)"
                        )
                elif "osclass" in host_info:
                    os_classes = host_info["osclass"]
                    if os_classes:
                        os_class = os_classes[0]
                        os_fingerprint = (
                            f"{os_class.get('osfamily', 'Unknown')} "
                            f"{os_class.get('osgen', '')} "
                            f"({os_class.get('accuracy', 0)}% accuracy)"
                        ).strip()

        except nmap.PortScannerError as e:
            if "root" in str(e).lower() or "permission" in str(e).lower():
                error_msg = "(os) OS detection requires root privileges"
            else:
                error_msg = f"(os) Nmap error: {e}"
            errors.append(error_msg)
            logger.warning("OS detection error on %s: %s", device.host, e)

        except Exception as e:
            error_msg = f"(os) Error: {e}"
            errors.append(error_msg)
            logger.error("OS detection error on %s: %s", device.host, e)

        return os_fingerprint, errors

    async def check_snmp_v3(  # noqa: PLR0911
        self, device: Device
    ) -> tuple[bool, list[str]]:
        """Check if SNMPv3 is available on a device with authentication.

        Uses pysnmp for SNMPv3 authentication and privacy.

        Args:
            device: The device to check.

        Returns:
            A tuple containing:
            - A boolean indicating if SNMPv3 is available
            - A list of error messages, if any
        """
        errors: list[str] = []

        if not PYSNMP_AVAILABLE:
            errors.append("(snmpv3) SNMPv3 requires pysnmp library")
            return False, errors

        if device.snmp_version != 3:
            errors.append("(snmpv3) Device not configured for SNMPv3")
            return False, errors

        if not device.snmpv3_user:
            errors.append("(snmpv3) No SNMPv3 username configured")
            return False, errors

        port = self._get_port(device, "snmp")
        port_open, port_errors = await self.is_port_open(device, port)
        errors.extend(port_errors)

        if not port_open:
            errors.append(f"(snmpv3) Port {port} closed")
            return False, errors

        try:
            # Build authentication parameters
            auth_protocol = SNMPV3_AUTH_PROTOCOLS.get(
                device.snmpv3_auth_protocol.upper(), usmHMACSHAAuthProtocol
            )
            priv_protocol = SNMPV3_PRIV_PROTOCOLS.get(
                device.snmpv3_priv_protocol.upper(), usmAesCfb128Protocol
            )

            # Create user data based on security level
            if device.snmpv3_auth_password and device.snmpv3_priv_password:
                # authPriv - authentication and privacy
                user_data = UsmUserData(
                    device.snmpv3_user,
                    authKey=device.snmpv3_auth_password,
                    privKey=device.snmpv3_priv_password,
                    authProtocol=auth_protocol,
                    privProtocol=priv_protocol,
                )
            elif device.snmpv3_auth_password:
                # authNoPriv - authentication only
                user_data = UsmUserData(
                    device.snmpv3_user,
                    authKey=device.snmpv3_auth_password,
                    authProtocol=auth_protocol,
                )
            else:
                # noAuthNoPriv - no authentication
                user_data = UsmUserData(device.snmpv3_user)

            # Execute SNMPv3 GET request
            iterator = getCmd(
                SnmpEngine(),
                user_data,
                UdpTransportTarget((device.ip, port), timeout=5, retries=1),
                ContextData(),
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysName", 0)),
            )

            error_indication, error_status, _error_index, _var_binds = next(iterator)

            if error_indication:
                error_msg = f"(snmpv3) {error_indication}"
                errors.append(error_msg)
                logger.warning("SNMPv3 error on %s: %s", device.host, error_indication)
                return False, errors

            if error_status:
                error_msg = f"(snmpv3) {error_status.prettyPrint()}"
                errors.append(error_msg)
                logger.warning("SNMPv3 error on %s: %s", device.host, error_status)
                return False, errors

            return True, errors

        except Exception as e:
            error_msg = f"(snmpv3) Error: {e}"
            errors.append(error_msg)
            logger.error("SNMPv3 error on %s: %s", device.host, e)
            return False, errors

    async def check_postgres(self, device: Device) -> tuple[bool, list[str]]:  # noqa: PLR0911
        """Check if PostgreSQL is available on a device.

        Attempts to connect to PostgreSQL and execute a version query.

        Args:
            device: The device to check.

        Returns:
            A tuple containing:
            - A boolean indicating if PostgreSQL is available
            - A list of error messages, if any
        """
        errors: list[str] = []

        if not POSTGRES_AVAILABLE:
            errors.append(
                "(postgres) PostgreSQL support not available - pg8000 not installed"
            )
            return False, errors

        port = self._get_port(device, "postgres")
        port_open, port_errors = await self.is_port_open(device, port)
        errors.extend(port_errors)

        if not port_open:
            errors.append(f"(postgres) Port {port} closed")
            return False, errors

        try:
            # Attempt connection - will fail auth but confirms service is running
            conn = pg8000.connect(
                host=device.ip,
                port=port,
                user="postgres",
                password="",
                database="postgres",
                timeout=3,
            )
            conn.close()
            return True, errors

        except pg8000.exceptions.InterfaceError as e:
            # Connection refused or timeout
            error_msg = f"(postgres) Connection failed: {e}"
            errors.append(error_msg)
            logger.warning("PostgreSQL connection error on %s: %s", device.host, e)
            return False, errors

        except pg8000.exceptions.DatabaseError as e:
            # Authentication failed means PostgreSQL is running
            error_str = str(e)
            if "authentication" in error_str.lower() or "password" in error_str.lower():
                # Service is running, auth just failed
                return True, errors
            error_msg = f"(postgres) Database error: {e}"
            errors.append(error_msg)
            logger.warning("PostgreSQL error on %s: %s", device.host, e)
            return False, errors

        except Exception as e:
            # Check if it's an auth error (service is running)
            error_str = str(e).lower()
            if "authentication" in error_str or "password" in error_str:
                return True, errors
            error_msg = f"(postgres) Error: {e}"
            errors.append(error_msg)
            logger.error("PostgreSQL error on %s: %s", device.host, e)
            return False, errors

    async def check_redis(self, device: Device) -> tuple[bool, list[str]]:  # noqa: PLR0911
        """Check if Redis is available on a device.

        Attempts to connect to Redis and execute a PING command.

        Args:
            device: The device to check.

        Returns:
            A tuple containing:
            - A boolean indicating if Redis is available
            - A list of error messages, if any
        """
        errors: list[str] = []

        if not REDIS_AVAILABLE:
            errors.append("(redis) Redis support not available - redis not installed")
            return False, errors

        port = self._get_port(device, "redis")
        port_open, port_errors = await self.is_port_open(device, port)
        errors.extend(port_errors)

        if not port_open:
            errors.append(f"(redis) Port {port} closed")
            return False, errors

        try:
            client = redis_client.Redis(
                host=device.ip,
                port=port,
                socket_timeout=3,
                socket_connect_timeout=3,
            )
            # PING returns True if successful
            response = client.ping()
            client.close()
            return response, errors

        except redis_client.AuthenticationError:
            # Redis is running but requires auth - still counts as available
            return True, errors

        except redis_client.ConnectionError as e:
            error_msg = f"(redis) Connection failed: {e}"
            errors.append(error_msg)
            logger.warning("Redis connection error on %s: %s", device.host, e)
            return False, errors

        except redis_client.TimeoutError:
            error_msg = "(redis) Connection timeout"
            errors.append(error_msg)
            logger.warning("Redis timeout on %s", device.host)
            return False, errors

        except Exception as e:
            error_msg = f"(redis) Error: {e}"
            errors.append(error_msg)
            logger.error("Redis error on %s: %s", device.host, e)
            return False, errors

    async def check_dns(self, device: Device) -> tuple[bool, list[str]]:
        """Check if DNS service is available on a device.

        Attempts to query the DNS server for a well-known domain.

        Args:
            device: The device to check.

        Returns:
            A tuple containing:
            - A boolean indicating if DNS is available
            - A list of error messages, if any
        """
        errors: list[str] = []

        port = self._get_port(device, "dns")
        port_open, port_errors = await self.is_port_open(device, port)
        errors.extend(port_errors)

        if not port_open:
            errors.append(f"(dns) Port {port} closed")
            return False, errors

        if DNS_AVAILABLE:
            return await self._check_dns_with_dnspython(device, port, errors)
        return await self._check_dns_with_socket(device, port, errors)

    async def _check_dns_with_dnspython(
        self, device: Device, port: int, errors: list[str]
    ) -> tuple[bool, list[str]]:
        """Check DNS using dnspython library."""
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [device.ip]
            resolver.port = port
            resolver.lifetime = 5  # 5 second timeout

            # Try to resolve a well-known domain
            resolver.resolve("google.com", "A")
            return True, errors

        except dns.resolver.NXDOMAIN:
            # Domain doesn't exist but DNS is responding
            return True, errors

        except dns.resolver.NoAnswer:
            # No answer but DNS is responding
            return True, errors

        except dns.resolver.Timeout:
            error_msg = "(dns) Query timeout"
            errors.append(error_msg)
            logger.warning("DNS timeout on %s", device.host)
            return False, errors

        except dns.resolver.NoNameservers:
            error_msg = "(dns) No nameservers available"
            errors.append(error_msg)
            logger.warning("DNS no nameservers on %s", device.host)
            return False, errors

        except Exception as e:
            error_msg = f"(dns) Error: {e}"
            errors.append(error_msg)
            logger.error("DNS error on %s: %s", device.host, e)
            return False, errors

    async def _check_dns_with_socket(
        self, device: Device, port: int, errors: list[str]
    ) -> tuple[bool, list[str]]:
        """Check DNS using basic socket (fallback when dnspython not available)."""
        try:
            # Build a simple DNS query for google.com
            # This is a minimal DNS query packet
            query = (
                b"\x00\x01"  # Transaction ID
                b"\x01\x00"  # Flags: standard query
                b"\x00\x01"  # Questions: 1
                b"\x00\x00"  # Answer RRs: 0
                b"\x00\x00"  # Authority RRs: 0
                b"\x00\x00"  # Additional RRs: 0
                b"\x06google\x03com\x00"  # Query name: google.com
                b"\x00\x01"  # Type: A
                b"\x00\x01"  # Class: IN
            )

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            sock.sendto(query, (device.ip, port))
            response, _ = sock.recvfrom(512)
            sock.close()

            # If we got a response, DNS is working
            return len(response) > 0, errors

        except TimeoutError:
            error_msg = "(dns) Query timeout"
            errors.append(error_msg)
            logger.warning("DNS timeout on %s", device.host)
            return False, errors

        except Exception as e:
            error_msg = f"(dns) Error: {e}"
            errors.append(error_msg)
            logger.error("DNS error on %s: %s", device.host, e)
            return False, errors
