"""Device domain model for the network discovery tool.

This module defines the Device entity, which represents a network device
and its key properties. The Device class is implemented as an immutable
dataclass to ensure consistency and thread safety.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class Device:
    """Represents a network device and its properties.

    This is the core domain entity that represents a device on the network.
    It contains all the properties and state of a network device.

    This class is immutable (frozen) to make it hashable and usable in sets.
    Methods that modify the device's state will return a new Device instance.

    Attributes:
        id: Unique identifier for the device.
        host: Hostname or IP address string for the device.
        ip: IP address of the device.
        snmp_group: SNMP community string for the device.
        alive: Whether the device is reachable on the network.
        snmp: Whether SNMP is available on the device.
        ssh: Whether SSH is available on the device.
        mysql: Whether MySQL is available on the device.
        mysql_user: Username for MySQL authentication.
        mysql_password: Password for MySQL authentication.
        uname: Output of uname command if available.
        errors: Tuple of error messages encountered during scanning.
        scanned: Whether the device has been scanned.
    """

    id: int
    host: str
    ip: str
    snmp_group: str = "public"
    alive: bool = False
    snmp: bool = False
    ssh: bool = False
    mysql: bool = False
    mysql_user: str = ""
    mysql_password: str = ""
    uname: str = ""
    errors: Tuple[str, ...] = field(default_factory=tuple)
    scanned: bool = False

    def add_error(self, msg: str) -> "Device":
        """Add an error message to the device's error log.

        Creates a new Device instance with the error message added to the errors tuple,
        preserving immutability.

        Args:
            msg: The error message to add.

        Returns:
            A new Device instance with the error message added.
        """
        return self.replace(errors=self.errors + (msg,))

    def reset_services(self) -> "Device":
        """Reset the statuses of all services to their default values.

        Creates a new Device instance with all service flags reset to False and
        the uname field reset to "unknown".

        Returns:
            A new Device instance with services reset.
        """
        return self.replace(ssh=False, snmp=False, mysql=False, uname="unknown")

    def replace(self, **kwargs) -> "Device":
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

    def to_dict(self) -> Dict[str, Any]:
        """Convert the device attributes to a dictionary.

        Creates a dictionary containing all the device's attributes. The errors
        tuple is converted to a list for better serialization compatibility.

        Returns:
            A dictionary representation of the device with all attributes.
        """
        return {
            "id": self.id,
            "host": self.host,
            "ip": self.ip,
            "snmp_group": self.snmp_group,
            "alive": self.alive,
            "snmp": self.snmp,
            "ssh": self.ssh,
            "mysql": self.mysql,
            "mysql_user": self.mysql_user,
            "mysql_password": self.mysql_password,
            "uname": self.uname,
            "errors": list(
                self.errors
            ),  # Convert tuple to list for serialization
            "scanned": self.scanned,
        }

    @classmethod
    def from_dict(cls, dict_device: Dict[str, Any]) -> "Device":
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
        """
        # Convert errors list to tuple for immutability
        errors = dict_device.get("errors", [])
        if isinstance(errors, list):
            errors = tuple(errors)

        return cls(
            id=dict_device["id"],
            host=str(dict_device["host"]),
            ip=str(dict_device["ip"]),
            snmp_group=str(dict_device.get("snmp_group", "public")),
            alive=dict_device.get("alive", False),
            snmp=dict_device.get("snmp", False),
            ssh=dict_device.get("ssh", False),
            mysql=dict_device.get("mysql", False),
            mysql_user=str(dict_device.get("mysql_user", "")),
            mysql_password=str(dict_device.get("mysql_password", "")),
            uname=str(dict_device.get("uname", "")),
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
        return (
            f"{self.host} -> alive: {self.alive}, ssh: {self.ssh}, "
            f"snmp: {self.snmp}, mysql: {self.mysql}, "
            f"info: {', '.join(self.errors)}"
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
