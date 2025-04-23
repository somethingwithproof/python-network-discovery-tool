"""Device domain model.

This module defines the Device entity, which represents a network device and its properties.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Tuple


@dataclass(frozen=True)
class Device:
    """Represents a network device and its properties.

    This is the core domain entity that represents a device on the network.
    It contains all the properties and state of a network device.

    This class is immutable (frozen) to make it hashable, which allows it to be used in sets.
    Methods that modify the device's state will return a new Device instance.
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

        Args:
            msg: The error message to add.

        Returns:
            A new Device instance with the error added.
        """
        return self.replace(errors=self.errors + (msg,))

    def reset_services(self) -> "Device":
        """Reset the statuses of all services.

        Returns:
            A new Device instance with services reset.
        """
        return self.replace(ssh=False, snmp=False, mysql=False, uname="unknown")

    def replace(self, **kwargs) -> "Device":
        """Create a new Device with some fields replaced.

        Args:
            **kwargs: The fields to replace and their new values.

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

        Returns:
            A dictionary representation of the device.
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
            "errors": list(self.errors),
            "scanned": self.scanned,
        }

    @classmethod
    def from_dict(cls, dict_device: Dict[str, Any]) -> "Device":
        """Create a Device object from a dictionary.

        Args:
            dict_device: A dictionary containing device attributes.

        Returns:
            A new Device instance.
        """
        # Convert errors list to tuple for immutability
        errors = dict_device.get("errors", [])
        if isinstance(errors, list):
            errors = tuple(errors)

        return cls(
            id=dict_device["id"],
            host=str(dict_device["host"]),
            ip=str(dict_device["ip"]),
            snmp_group=str(dict_device["snmp_group"]),
            alive=dict_device["alive"],
            snmp=dict_device["snmp"],
            ssh=dict_device["ssh"],
            mysql=dict_device["mysql"],
            mysql_user=str(dict_device["mysql_user"]),
            mysql_password=str(dict_device["mysql_password"]),
            uname=str(dict_device["uname"]),
            errors=errors,
            scanned=dict_device["scanned"],
        )

    def status(self) -> str:
        """Return a string summarizing the device's status.

        Returns:
            A string representation of the device's status.
        """
        return (
            f"{self.host} -> alive: {self.alive}, ssh: {self.ssh}, "
            f"snmp: {self.snmp}, mysql: {self.mysql}, "
            f"info: {', '.join(self.errors)}"
        )

    def __repr__(self) -> str:
        """Return a string representation of the device.

        Returns:
            A string representation of the device.
        """
        return f"{self.host} ({self.ip})"

    def __str__(self) -> str:
        """Return a string representation of the device.

        Returns:
            A string representation of the device.
        """
        return str(self.to_dict())

    def __hash__(self) -> int:
        """Return a hash of the device.

        Returns:
            A hash value based on the device's ID, host, and IP.
        """
        return hash((self.id, self.host, self.ip))
