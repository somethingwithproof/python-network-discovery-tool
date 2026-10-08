"""Scan result types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

Protocol = Literal["tcp", "udp"]

# Services that have a boolean field of their own in the original output.
LEGACY_FLAGS = ("ssh", "snmp", "mysql")


@dataclass(frozen=True)
class ServiceSpec:
    """A service to look for: its name, where it listens and how to probe it."""

    name: str
    port: int
    protocol: Protocol = "tcp"
    probe: str = "tcp"


@dataclass
class Service:
    """What a probe found for one ServiceSpec on one host."""

    name: str
    port: int
    protocol: Protocol
    state: str
    # Product and version the service announced, e.g. "OpenSSH_9.6"; "" if none.
    version: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class Device:
    """Network device with scan results.

    ssh, snmp and mysql predate the services list and are kept so existing
    JSON and CSV consumers keep working.
    """

    ip: str
    alive: bool = False
    ssh: bool = False
    snmp: bool = False
    mysql: bool = False
    hostname: str = ""
    errors: list[str] = field(default_factory=list)
    services: list[Service] = field(default_factory=list)

    @property
    def open_services(self) -> list[Service]:
        return [s for s in self.services if s.state == "open"]
