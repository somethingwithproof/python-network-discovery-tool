# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Versioned scan snapshots and the comparison between two of them."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.markup import escape
from rich.table import Table

from netprobe.models import Device, ServiceSpec
from netprobe.output import (
    REPORT_FORMAT,
    REPORT_VERSION,
    SNAPSHOT_FORMAT,
    SNAPSHOT_VERSION,
    scan_document,
    write_text,
)
from netprobe.probes import clean
from netprobe.scan_settings import (
    UNKNOWN,
    PortTransition,
    RecordedSettings,
    effective_timeouts,
    host_sort_key,
    port_transition,
    setting_warnings,
)
from netprobe.scanner import stored_target

DIFF_FORMAT = "netprobe-diff"
DIFF_VERSION = 1
# Both carry the same envelope; a report also lists hosts that were down.
INVENTORY_FORMATS = {REPORT_FORMAT: REPORT_VERSION, SNAPSHOT_FORMAT: SNAPSHOT_VERSION}

# Ports a pre-2.1 report could only express as booleans.
LEGACY_PORTS = {"ssh": (22, "tcp"), "snmp": (161, "udp"), "mysql": (3306, "tcp")}

Port = tuple[int, str]
# A probed port that answered closed or filtered; snapshots keep only open and unknown.
NOT_OPEN = "not-open"
# (before, after) service versions of one port.
Versions = tuple[str, str]
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
    # Down hosts carry no information worth diffing and would make a /16
    # snapshot 65k entries long.
    kept = [d for d in devices if d.alive or _uncertain(d)]
    document = scan_document(
        SNAPSHOT_FORMAT, SNAPSHOT_VERSION, network, services, kept, timeout=timeout, backend=backend
    )
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
    # False for a report from a scan stopped by --deadline: hosts it never
    # reached are missing, not gone.
    complete: bool = True

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
    """One stored device, validated and cleaned: files are untrusted input.

    Every command that reads snapshots or reports goes through here, so an
    address is canonical and text holds no control characters by the time
    it reaches a terminal, a script or a comparison.
    """
    if not isinstance(entry, dict) or "ip" not in entry:
        raise SnapshotError("device entry without an ip")
    try:
        ip = stored_target(entry["ip"])
    except ValueError as e:
        raise SnapshotError(f"device entry with {e}") from e
    hostname = clean(str(entry.get("hostname", "")))
    services = entry.get("services")
    if not isinstance(services, list):
        legacy = {
            (port, protocol, name): ""
            for name, (port, protocol) in LEGACY_PORTS.items()
            if entry.get(name) is True
        }
        return Host(ip, hostname, legacy)
    listed = [s for s in services if isinstance(s, dict)]
    found = {
        (*_endpoint(s), clean(str(s["name"]))): clean(str(s.get("version", "")))
        for s in listed
        if s.get("state") == "open"
    }
    unknown = {_endpoint(s): clean(str(s["name"])) for s in listed if s.get("state") == UNKNOWN}
    return Host(ip, hostname, found, unknown)


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
    return timeout, clean(backend)


def _snapshot_parts(path: Path, document: dict[str, Any]) -> dict[str, Any]:
    supported = INVENTORY_FORMATS[document["format"]]
    if document.get("version") != supported:
        raise SnapshotError(
            f"{path}: {document['format']} version {document.get('version')!r} is not "
            f"supported (this netprobe reads version {supported})"
        )
    timeout, backend = _recorded_settings(document)
    return {
        "devices": document["devices"],
        "probed": {_endpoint(s) for s in document["services"]},
        "created": clean(str(document.get("created", ""))),
        "target": clean(str(document.get("target", ""))),
        "timeout": timeout,
        "backend": backend,
        "service_timeouts": effective_timeouts(document),
        "complete": _recorded_complete(document),
    }


def _recorded_complete(document: dict[str, Any]) -> bool:
    # Files from before --deadline do not record it; they were complete.
    complete = document.get("complete", True)
    if not isinstance(complete, bool):
        raise ValueError("complete must be a boolean")
    return complete


def load_inventory(path: Path, *, allow_partial: bool = False) -> Inventory:
    """Read a snapshot, or a plain `scan -o file.json` report.

    A report from a scan stopped by --deadline lists only the hosts it
    reached, so it is refused unless allow_partial is given.
    """
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
        elif isinstance(document, dict) and document.get("format") in INVENTORY_FORMATS:
            parts = _snapshot_parts(path, document)
        else:
            raise SnapshotError(f"{path}: not a netprobe snapshot or JSON report")
        alive, hosts, uncertain = _partition(parts["devices"])
    except SnapshotError:
        raise
    except (KeyError, TypeError, ValueError) as e:
        raise SnapshotError(f"{path}: malformed snapshot: {e}") from e
    complete = parts.get("complete", True)
    if not complete and not allow_partial:
        raise SnapshotError(
            f"{path}: the scan stopped before every host was reached (complete: false); "
            "pass --allow-partial to use it anyway"
        )
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
        complete=complete,
    )


UP, UNCERTAIN, ABSENT, UNSCANNED = "up", "uncertain", "absent", "unscanned"
# States in which a host was not observed: never a vanished host or "no change".
UNOBSERVED = frozenset({UNCERTAIN, UNSCANNED})


def _host_state(inventory: Inventory, ip: str) -> str:
    """Whether a scan saw ip answer, saw only failed probes, or did not list it."""
    if ip in inventory.hosts:
        return UP
    if ip in inventory.uncertain:
        return UNCERTAIN
    # An incomplete scan may simply not have reached the host.
    return ABSENT if inventory.complete else UNSCANNED


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
    """A port whose state is "unknown" in at least one scan and is not now open.

    before is open, unknown or not-open; after is unknown or not-open.
    """

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
    # Hosts whose probes all failed in at least one scan: before and after
    # are up, uncertain or absent.
    unsettled_hosts: list[dict[str, str]] = field(default_factory=list)
    # Ports that cannot be confirmed open or closed because a probe failed.
    unconfirmed: list[Unconfirmed] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    # A side was an incomplete scan, so hosts it never reached are unknown.
    partial: bool = False

    @property
    def changed(self) -> bool:
        """True when anything changed or could not be confirmed unchanged.

        A failed observation must never read as "no change", so unsettled
        hosts, unconfirmed ports and an incomplete scan count, and `diff`
        exits 3 for them.
        """
        return bool(
            self.partial
            or self.new_hosts
            or self.vanished_hosts
            or self.opened
            or self.closed
            or self.version_changes
            or self.unsettled_hosts
            or self.unconfirmed
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": DIFF_FORMAT,
            "version": DIFF_VERSION,
            "changed": self.changed,
            **asdict(self),
        }


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
    for side in (old, new):
        if not side.complete:
            diff.partial = True
            diff.warnings.append(
                f"{side.label} is an incomplete scan; hosts it did not reach are unscanned"
            )
    comparable: set[Port] | None = None
    if old.probed is not None and new.probed is not None:
        comparable = old.probed & new.probed
        skipped = sorted(old.probed ^ new.probed)
        if skipped:
            diff.warnings.append(
                "ports probed in only one scan are not compared: "
                + ", ".join(f"{p}/{proto}" for p, proto in skipped)
            )

    for ip in sorted(
        old.hosts.keys() | new.hosts.keys() | old.uncertain | new.uncertain, key=host_sort_key
    ):
        compare_host(diff, ip, old, new, comparable)
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
            escape(entry["ip"]),
            escape(services(entry)),
            escape(entry["hostname"]),
        )
    for entry in diff.vanished_hosts:
        table.add_row(
            "[red]vanished host[/red]",
            escape(entry["ip"]),
            escape(services(entry)),
            escape(entry["hostname"]),
        )
    for c in diff.opened:
        table.add_row(
            "[green]opened[/green]",
            escape(c.ip),
            f"{escape(c.name)}:{c.port}/{c.protocol}",
            escape(c.version),
        )
    for c in diff.closed:
        table.add_row(
            "[red]closed[/red]",
            escape(c.ip),
            f"{escape(c.name)}:{c.port}/{c.protocol}",
            escape(c.old_version),
        )
    for c in diff.version_changes:
        table.add_row(
            "[yellow]version[/yellow]",
            escape(c.ip),
            f"{escape(c.name)}:{c.port}/{c.protocol}",
            escape(f"{c.old_version or '-'} -> {c.version or '-'}"),
        )
    for h in diff.unsettled_hosts:
        table.add_row(
            "[magenta]unsettled host[/magenta]",
            escape(h["ip"]),
            "",
            escape(f"{h['before']} -> {h['after']}"),
        )
    for u in diff.unconfirmed:
        table.add_row(
            "[magenta]unconfirmed[/magenta]",
            escape(u.ip),
            f"{escape(u.name)}:{u.port}/{u.protocol}",
            escape(f"{u.before} -> {u.after}"),
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


def compare_host(
    diff: Diff, ip: str, old: Inventory, new: Inventory, comparable: set[Port] | None
) -> None:
    """Classify one host present in either scan.

    A host answering now is reported with its open ports even when the
    earlier scan could not observe it. A failed observation on either side
    is unsettled, never a vanished host or "no change".
    """
    before, after = _host_state(old, ip), _host_state(new, ip)
    if before == after == UP:
        compare_host_ports(diff, ip, old.hosts[ip], new.hosts[ip], comparable)
        return
    if after == UP:
        diff.new_hosts.append(_summary(new.hosts[ip]))
    elif before == UP and after == ABSENT:
        diff.vanished_hosts.append(_summary(old.hosts[ip]))
    if UNOBSERVED & {before, after}:
        diff.unsettled_hosts.append({"ip": ip, "before": before, "after": after})


def _state(host: Host, key: OpenKey, open_ports: dict[OpenKey, str]) -> str:
    """A port's state in one scan: open, unknown, or not open (closed or filtered)."""
    if key in open_ports:
        return "open"
    return UNKNOWN if key[:2] in host.unknown else NOT_OPEN


def _record(diff: Diff, ip: str, key: OpenKey, states: tuple[str, str], versions: Versions) -> None:
    """File one port's transition under the list port_transition assigns it."""
    port, protocol, name = key
    before, after = states
    old_version, version = versions
    match port_transition(before, after):
        case PortTransition.OPENED:
            diff.opened.append(Change(ip, name, port, protocol, version))
        case PortTransition.CLOSED:
            diff.closed.append(Change(ip, name, port, protocol, "", old_version))
        case PortTransition.UNCONFIRMED:
            diff.unconfirmed.append(Unconfirmed(ip, name, port, protocol, before, after))
        case PortTransition.UNCHANGED if before == "open" and old_version != version:
            diff.version_changes.append(Change(ip, name, port, protocol, version, old_version))


def compare_host_ports(
    diff: Diff, ip: str, old: Host, new: Host, comparable: set[Port] | None
) -> None:
    """Compare the ports of a host up in both scans.

    Every comparable port open in either scan is classified, then every
    port whose probe failed in either scan and that is open in neither.
    """
    before = _relabel(old, new)
    seen: set[Port] = set()
    for key in sorted(before.keys() | new.open.keys()):
        seen.add(key[:2])
        if comparable is None or key[:2] in comparable:
            states = (_state(old, key, before), _state(new, key, new.open))
            _record(diff, ip, key, states, (before.get(key, ""), new.open.get(key, "")))
    for port, protocol in sorted((old.unknown.keys() | new.unknown.keys()) - seen):
        if comparable is None or (port, protocol) in comparable:
            name = new.unknown.get((port, protocol)) or old.unknown[(port, protocol)]
            key = (port, protocol, name)
            states = (_state(old, key, {}), _state(new, key, {}))
            _record(diff, ip, key, states, ("", ""))
