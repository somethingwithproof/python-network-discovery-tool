"""Report writers and the terminal table."""

from __future__ import annotations

import csv
import json
import logging
from collections import Counter
from dataclasses import asdict
from pathlib import Path

from rich.console import Console
from rich.table import Table

from netprobe.models import LEGACY_FLAGS, Device

logger = logging.getLogger(__name__)
console = Console()

# New columns go at the end so positional CSV readers keep working.
CSV_FIELDS = ["ip", "alive", "ssh", "snmp", "mysql", "hostname", "errors", "services"]


def save_json(devices: list[Device], output_path: Path) -> None:
    """Save devices to JSON file."""
    data = [asdict(d) for d in devices]
    output_path.write_text(json.dumps(data, indent=2))
    logger.info(f"Saved JSON report to {output_path}")


def save_csv(devices: list[Device], output_path: Path) -> None:
    """Save devices to CSV file."""
    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for device in devices:
            row = asdict(device)
            row["errors"] = "; ".join(row["errors"]) if row["errors"] else ""
            row["services"] = "; ".join(
                f"{s.name}:{s.port}/{s.protocol}" for s in device.open_services
            )
            writer.writerow(row)
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
    table.add_column("Other open")
    table.add_column("Status")

    for device in alive_devices:
        others = [f"{s.name}:{s.port}" for s in device.open_services if s.name not in LEGACY_FLAGS]
        table.add_row(
            device.ip,
            device.hostname or "-",
            "✅" if device.ssh else "❌",
            "✅" if device.snmp else "❌",
            "✅" if device.mysql else "❌",
            ", ".join(others) or "-",
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
