# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Versioned scan snapshots and the comparison between two of them."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.markup import escape
from rich.table import Table

from netprobe.models import Device, ServiceSpec
from netprobe.output import write_text
from netprobe.scan_settings import (
    NETPROBE_VERSION,
    RecordedSettings,
    effective_timeouts,
    host_sort_key,
    setting_warnings,
)

SNAPSHOT_FORMAT = "netprobe-snapshot"
SNAPSHOT_VERSION = 1

# Ports a pre-2.1 report could only express as booleans.
LEGACY_PORTS = {"ssh": (22, "tcp"), "snmp": (161, "udp"), "mysql": (3306, "tcp")}

Port = tuple[int, str]
# port, protocol, service name. The name keeps two open services on one socket apart.
OpenKey = tuple[int, str, str]


class SnapshotError(ValueError):
    """A file is not a snapshot or report this version can read."""


def write_snapshot(
    path: Path,
    network: str,
    services: tuple[ServiceSpec, ...],
    devices: list[Device],
    *,
    timeout: float | None = None,
    backend: str | None = None,
) -> None:
    """Write the alive hosts of a scan, with what was probed, as versioned JSON.

    Hosts that gave no answer but had a probe fail are kept too, so a later
    diff does not mistake a failed observation for a vanished host.
    """
    document: dict[str, Any] = {
        "format": SNAPSHOT_FORMAT,
        "version": SNAPSHOT_VERSION,
        "netprobe_version": NETPROBE_VERSION,
        "created": datetime.now(UTC).isoformat(timespec="seconds"),
        "target": network,
        "services": [
            {
                "name": s.name,
                "port": s.port,
                "protocol": s.protocol,
                "probe": s.probe,
                "timeout": s.timeout,
            }
            for s in services
        ],
    }
    if timeout is not None:
        document["timeout"] = timeout
    if backend is not None:
        document["backend"] = backend
    # Down hosts carry no information worth diffing and would make a /16
    # snapshot 65k entries long.
    document["devices"] = [asdict(d) for d in devices if d.alive or _uncertain(d)]
    write_text(path, json.dumps(document, indent=2) + "\n")


@dataclass
class Host:
    ip: str
    hostname: str
    # (port, protocol, name) -> version
    open: dict[OpenKey, str]
    # Ports whose probe failed or timed out, with the service name; their
    # state is not known either way.
    unknown: dict[Port, str] = field(default_factory=dict)


@dataclass
class Inventory:
    label: str
    created: str
    target: str
    # None for plain reports, which do not record what was probed.
    probed: set[Port] | None
    hosts: dict[str, Host]
    # The alive device entries as stored, for consumers such as the exporter.
    devices: list[dict[str, Any]] = field(default_factory=list)
    # Hosts that did not answer but had probes fail: neither up nor gone.
    uncertain: set[str] = field(default_factory=set)
    # None when the file did not record the setting (older snapshots, plain reports).
    timeout: float | None = None
    backend: str | None = None
    service_timeouts: dict[str, float] = field(default_factory=dict)

    @property
    def settings(self) -> RecordedSettings:
        return RecordedSettings(self.target, self.timeout, self.backend, self.service_timeouts)


def _uncertain(device: Device) -> bool:
    return any(s.state == "unknown" for s in device.services)


def _endpoint(service: dict[str, Any]) -> Port:
    """A stored service's (port, protocol), rejecting values no scan produces."""
    port, protocol = service["port"], service["protocol"]
    if type(port) is not int or not 1 <= port <= 65535 or protocol not in ("tcp", "udp"):
        raise ValueError(f"invalid service endpoint {port!r}/{protocol!r}")
    return port, protocol


def _host(entry: Any) -> Host:
    if not isinstance(entry, dict) or not isinstance(entry.get("ip"), str):
        raise SnapshotError("device entry without an ip")
    services = entry.get("services")
    if not isinstance(services, list):
        legacy = {
            (port, protocol, name): ""
            for name, (port, protocol) in LEGACY_PORTS.items()
            if entry.get(name) is True
        }
        return Host(entry["ip"], str(entry.get("hostname", "")), legacy)
    listed = [s for s in services if isinstance(s, dict)]
    found = {
        (*_endpoint(s), str(s["name"])): str(s.get("version", ""))
        for s in listed
        if s.get("state") == "open"
    }
    unknown = {_endpoint(s): str(s["name"]) for s in listed if s.get("state") == "unknown"}
    return Host(entry["ip"], str(entry.get("hostname", "")), found, unknown)


def _partition(devices: list[Any]) -> tuple[list[Any], list[Host], set[str]]:
    """Split stored devices into alive entries, their hosts, and uncertain IPs."""
    answered = [not isinstance(d, dict) or bool(d.get("alive", True)) for d in devices]
    alive = [d for d, up in zip(devices, answered, strict=True) if up]
    quiet = [d for d, up in zip(devices, answered, strict=True) if not up]
    uncertain = {h.ip for h in map(_host, quiet) if h.unknown}
    return alive, [_host(d) for d in alive], uncertain


def _recorded_number(document: dict[str, Any], key: str) -> float | None:
    if key not in document:
        return None
    value = document[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key} must be a number")
    return float(value)


def _recorded_settings(document: dict[str, Any]) -> tuple[float | None, str | None]:
    timeout = _recorded_number(document, "timeout")
    if "backend" not in document:
        return timeout, None
    backend = document["backend"]
    if not isinstance(backend, str):
        raise ValueError("backend must be a string")
    return timeout, backend


def _snapshot_parts(path: Path, document: dict[str, Any]) -> dict[str, Any]:
    if document.get("version") != SNAPSHOT_VERSION:
        raise SnapshotError(
            f"{path}: snapshot version {document.get('version')!r} is not supported "
            f"(this netprobe reads version {SNAPSHOT_VERSION})"
        )
    timeout, backend = _recorded_settings(document)
    return {
        "devices": document["devices"],
        "probed": {_endpoint(s) for s in document["services"]},
        "created": str(document.get("created", "")),
        "target": str(document.get("target", "")),
        "timeout": timeout,
        "backend": backend,
        "service_timeouts": effective_timeouts(document),
    }


def load_inventory(path: Path) -> Inventory:
    """Read a snapshot, or a plain `scan -o file.json` report."""
    try:
        document = json.loads(path.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        raise SnapshotError(f"cannot read {path}: {e}") from e

    try:
        if isinstance(document, list):
            parts: dict[str, Any] = {
                "devices": document,
                "probed": None,
                "created": "",
                "target": "",
            }
        elif isinstance(document, dict) and document.get("format") == SNAPSHOT_FORMAT:
            parts = _snapshot_parts(path, document)
        else:
            raise SnapshotError(f"{path}: not a netprobe snapshot or JSON report")
        alive, hosts, uncertain = _partition(parts["devices"])
    except SnapshotError:
        raise
    except (KeyError, TypeError, ValueError) as e:
        raise SnapshotError(f"{path}: malformed snapshot: {e}") from e
    return Inventory(
        str(path),
        parts["created"],
        parts["target"],
        parts["probed"],
        {h.ip: h for h in hosts},
        alive,
        timeout=parts.get("timeout"),
        backend=parts.get("backend"),
        service_timeouts=parts.get("service_timeouts", {}),
        uncertain=uncertain,
    )


@dataclass
class Change:
    ip: str
    name: str
    port: int
    protocol: str
    version: str = ""
    old_version: str = ""


@dataclass
class Unconfirmed:
    """A port whose state is "unknown" in at least one scan and is not now open."""

    ip: str
    name: str
    port: int
    protocol: str
    before: str
    after: str


@dataclass
class Diff:
    old: dict[str, str]
    new: dict[str, str]
    new_hosts: list[dict[str, Any]] = field(default_factory=list)
    vanished_hosts: list[dict[str, Any]] = field(default_factory=list)
    opened: list[Change] = field(default_factory=list)
    closed: list[Change] = field(default_factory=list)
    version_changes: list[Change] = field(default_factory=list)
    # Hosts answering in one scan whose probes all failed in the other.
    unsettled_hosts: list[dict[str, str]] = field(default_factory=list)
    # Ports that cannot be confirmed open or closed because a probe failed.
    unconfirmed: list[Unconfirmed] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        """True when anything changed or could not be confirmed unchanged.

        A failed observation must never read as "no change", so unsettled
        hosts and unconfirmed ports count, and `diff` exits 3 for them.
        """
        return bool(
            self.new_hosts
            or self.vanished_hosts
            or self.opened
            or self.closed
            or self.version_changes
            or self.unsettled_hosts
            or self.unconfirmed
        )

    def to_dict(self) -> dict[str, Any]:
        return {"changed": self.changed, **asdict(self)}


def _summary(host: Host) -> dict[str, Any]:
    return {
        "ip": host.ip,
        "hostname": host.hostname,
        "services": [
            {"name": name, "port": port, "protocol": proto, "version": version}
            for (port, proto, name), version in sorted(host.open.items())
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
    diff.warnings.extend(setting_warnings(old.settings, new.settings))
    comparable: set[Port] | None = None
    if old.probed is not None and new.probed is not None:
        comparable = old.probed & new.probed
        skipped = sorted(old.probed ^ new.probed)
        if skipped:
            diff.warnings.append(
                "ports probed in only one scan are not compared: "
                + ", ".join(f"{p}/{proto}" for p, proto in skipped)
            )

    # A host now answering is reported with its open ports even when the
    # earlier scan could not observe it; only the reverse is held back,
    # because failed probes do not show that a host went away.
    appeared = sorted(new.hosts.keys() - old.hosts.keys(), key=host_sort_key)
    diff.new_hosts.extend(_summary(new.hosts[ip]) for ip in appeared)
    diff.unsettled_hosts.extend(
        {"ip": ip, "before": "uncertain", "after": "up"} for ip in appeared if ip in old.uncertain
    )
    for ip in sorted(old.hosts.keys() - new.hosts.keys(), key=host_sort_key):
        if ip in new.uncertain:
            diff.unsettled_hosts.append({"ip": ip, "before": "up", "after": "uncertain"})
        else:
            diff.vanished_hosts.append(_summary(old.hosts[ip]))
    # Failed in both scans: nothing was observed either time, which still
    # needs attention rather than a "no changes" result.
    diff.unsettled_hosts.extend(
        {"ip": ip, "before": "uncertain", "after": "uncertain"}
        for ip in sorted(old.uncertain & new.uncertain, key=host_sort_key)
    )

    for ip in sorted(old.hosts.keys() & new.hosts.keys(), key=host_sort_key):
        compare_host_ports(diff, ip, old.hosts[ip], new.hosts[ip], comparable)

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
    for h in diff.unsettled_hosts:
        table.add_row(
            "[magenta]unsettled host[/magenta]", h["ip"], "", f"{h['before']} -> {h['after']}"
        )
    for u in diff.unconfirmed:
        table.add_row(
            "[magenta]unconfirmed[/magenta]",
            u.ip,
            f"{escape(u.name)}:{u.port}/{u.protocol}",
            f"{u.before} -> {u.after}",
        )
    console.print(table)


def _relabel(old: Host, new: Host) -> dict[OpenKey, str]:
    """Old open services keyed by the new label when the socket is unambiguous.

    A label change is not a port transition. Retain name matching only for
    older inventories that contain multiple services on the same socket.
    """
    before_counts = Counter((port, protocol) for port, protocol, _ in old.open)
    after_counts = Counter((port, protocol) for port, protocol, _ in new.open)
    unique_after = {
        (port, protocol): (port, protocol, name)
        for port, protocol, name in new.open
        if after_counts[(port, protocol)] == 1
    }
    return {
        unique_after.get((port, protocol), (port, protocol, name))
        if before_counts[(port, protocol)] == 1
        else (port, protocol, name): version
        for (port, protocol, name), version in old.open.items()
    }


def _compare_port(diff: Diff, ip: str, key: OpenKey, before: dict[OpenKey, str], new: Host) -> None:
    port, protocol, name = key
    after = new.open
    if key not in before:
        # Reported even when the earlier probe failed: an open port is news.
        diff.opened.append(Change(ip, name, port, protocol, after[key]))
    elif key in after:
        if before[key] != after[key]:
            diff.version_changes.append(Change(ip, name, port, protocol, after[key], before[key]))
    elif (port, protocol) in new.unknown:
        diff.unconfirmed.append(Unconfirmed(ip, name, port, protocol, "open", "unknown"))
    else:
        diff.closed.append(Change(ip, name, port, protocol, "", before[key]))


def compare_host_ports(
    diff: Diff, ip: str, old: Host, new: Host, comparable: set[Port] | None
) -> None:
    before = _relabel(old, new)
    for key in sorted(before.keys() | new.open.keys()):
        if comparable is None or key[:2] in comparable:
            _compare_port(diff, ip, key, before, new)
    for port, protocol in sorted(old.unknown.keys() & new.unknown.keys()):
        if comparable is None or (port, protocol) in comparable:
            name = new.unknown[(port, protocol)]
            diff.unconfirmed.append(Unconfirmed(ip, name, port, protocol, "unknown", "unknown"))
