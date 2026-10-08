"""Scan result types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Protocol = Literal["tcp", "udp"]


@dataclass(frozen=True)
class ServiceSpec:
    """A service to look for: a name and where it listens."""

    name: str
    port: int
    protocol: Protocol = "tcp"


@dataclass
class Service:
    """What a probe found for one ServiceSpec on one host."""

    name: str
    port: int
    protocol: Protocol
    state: str


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
