"""Device domain model for the network discovery tool.

This module defines the Device entity, which represents a network device
and its key properties. The Device class is implemented as an immutable
dataclass to ensure consistency and thread safety.
"""

from __future__ import annotations

import ipaddress
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Device:
    """Represents a network device and its properties.

    This is the core domain entity that represents a device on the network.
    It contains all the properties and state of a network device.

    This class is immutable (frozen) to make it hashable and usable in sets.
    Methods that modify the device's state will return a new Device instance.

    Attributes:
        id: Unique identifier for the device (must be positive integer).
        host: Hostname or IP address string for the device (non-empty).
        ip: IP address of the device (must be valid IP format).
        snmp_group: SNMP community string for the device (non-empty).
        alive: Whether the device is reachable on the network.
        snmp: Whether SNMP is available on the device.
        ssh: Whether SSH is available on the device.
        mysql: Whether MySQL is available on the device.
        http: Whether HTTP is available on the device.
        https: Whether HTTPS is available on the device.
        postgres: Whether PostgreSQL is available on the device.
        redis_service: Whether Redis is available on the device.
        dns: Whether DNS is available on the device.
        mysql_user: Username for MySQL authentication.
        mysql_password: Password for MySQL authentication.
        uname: Output of uname command if available.
        os_fingerprint: Operating system fingerprint from Nmap -O scan.
        server_headers: HTTP server headers (Server, X-Powered-By, etc.).
        ssl_info: SSL/TLS certificate information.
        snmp_version: SNMP version to use (1, 2, or 3).
        snmpv3_user: SNMPv3 username for authentication.
        snmpv3_auth_protocol: SNMPv3 auth protocol (MD5, SHA, SHA256, etc.).
        snmpv3_auth_password: SNMPv3 authentication password.
        snmpv3_priv_protocol: SNMPv3 privacy protocol (DES, AES, AES256, etc.).
        snmpv3_priv_password: SNMPv3 privacy password.
        custom_ports: Custom port mappings for non-standard services.
        errors: Tuple of error messages encountered during scanning.
        scanned: Whether the device has been scanned.

    Raises:
        ValueError: If id is not a positive integer, host is empty,
            ip is empty or invalid, or snmp_group is empty.
    """

    id: int
    host: str
    ip: str
    snmp_group: str = "public"
    alive: bool = False
    snmp: bool = False
    ssh: bool = False
    mysql: bool = False
    http: bool = False
    https: bool = False
    postgres: bool = False
    redis_service: bool = False
    dns: bool = False
    mysql_user: str = ""
    mysql_password: str = ""
    uname: str = ""
    os_fingerprint: str = ""
    server_headers: str = ""
    ssl_info: str = ""
    snmp_version: int = 2
    snmpv3_user: str = ""
    snmpv3_auth_protocol: str = ""
    snmpv3_auth_password: str = ""
    snmpv3_priv_protocol: str = ""
    snmpv3_priv_password: str = ""
    custom_ports: tuple[tuple[str, int], ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    scanned: bool = False

    def __post_init__(self) -> None:
        """Validate device attributes after initialization.

        Raises:
            ValueError: If any validation fails.
        """
        # Validate id is an integer
        if not isinstance(self.id, int):
            raise ValueError(f"id must be an integer, got {type(self.id).__name__}")

        # Validate id is positive
        if self.id < 0:
            raise ValueError(f"id must be non-negative, got {self.id}")

        # Validate host is not empty
        if not self.host or not self.host.strip():
            raise ValueError("host cannot be empty")

        # Validate ip is not empty
        if not self.ip or not self.ip.strip():
            raise ValueError("ip cannot be empty")

        # Validate ip format
        try:
            ipaddress.ip_address(self.ip)
        except ValueError as e:
            raise ValueError(f"ip must be a valid IP address: {e}") from e

        # Validate snmp_group is not empty
        if not self.snmp_group or not self.snmp_group.strip():
            raise ValueError("snmp_group cannot be empty")

        # Validate snmp_group length (max 255 characters for SNMP community strings)
        if len(self.snmp_group) > 255:
            raise ValueError(
                f"snmp_group cannot exceed 255 characters, got {len(self.snmp_group)}"
            )

    def add_error(self, msg: str) -> Device:
        """Add an error message to the device's error log.

        Creates a new Device instance with the error message added to the errors tuple,
        preserving immutability.

        Args:
            msg: The error message to add.

        Returns:
            A new Device instance with the error message added.
        """
        return self.replace(errors=(*self.errors, msg))

    def reset_services(self) -> Device:
        """Reset the statuses of all services to their default values.

        Creates a new Device instance with all service flags reset to False and
        the uname field reset to "unknown".

        Returns:
            A new Device instance with services reset.
        """
        return self.replace(
            ssh=False,
            snmp=False,
            mysql=False,
            http=False,
            https=False,
            postgres=False,
            redis_service=False,
            dns=False,
            uname="unknown",
            os_fingerprint="",
            server_headers="",
            ssl_info="",
        )

    def replace(self, **kwargs: Any) -> Device:
        """Create a new Device with some fields replaced.

        This method preserves immutability by creating a new Device instance
        with specified fields replaced with new values.

        Args:
            **kwargs: The fields to replace and their new values. Keys should
                match attribute names of the Device class.

        Returns:
            A new Device instance with the specified fields replaced.
        """
        # Create a dictionary of the current field values
        fields = self.to_dict()

        # Update with the new values
        fields.update(kwargs)

        # Create a new Device instance
        return Device.from_dict(fields)

    def to_dict(self, mask_sensitive: bool = False) -> dict[str, Any]:
        """Convert the device attributes to a dictionary.

        Creates a dictionary containing all the device's attributes. The errors
        tuple is converted to a list for better serialization compatibility.

        Args:
            mask_sensitive: If True, mask sensitive fields like passwords.

        Returns:
            A dictionary representation of the device with all attributes.
        """

        # Helper function to mask sensitive values
        def mask_value(value: str) -> str:
            if not value or not mask_sensitive:
                return value
            return "****" if len(value) > 0 else ""

        return {
            "id": self.id,
            "host": self.host,
            "ip": self.ip,
            "snmp_group": self.snmp_group,
            "alive": self.alive,
            "snmp": self.snmp,
            "ssh": self.ssh,
            "mysql": self.mysql,
            "http": self.http,
            "https": self.https,
            "postgres": self.postgres,
            "redis_service": self.redis_service,
            "dns": self.dns,
            "mysql_user": self.mysql_user,
            "mysql_password": mask_value(self.mysql_password),
            "uname": self.uname,
            "os_fingerprint": self.os_fingerprint,
            "server_headers": self.server_headers,
            "ssl_info": self.ssl_info,
            "snmp_version": self.snmp_version,
            "snmpv3_user": self.snmpv3_user,
            "snmpv3_auth_protocol": self.snmpv3_auth_protocol,
            "snmpv3_auth_password": mask_value(self.snmpv3_auth_password),
            "snmpv3_priv_protocol": self.snmpv3_priv_protocol,
            "snmpv3_priv_password": mask_value(self.snmpv3_priv_password),
            "custom_ports": [list(p) for p in self.custom_ports],
            "errors": list(self.errors),  # Convert tuple to list for serialization
            "scanned": self.scanned,
        }

    @classmethod
    def from_dict(cls, dict_device: dict[str, Any]) -> Device:
        """Create a Device object from a dictionary.

        Constructs a new Device instance from a dictionary representation. This
        method handles type conversions and applies defaults for missing values.

        Args:
            dict_device: A dictionary containing device attributes. Must include
                at least 'id', 'host', and 'ip' keys.

        Returns:
            A new Device instance initialized with values from the dictionary.

        Raises:
            KeyError: If required keys ('id', 'host', 'ip') are missing from the dictionary.
            ValueError: If validation fails for any field.
        """
        # Convert errors list to tuple for immutability
        errors = dict_device.get("errors", [])
        if isinstance(errors, list):
            errors = tuple(errors)

        # Convert custom_ports list to tuple of tuples
        custom_ports = dict_device.get("custom_ports", [])
        if isinstance(custom_ports, list):
            custom_ports = tuple(tuple(p) for p in custom_ports)

        return cls(
            id=dict_device["id"],
            host=str(dict_device["host"]),
            ip=str(dict_device["ip"]),
            snmp_group=str(dict_device.get("snmp_group", "public")),
            alive=dict_device.get("alive", False),
            snmp=dict_device.get("snmp", False),
            ssh=dict_device.get("ssh", False),
            mysql=dict_device.get("mysql", False),
            http=dict_device.get("http", False),
            https=dict_device.get("https", False),
            postgres=dict_device.get("postgres", False),
            redis_service=dict_device.get("redis_service", False),
            dns=dict_device.get("dns", False),
            mysql_user=str(dict_device.get("mysql_user", "")),
            mysql_password=str(dict_device.get("mysql_password", "")),
            uname=str(dict_device.get("uname", "")),
            os_fingerprint=str(dict_device.get("os_fingerprint", "")),
            server_headers=str(dict_device.get("server_headers", "")),
            ssl_info=str(dict_device.get("ssl_info", "")),
            snmp_version=int(dict_device.get("snmp_version", 2)),
            snmpv3_user=str(dict_device.get("snmpv3_user", "")),
            snmpv3_auth_protocol=str(dict_device.get("snmpv3_auth_protocol", "")),
            snmpv3_auth_password=str(dict_device.get("snmpv3_auth_password", "")),
            snmpv3_priv_protocol=str(dict_device.get("snmpv3_priv_protocol", "")),
            snmpv3_priv_password=str(dict_device.get("snmpv3_priv_password", "")),
            custom_ports=custom_ports,
            errors=errors,
            scanned=dict_device.get("scanned", False),
        )

    def status(self) -> str:
        """Return a string summarizing the device's status.

        Creates a human-readable summary of the device's status, including
        its host, availability, service status, and any errors encountered.

        Returns:
            A string representation of the device's status.
        """
        services = []
        if self.ssh:
            services.append("ssh")
        if self.snmp:
            services.append(f"snmp(v{self.snmp_version})")
        if self.mysql:
            services.append("mysql")
        if self.postgres:
            services.append("postgres")
        if self.redis_service:
            services.append("redis")
        if self.dns:
            services.append("dns")
        if self.http:
            services.append("http")
        if self.https:
            services.append("https")

        services_str = ", ".join(services) if services else "none"
        os_info = f", os: {self.os_fingerprint}" if self.os_fingerprint else ""

        return (
            f"{self.host} -> alive: {self.alive}, services: [{services_str}]"
            f"{os_info}, errors: {len(self.errors)}"
        )

    def __repr__(self) -> str:
        """Return a developer-friendly string representation of the device.

        Returns:
            A concise string representation of the device with host and IP.
        """
        return f"{self.host} ({self.ip})"

    def __str__(self) -> str:
        """Return a user-friendly string representation of the device.

        Returns:
            A detailed string representation of the device (dictionary format).
        """
        return str(self.to_dict())

    def __hash__(self) -> int:
        """Return a hash of the device for use in hash-based collections.

        The hash is based solely on the device's ID, which should be unique.

        Returns:
            A hash value based on the device's ID.
        """
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        """Return whether this device equals another object.

        Two devices are considered equal if they have the same ID.
        This method properly handles comparison with non-Device objects.

        Args:
            other: The other object to compare with.

        Returns:
            True if other is a Device with the same ID, False otherwise.
        """
        if not isinstance(other, Device):
            return False
        return self.id == other.id
