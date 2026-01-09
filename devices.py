"""
Network device discovery and scanning module.

This module provides functionality for discovering network devices and checking
their availability for various services (ping, SSH, SNMP, MySQL).

Requires Python 3.14+
"""

from __future__ import annotations

import ipaddress
import logging
import os
import re
import subprocess
from dataclasses import dataclass, field
from enum import StrEnum, auto
from functools import cached_property
from pathlib import Path
from typing import Self

import paramiko
import MySQLdb
from snimpy.manager import Manager as SnmpManager
from snimpy.manager import load as load_mib

# Type aliases using Python 3.12+ syntax
type HostStr = str
type ErrorList = list[str]
type ScanData = dict[str, str | int | bool | None]

# Configure module logger
logger = logging.getLogger(__name__)


class ScanType(StrEnum):
    """Types of network scans that can be performed."""
    PING = auto()
    SNMP = auto()
    SSH = auto()
    MYSQL = auto()


class DeviceStatus(StrEnum):
    """Device connectivity status."""
    UNKNOWN = auto()
    UP = auto()
    DOWN = auto()
    ERROR = auto()


class ValidationError(Exception):
    """Raised when input validation fails."""
    __slots__ = ('value', 'reason')

    def __init__(self, message: str, value: str | None = None, reason: str | None = None) -> None:
        super().__init__(message)
        self.value = value
        self.reason = reason


# Validation pattern - compiled once at module load
_HOSTNAME_PATTERN: re.Pattern[str] = re.compile(
    r'^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})*$'
)

# Dangerous shell characters for defense-in-depth validation
_DANGEROUS_CHARS: frozenset[str] = frozenset(';|&$`\\"\'\n\r\t<>()')


def validate_host(value: str | None) -> HostStr:
    """
    Validate and sanitize a hostname or IP address.

    This function prevents command injection by ensuring the host value
    contains only valid hostname or IP address characters.

    Args:
        value: The hostname or IP address to validate

    Returns:
        The validated hostname/IP as a string

    Raises:
        ValidationError: If the hostname/IP is invalid or None
    """
    match value:
        case None:
            raise ValidationError("Host cannot be None", value=None, reason="null_value")
        case str() as s if not (stripped := s.strip()):
            raise ValidationError("Host cannot be empty", value=s, reason="empty_value")
        case str() as s if any(c in s for c in _DANGEROUS_CHARS):
            raise ValidationError(
                f"Host contains invalid characters: {s}",
                value=s,
                reason="dangerous_chars"
            )
        case str() as s:
            stripped = s.strip()
            # Try parsing as IP address first
            try:
                return str(ipaddress.ip_address(stripped))
            except ValueError:
                pass

            # Validate as hostname
            if _HOSTNAME_PATTERN.match(stripped):
                return stripped

            raise ValidationError(
                f"Invalid hostname or IP address: {stripped}",
                value=stripped,
                reason="invalid_format"
            )
        case _:
            raise ValidationError(
                f"Host must be a string, got {type(value).__name__}",
                value=str(value),
                reason="invalid_type"
            )


@dataclass(slots=True, kw_only=True)
class ScanConfig:
    """Configuration for network scanning operations."""

    ssh_user: str = field(default_factory=lambda: os.environ.get('SSH_USER', 'root'))
    ssh_key_file: Path = field(
        default_factory=lambda: Path(
            os.environ.get('SSH_KEY_FILE', Path.home() / '.ssh' / 'known_hosts')
        )
    )
    ssh_timeout: int = 3
    ping_timeout: int = 20
    ping_count: int = 1
    snmp_timeout: int = 2
    snmp_version: int = 2
    snmp_default_community: str = "public"
    mysql_timeout: int = 5

    # Security settings - strict by default
    ssh_strict_host_key: bool = field(
        default_factory=lambda: os.environ.get('SSH_STRICT_HOST_KEY', 'true').lower() == 'true'
    )

    @cached_property
    def ssh_policy(self) -> paramiko.MissingHostKeyPolicy:
        """Get the appropriate SSH host key policy based on configuration."""
        if self.ssh_strict_host_key:
            return paramiko.RejectPolicy()
        logger.warning("SSH strict host key checking is disabled - vulnerable to MITM attacks")
        return paramiko.WarningPolicy()


# Module-level default configuration
_default_config: ScanConfig = ScanConfig()


@dataclass(slots=True, kw_only=True)
class ScanResult:
    """Result of a network scan operation."""

    scan_type: ScanType
    success: bool
    error: str | None = None
    data: ScanData = field(default_factory=dict)

    @property
    def failed(self) -> bool:
        """Check if the scan failed."""
        return not self.success

    def __bool__(self) -> bool:
        """Allow using ScanResult in boolean context."""
        return self.success


@dataclass(slots=True)
class Device:
    """
    Represents a network device that can be scanned.

    This class uses slots for memory efficiency and provides methods
    for scanning various network services.
    """

    id: int
    host: HostStr
    ip: HostStr
    snmp_community: str = "public"
    alive: bool = False
    snmp: bool = False
    ssh: bool = False
    mysql: bool = False
    errors: ErrorList = field(default_factory=list)
    mysql_user: str = ""
    _mysql_password: str = field(default="", repr=False)
    uname: str = ""
    scanned: bool = False

    def __post_init__(self) -> None:
        """Validate device attributes after initialization."""
        self.host = validate_host(self.host)
        self.ip = validate_host(self.ip) if self.ip else self.host
        self.snmp_community = self.snmp_community or "public"
        # Ensure errors is a mutable list
        if not isinstance(self.errors, list):
            self.errors = list(self.errors) if self.errors else []

    @property
    def mysql_password(self) -> str:
        """Get MySQL password."""
        return self._mysql_password

    @mysql_password.setter
    def mysql_password(self, value: str) -> None:
        """Set MySQL password."""
        self._mysql_password = value or ""

    @property
    def status(self) -> DeviceStatus:
        """Get the current device status."""
        match (self.scanned, self.alive, bool(self.errors)):
            case (False, _, _):
                return DeviceStatus.UNKNOWN
            case (True, True, _):
                return DeviceStatus.UP
            case (True, False, True):
                return DeviceStatus.ERROR
            case (True, False, False):
                return DeviceStatus.DOWN
            case _:
                return DeviceStatus.UNKNOWN

    def add_error(self, message: str) -> None:
        """Add an error message to the device's error list."""
        self.errors.append(message)
        logger.debug("Device %s error: %s", self.host, message)

    def clear_errors(self) -> None:
        """Clear all error messages."""
        self.errors.clear()

    def scan_ping(self, config: ScanConfig | None = None) -> ScanResult:
        """Check if the device responds to ICMP ping."""
        config = config or _default_config

        try:
            validated_host = validate_host(self.host)
            result = subprocess.run(
                ["ping", "-c", str(config.ping_count), "-W", str(config.ping_timeout), validated_host],
                capture_output=True,
                timeout=config.ping_timeout + 5,
                check=False,
            )
            self.alive = result.returncode == 0

            if not self.alive:
                self.add_error("(ping) Host unreachable")

            return ScanResult(
                scan_type=ScanType.PING,
                success=self.alive,
                data={"output": result.stdout.decode(errors='replace')},
            )

        except subprocess.TimeoutExpired:
            self.alive = False
            self.add_error("(ping) Timeout")
            return ScanResult(scan_type=ScanType.PING, success=False, error="Timeout")

        except ValidationError as e:
            self.alive = False
            self.add_error(f"(ping) {e}")
            return ScanResult(scan_type=ScanType.PING, success=False, error=str(e))

        except OSError as e:
            self.alive = False
            self.add_error(f"(ping) {e}")
            logger.exception("OS error during ping scan of %s", self.host)
            return ScanResult(scan_type=ScanType.PING, success=False, error=str(e))

    def scan_ssh(self, config: ScanConfig | None = None) -> ScanResult:
        """Check if SSH is accessible on the device."""
        config = config or _default_config
        ssh_client = paramiko.SSHClient()

        try:
            validated_host = validate_host(self.host)

            # Load known hosts if file exists
            if config.ssh_key_file.exists():
                ssh_client.load_host_keys(str(config.ssh_key_file))

            ssh_client.set_missing_host_key_policy(config.ssh_policy)

            ssh_client.connect(
                validated_host,
                username=config.ssh_user,
                timeout=config.ssh_timeout,
                look_for_keys=True,
                allow_agent=True,
            )

            _, stdout, _ = ssh_client.exec_command('uname -a')
            self.uname = stdout.read().decode(errors='replace').strip()
            self.ssh = True

            return ScanResult(
                scan_type=ScanType.SSH,
                success=True,
                data={"uname": self.uname},
            )

        except paramiko.AuthenticationException as e:
            self.ssh = False
            self.add_error(f"(ssh) Authentication failed: {e}")
            return ScanResult(scan_type=ScanType.SSH, success=False, error=str(e))

        except paramiko.SSHException as e:
            self.ssh = False
            self.add_error(f"(ssh) SSH error: {e}")
            return ScanResult(scan_type=ScanType.SSH, success=False, error=str(e))

        except OSError as e:
            self.ssh = False
            self.add_error(f"(ssh) Connection error: {e}")
            return ScanResult(scan_type=ScanType.SSH, success=False, error=str(e))

        except ValidationError as e:
            self.ssh = False
            self.add_error(f"(ssh) {e}")
            return ScanResult(scan_type=ScanType.SSH, success=False, error=str(e))

        finally:
            ssh_client.close()

    def scan_snmp(self, config: ScanConfig | None = None) -> ScanResult:
        """Check if SNMP is accessible on the device."""
        config = config or _default_config

        try:
            validated_host = validate_host(self.host)
            load_mib("SNMPv2-MIB")

            manager = SnmpManager(
                host=validated_host,
                community=self.snmp_community,
                version=config.snmp_version,
                timeout=config.snmp_timeout,
            )

            sys_name = manager.sysName
            self.snmp = sys_name is not None

            return ScanResult(
                scan_type=ScanType.SNMP,
                success=self.snmp,
                data={"sysName": str(sys_name) if sys_name else None},
            )

        except ValidationError as e:
            self.snmp = False
            self.add_error(f"(snmp) {e}")
            return ScanResult(scan_type=ScanType.SNMP, success=False, error=str(e))

        except Exception as e:
            self.snmp = False
            self.add_error(f"(snmp) {e}")
            logger.debug("SNMP scan failed for %s: %s", self.host, e)
            return ScanResult(scan_type=ScanType.SNMP, success=False, error=str(e))

    def scan_mysql(self, config: ScanConfig | None = None) -> ScanResult:
        """Check if MySQL is accessible on the device."""
        config = config or _default_config

        if not self.mysql_user:
            self.add_error("(mysql) No credentials provided")
            return ScanResult(
                scan_type=ScanType.MYSQL,
                success=False,
                error="No MySQL credentials provided",
            )

        connection = None

        try:
            validated_host = validate_host(self.host)

            connection = MySQLdb.connect(
                host=validated_host,
                user=self.mysql_user,
                passwd=self._mysql_password,
                connect_timeout=config.mysql_timeout,
            )

            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                result = cursor.fetchone()

            self.mysql = result is not None
            version = result[0] if result else None

            return ScanResult(
                scan_type=ScanType.MYSQL,
                success=self.mysql,
                data={"version": version},
            )

        except MySQLdb.Error as e:
            self.mysql = False
            self.add_error(f"(mysql) {e}")
            return ScanResult(scan_type=ScanType.MYSQL, success=False, error=str(e))

        except ValidationError as e:
            self.mysql = False
            self.add_error(f"(mysql) {e}")
            return ScanResult(scan_type=ScanType.MYSQL, success=False, error=str(e))

        finally:
            if connection is not None:
                connection.close()

    def scan_all(self, config: ScanConfig | None = None) -> list[ScanResult]:
        """Perform all applicable scans on the device."""
        config = config or _default_config
        results: list[ScanResult] = []

        results.append(self.scan_ping(config))

        if self.alive:
            results.append(self.scan_snmp(config))
            results.append(self.scan_ssh(config))

            if self.mysql_user:
                results.append(self.scan_mysql(config))

        self.scanned = True
        return results

    def to_dict(self, *, mask_credentials: bool = True) -> ScanData:
        """Convert device to dictionary representation."""
        return {
            "id": self.id,
            "host": self.host,
            "ip": self.ip,
            "snmp_community": "***" if mask_credentials else self.snmp_community,
            "alive": self.alive,
            "snmp": self.snmp,
            "ssh": self.ssh,
            "mysql": self.mysql,
            "mysql_user": self.mysql_user,
            "mysql_password": "***" if mask_credentials else self._mysql_password,
            "uname": self.uname,
            "errors": self.errors.copy(),
            "scanned": self.scanned,
            "status": self.status.value,
        }

    def __repr__(self) -> str:
        return f"Device(id={self.id}, host={self.host!r}, ip={self.ip!r}, status={self.status.value})"

    def __str__(self) -> str:
        parts = [f"{self.host} ({self.ip})"]
        if self.scanned:
            services = []
            if self.alive:
                services.append("alive")
            if self.ssh:
                services.append("ssh")
            if self.snmp:
                services.append("snmp")
            if self.mysql:
                services.append("mysql")
            parts.append(f"[{', '.join(services) or 'no services'}]")
        else:
            parts.append("[not scanned]")
        return " ".join(parts)

    @classmethod
    def from_dict(cls, data: ScanData) -> Self:
        """Create a Device instance from a dictionary."""
        return cls(
            id=int(data.get('id', 0)),
            host=str(data.get('host', '')),
            ip=str(data.get('ip', data.get('host', ''))),
            snmp_community=str(data.get('snmp_community', data.get('snmp_group', 'public'))),
            alive=bool(data.get('alive', False)),
            snmp=bool(data.get('snmp', False)),
            ssh=bool(data.get('ssh', False)),
            mysql=bool(data.get('mysql', False)),
            errors=list(data.get('errors', [])),
            mysql_user=str(data.get('mysql_user', '')),
            _mysql_password=str(data.get('mysql_password', '')),
            uname=str(data.get('uname', '')),
            scanned=bool(data.get('scanned', False)),
        )
