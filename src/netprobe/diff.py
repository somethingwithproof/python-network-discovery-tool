"""Versioned scan snapshots and the comparison between two of them."""

from __future__ import annotations

import ipaddress
import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from importlib.metadata import version as package_version
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.markup import escape
from rich.table import Table

from netprobe.models import Device, ServiceSpec

SNAPSHOT_FORMAT = "netprobe-snapshot"
SNAPSHOT_VERSION = 1

# Ports a pre-2.1 report could only express as booleans.
LEGACY_PORTS = {"ssh": (22, "tcp"), "snmp": (161, "udp"), "mysql": (3306, "tcp")}

Port = tuple[int, str]


class SnapshotError(ValueError):
    """A file is not a snapshot or report this version can read."""


def write_snapshot(
    path: Path, network: str, services: tuple[ServiceSpec, ...], devices: list[Device]
) -> None:
    """Write the alive hosts of a scan, with what was probed, as versioned JSON."""
    document = {
        "format": SNAPSHOT_FORMAT,
        "version": SNAPSHOT_VERSION,
        "netprobe_version": package_version("netprobe"),
        "created": datetime.now(UTC).isoformat(timespec="seconds"),
        "target": network,
        "services": [
            {"name": s.name, "port": s.port, "protocol": s.protocol, "probe": s.probe}
            for s in services
        ],
        # Down hosts carry no information worth diffing and would make a /16
        # snapshot 65k entries long.
        "devices": [asdict(d) for d in devices if d.alive],
    }
    path.write_text(json.dumps(document, indent=2) + "\n")


@dataclass
class Host:
    ip: str
    hostname: str
    # (port, protocol) -> (service name, version)
    open: dict[Port, tuple[str, str]]


@dataclass
class Inventory:
    label: str
    created: str
    target: str
    # None for plain reports, which do not record what was probed.
    probed: set[Port] | None
    hosts: dict[str, Host]


def _host(entry: Any) -> Host:
    if not isinstance(entry, dict) or not isinstance(entry.get("ip"), str):
        raise SnapshotError("device entry without an ip")
    found: dict[Port, tuple[str, str]] = {}
    services = entry.get("services")
    if isinstance(services, list):
        for s in services:
            if isinstance(s, dict) and s.get("state") == "open":
                found[(int(s["port"]), str(s["protocol"]))] = (
                    str(s["name"]),
                    str(s.get("version", "")),
                )
    else:
        for name, port in LEGACY_PORTS.items():
            if entry.get(name) is True:
                found[port] = (name, "")
    return Host(entry["ip"], str(entry.get("hostname", "")), found)


def load_inventory(path: Path) -> Inventory:
    """Read a snapshot, or a plain `scan -o file.json` report."""
    try:
        document = json.loads(path.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        raise SnapshotError(f"cannot read {path}: {e}") from e

    try:
        if isinstance(document, list):
            devices, probed, created, target = document, None, "", ""
        elif isinstance(document, dict) and document.get("format") == SNAPSHOT_FORMAT:
            if document.get("version") != SNAPSHOT_VERSION:
                raise SnapshotError(
                    f"{path}: snapshot version {document.get('version')!r} is not supported "
                    f"(this netprobe reads version {SNAPSHOT_VERSION})"
                )
            devices = document["devices"]
            probed = {(int(s["port"]), str(s["protocol"])) for s in document["services"]}
            created, target = str(document.get("created", "")), str(document.get("target", ""))
        else:
            raise SnapshotError(f"{path}: not a netprobe snapshot or JSON report")
        hosts = [_host(d) for d in devices if not isinstance(d, dict) or d.get("alive", True)]
    except SnapshotError:
        raise
    except (KeyError, TypeError, ValueError) as e:
        raise SnapshotError(f"{path}: malformed snapshot: {e}") from e
    return Inventory(str(path), created, target, probed, {h.ip: h for h in hosts})


@dataclass
class Change:
    ip: str
    name: str
    port: int
    protocol: str
    version: str = ""
    old_version: str = ""


@dataclass
class Diff:
    old: dict[str, str]
    new: dict[str, str]
    new_hosts: list[dict[str, Any]] = field(default_factory=list)
    vanished_hosts: list[dict[str, Any]] = field(default_factory=list)
    opened: list[Change] = field(default_factory=list)
    closed: list[Change] = field(default_factory=list)
    version_changes: list[Change] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        return bool(
            self.new_hosts
            or self.vanished_hosts
            or self.opened
            or self.closed
            or self.version_changes
        )

    def to_dict(self) -> dict[str, Any]:
        return {"changed": self.changed, **asdict(self)}


def _ip_key(ip: str) -> tuple[int, int, str]:
    """IPv4 numerically, then IPv6, then hostnames alphabetically."""
    try:
        address = ipaddress.ip_address(ip)
    except ValueError:
        return (99, 0, ip)
    return (address.version, int(address), "")


def _summary(host: Host) -> dict[str, Any]:
    return {
        "ip": host.ip,
        "hostname": host.hostname,
        "services": [
            {"name": name, "port": port, "protocol": proto, "version": version}
            for (port, proto), (name, version) in sorted(host.open.items())
        ],
    }


def compare(old: Inventory, new: Inventory) -> Diff:
    """Hosts that appeared or vanished, ports that opened or closed, versions that changed.

    Ports probed in only one of the two scans are left out, so changing the
    service list between runs does not look like ports closing.
    """
    diff = Diff(
        old={"source": old.label, "created": old.created, "target": old.target},
        new={"source": new.label, "created": new.created, "target": new.target},
    )
    if old.target and new.target and old.target != new.target:
        diff.warnings.append(f"targets differ: {old.target} vs {new.target}")
    comparable: set[Port] | None = None
    if old.probed is not None and new.probed is not None:
        comparable = old.probed & new.probed
        skipped = sorted(old.probed ^ new.probed)
        if skipped:
            diff.warnings.append(
                "ports probed in only one scan are not compared: "
                + ", ".join(f"{p}/{proto}" for p, proto in skipped)
            )

    for ip in sorted(new.hosts.keys() - old.hosts.keys(), key=_ip_key):
        diff.new_hosts.append(_summary(new.hosts[ip]))
    for ip in sorted(old.hosts.keys() - new.hosts.keys(), key=_ip_key):
        diff.vanished_hosts.append(_summary(old.hosts[ip]))

    for ip in sorted(old.hosts.keys() & new.hosts.keys(), key=_ip_key):
        before, after = old.hosts[ip].open, new.hosts[ip].open
        for port in sorted(before.keys() | after.keys()):
            if comparable is not None and port not in comparable:
                continue
            if port not in before:
                name, version = after[port]
                diff.opened.append(Change(ip, name, port[0], port[1], version))
            elif port not in after:
                name, version = before[port]
                diff.closed.append(Change(ip, name, port[0], port[1], "", version))
            elif before[port][1] != after[port][1]:
                name = after[port][0]
                diff.version_changes.append(
                    Change(ip, name, port[0], port[1], after[port][1], before[port][1])
                )
    return diff


def print_diff(diff: Diff, console: Console) -> None:
    for warning in diff.warnings:
        console.print(f"[yellow]Warning:[/yellow] {escape(warning)}")
    if not diff.changed:
        console.print("[green]No changes[/green]")
        return

    table = Table(title="Inventory changes")
    table.add_column("Change")
    table.add_column("Host", style="cyan")
    table.add_column("Service")
    table.add_column("Detail")

    def services(entry: dict[str, Any]) -> str:
        return ", ".join(f"{s['name']}:{s['port']}/{s['protocol']}" for s in entry["services"])

    for entry in diff.new_hosts:
        table.add_row(
            "[green]new host[/green]",
            entry["ip"],
            escape(services(entry)),
            escape(entry["hostname"]),
        )
    for entry in diff.vanished_hosts:
        table.add_row(
            "[red]vanished host[/red]",
            entry["ip"],
            escape(services(entry)),
            escape(entry["hostname"]),
        )
    for c in diff.opened:
        table.add_row(
            "[green]opened[/green]",
            c.ip,
            f"{escape(c.name)}:{c.port}/{c.protocol}",
            escape(c.version),
        )
    for c in diff.closed:
        table.add_row(
            "[red]closed[/red]",
            c.ip,
            f"{escape(c.name)}:{c.port}/{c.protocol}",
            escape(c.old_version),
        )
    for c in diff.version_changes:
        table.add_row(
            "[yellow]version[/yellow]",
            c.ip,
            f"{escape(c.name)}:{c.port}/{c.protocol}",
            escape(f"{c.old_version or '-'} -> {c.version or '-'}"),
        )
    console.print(table)
