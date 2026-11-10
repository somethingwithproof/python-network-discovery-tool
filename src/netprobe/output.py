# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

"""Report writers and the terminal table."""

from __future__ import annotations

import csv
import errno
import io
import json
import logging
import os
from collections import Counter
from collections.abc import Iterable
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.markup import escape
from rich.table import Table

from netprobe.models import LEGACY_FLAGS, Device, ServiceSpec
from netprobe.scan_settings import NETPROBE_VERSION

logger = logging.getLogger(__name__)
console = Console()

# A cell that starts with one of these is a formula in Excel and LibreOffice.
_FORMULA_PREFIX = ("=", "+", "-", "@", "\t", "\r")

# New columns go at the end so positional CSV readers keep working.
CSV_FIELDS = [
    "ip",
    "alive",
    "ssh",
    "snmp",
    "mysql",
    "hostname",
    "errors",
    "services",
    "versions",
]


def write_text(path: Path, text: str, *, private: bool = False) -> None:
    """Write text to path. The final component must not be a symbolic link.

    ``private`` forces mode 0600 on the opened descriptor, including when the
    file already existed and ``O_CREAT``'s mode was ignored.
    """
    no_follow = getattr(os, "O_NOFOLLOW", 0)
    if not no_follow:
        raise OSError(errno.ENOTSUP, "Safe output requires no-follow file opens on this platform")
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_CLOEXEC", 0) | no_follow
    try:
        # O_NONBLOCK makes opening a FIFO without a reader fail with ENXIO
        # instead of hanging the scan's final step forever.
        descriptor = os.open(path, flags | os.O_NONBLOCK, 0o600)
    except OSError as exc:
        if exc.errno == errno.ELOOP:
            raise OSError(errno.ELOOP, f"Destination must not be a symbolic link: {path}") from exc
        if exc.errno == errno.ENXIO:
            raise OSError(errno.ENXIO, f"Destination is a pipe with no reader: {path}") from exc
        raise
    owned = True
    try:
        os.set_blocking(descriptor, True)
        if private:
            os.fchmod(descriptor, 0o600)
        handle = os.fdopen(descriptor, "w", encoding="utf-8")
        owned = False
        with handle:
            handle.write(text)
    finally:
        if owned:
            os.close(descriptor)


def _csv_field(value: object) -> object:
    if isinstance(value, str) and value.startswith(_FORMULA_PREFIX):
        return "'" + value
    return value


# `scan -o report.json` and `--format json` on stdout. Every device scanned.
REPORT_FORMAT = "netprobe-report"
REPORT_VERSION = 1
# `--save-snapshot`. Only hosts that answered or had a probe fail.
SNAPSHOT_FORMAT = "netprobe-snapshot"
SNAPSHOT_VERSION = 1


def scan_document(
    format_name: str,
    version: int,
    network: str,
    services: Iterable[ServiceSpec],
    devices: Iterable[Device],
    *,
    timeout: float | None = None,
    backend: str | None = None,
    complete: bool = True,
) -> dict[str, Any]:
    """The versioned JSON envelope shared by reports and snapshots.

    The schemas in netprobe/schemas describe it; a change that removes or
    renames a field needs a new version.
    """
    document: dict[str, Any] = {
        "format": format_name,
        "version": version,
        "netprobe_version": NETPROBE_VERSION,
        "created": datetime.now(UTC).isoformat(timespec="seconds"),
        "target": network,
        # False when the scan stopped at its deadline: devices then lists only
        # the hosts that finished.
        "complete": complete,
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
    document["devices"] = [asdict(d) for d in devices]
    return document


def report_json(
    devices: list[Device],
    *,
    network: str = "",
    services: Iterable[ServiceSpec] = (),
    timeout: float | None = None,
    backend: str | None = None,
    complete: bool = True,
) -> str:
    document = scan_document(
        REPORT_FORMAT,
        REPORT_VERSION,
        network,
        services,
        devices,
        timeout=timeout,
        backend=backend,
        complete=complete,
    )
    return json.dumps(document, indent=2) + "\n"


def save_json(
    devices: list[Device],
    output_path: Path,
    *,
    network: str = "",
    services: Iterable[ServiceSpec] = (),
    timeout: float | None = None,
    backend: str | None = None,
    complete: bool = True,
) -> None:
    """Save a versioned JSON report of every scanned device."""
    text = report_json(
        devices,
        network=network,
        services=services,
        timeout=timeout,
        backend=backend,
        complete=complete,
    )
    write_text(output_path, text)
    logger.info(f"Saved JSON report to {output_path}")


def save_csv(devices: list[Device], output_path: Path) -> None:
    """Save devices to CSV file."""
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=CSV_FIELDS)
    writer.writeheader()
    for device in devices:
        row = asdict(device)
        row["errors"] = "; ".join(row["errors"]) if row["errors"] else ""
        row["services"] = "; ".join(f"{s.name}:{s.port}/{s.protocol}" for s in device.open_services)
        row["versions"] = "; ".join(
            f"{s.name}={s.version}" for s in device.open_services if s.version
        )
        writer.writerow({key: _csv_field(row[key]) for key in CSV_FIELDS})
    write_text(output_path, buffer.getvalue())
    logger.info(f"Saved CSV report to {output_path}")


def print_results(devices: list[Device]) -> None:
    """Print scan results in a beautiful table."""
    # Filter to only show alive devices by default
    alive_devices = [d for d in devices if d.alive]

    if not alive_devices:
        console.print("[yellow]No alive hosts found[/yellow]")
        return

    table = Table(title=f"🔍 Network Scan Results ({len(alive_devices)} alive hosts)")

    table.add_column("IP Address", style="cyan", no_wrap=True)
    table.add_column("Hostname", style="blue")
    table.add_column("SSH", justify="center")
    table.add_column("SNMP", justify="center")
    table.add_column("MySQL", justify="center")
    table.add_column("Open services")
    table.add_column("Status")

    for device in alive_devices:
        # Hostnames and banners come from the network; escape them so Rich
        # does not interpret "[...]" in them as markup.
        notes = [f"{s.name}:{s.port} {s.version}".rstrip() for s in device.open_services]
        table.add_row(
            device.ip,
            escape(device.hostname) or "-",
            "✅" if device.ssh else "❌",
            "✅" if device.snmp else "❌",
            "✅" if device.mysql else "❌",
            escape("\n".join(notes)) or "-",
            "[green]UP[/green]" if device.alive else "[red]DOWN[/red]",
        )

    console.print(table)

    # Summary
    ssh_count = sum(1 for d in alive_devices if d.ssh)
    snmp_count = sum(1 for d in alive_devices if d.snmp)
    mysql_count = sum(1 for d in alive_devices if d.mysql)

    console.print()
    console.print("[bold]Summary:[/bold]")
    console.print(f"  • SSH servers: {ssh_count}")
    console.print(f"  • SNMP devices: {snmp_count}")
    console.print(f"  • MySQL servers: {mysql_count}")
    other_counts = Counter(
        s.name for d in alive_devices for s in d.open_services if s.name not in LEGACY_FLAGS
    )
    for name, count in sorted(other_counts.items()):
        console.print(f"  • {name}: {count}")
