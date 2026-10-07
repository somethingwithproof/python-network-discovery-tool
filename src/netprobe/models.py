"""Scan result types."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Device:
    """Network device with scan results."""

    ip: str
    alive: bool = False
    ssh: bool = False
    snmp: bool = False
    mysql: bool = False
    hostname: str = ""
    errors: list[str] = field(default_factory=list)
