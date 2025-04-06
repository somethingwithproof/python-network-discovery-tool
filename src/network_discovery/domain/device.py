"""Device domain model.

This module defines the Device entity, which represents a network device and its properties.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Device:
    """Represents a network device and its properties.

    This is the core domain entity that represents a device on the network.
    It contains all the properties and state of a network device.
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
    errors: List[str] = field(default_factory=list)
    scanned: bool = False

    def add_error(self, msg: str) -> None:
        """Add an error message to the device's error log.

        Args:
            msg: The error message to add.
        """
        self.errors.append(msg)

    def reset_services(self) -> None:
        """Reset the statuses of all services."""
        self.ssh = False
        self.snmp = False
        self.mysql = False
        self.uname = "unknown"

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
            "errors": self.errors,
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
            errors=dict_device["errors"],
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
