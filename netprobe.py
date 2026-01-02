#!/usr/bin/env python3
"""Modern Network Scanner - 2026 Edition

A clean, fast network discovery tool for identifying SSH, SNMP, and MySQL services.
Built with modern Python practices and beautiful terminal output.
"""

from __future__ import annotations

import asyncio
import csv
import ipaddress
import json
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Literal

import nmap
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich import print as rprint
import typer

# Modern logger with Rich
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)]
)
logger = logging.getLogger(__name__)
console = Console()

# Typer app for modern CLI
app = typer.Typer(
    name="netprobe",
    help="🔍 Modern network scanner for SSH/SNMP/MySQL discovery",
    add_completion=False,
)


@dataclass
class Device:
    """Network device with scan results."""
    ip: str
    alive: bool = False
    ssh: bool = False
    snmp: bool = False
    mysql: bool = False
    hostname: str = ""
    errors: list[str] | None = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class NetworkScanner:
    """Fast async network scanner using nmap."""

    def __init__(self):
        self.nm = nmap.PortScanner()

    async def scan_device(self, ip: str) -> Device:
        """Scan a single device for services.

        Args:
            ip: IP address to scan

        Returns:
            Device object with scan results
        """
        device = Device(ip=ip)

        try:
            # Check if host is alive (faster than port scan)
            alive = await asyncio.to_thread(self._check_alive, ip)
            device.alive = alive

            if not alive:
                device.errors.append("Host is down")
                return device

            # Scan common ports concurrently
            ports_to_check = {
                22: "ssh",
                161: "snmp",
                3306: "mysql",
            }

            # Run port scans concurrently
            port_results = await asyncio.gather(
                *[self._check_port(ip, port) for port in ports_to_check.keys()],
                return_exceptions=True
            )

            # Update device with results
            for port, result in zip(ports_to_check.keys(), port_results):
                if isinstance(result, Exception):
                    device.errors.append(f"Error checking port {port}: {result}")
                else:
                    setattr(device, ports_to_check[port], result)

            # Try to get hostname
            try:
                device.hostname = await asyncio.to_thread(self._get_hostname, ip)
            except Exception as e:
                logger.debug(f"Could not resolve hostname for {ip}: {e}")

        except Exception as e:
            device.errors.append(f"Scan error: {e}")
            logger.error(f"Error scanning {ip}: {e}")

        return device

    def _check_alive(self, ip: str) -> bool:
        """Check if host is alive using nmap ping scan."""
        try:
            self.nm.scan(hosts=ip, arguments="-sn -T4")
            return ip in self.nm.all_hosts() and self.nm[ip].state() == "up"
        except Exception:
            return False

    async def _check_port(self, ip: str, port: int) -> bool:
        """Check if a specific port is open."""
        try:
            result = await asyncio.to_thread(
                self.nm.scan,
                hosts=ip,
                arguments=f"-p {port} -T4 --open"
            )

            if ip not in self.nm.all_hosts():
                return False

            tcp_ports = self.nm[ip].get("tcp", {})
            port_info = tcp_ports.get(port, {})
            return port_info.get("state") == "open"

        except Exception as e:
            logger.debug(f"Error checking port {port} on {ip}: {e}")
            return False

    def _get_hostname(self, ip: str) -> str:
        """Get hostname for IP address."""
        try:
            import socket
            return socket.gethostbyaddr(ip)[0]
        except Exception:
            return ""

    async def scan_network(self, network: str, progress: Progress | None = None) -> list[Device]:
        """Scan an entire network.

        Args:
            network: Network in CIDR notation (e.g., "192.168.1.0/24") or single IP
            progress: Optional Rich progress bar

        Returns:
            List of scanned devices
        """
        # Parse network
        try:
            if "/" in network:
                net = ipaddress.ip_network(network, strict=False)
                ips = [str(ip) for ip in net.hosts()]
            else:
                ips = [network]
        except ValueError as e:
            raise ValueError(f"Invalid network format: {e}")

        logger.info(f"Scanning {len(ips)} hosts...")

        # Create progress task if progress bar provided
        task = progress.add_task("[cyan]Scanning network...", total=len(ips)) if progress else None

        # Scan all IPs concurrently with semaphore to limit concurrency
        semaphore = asyncio.Semaphore(50)  # Max 50 concurrent scans

        async def scan_with_progress(ip: str) -> Device:
            async with semaphore:
                result = await self.scan_device(ip)
                if progress and task is not None:
                    progress.update(task, advance=1)
                return result

        devices = await asyncio.gather(*[scan_with_progress(ip) for ip in ips])

        return devices


def save_json(devices: list[Device], output_path: Path) -> None:
    """Save devices to JSON file."""
    data = [asdict(d) for d in devices]
    output_path.write_text(json.dumps(data, indent=2))
    logger.info(f"Saved JSON report to {output_path}")


def save_csv(devices: list[Device], output_path: Path) -> None:
    """Save devices to CSV file."""
    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["ip", "alive", "ssh", "snmp", "mysql", "hostname", "errors"]
        )
        writer.writeheader()
        for device in devices:
            row = asdict(device)
            row["errors"] = "; ".join(row["errors"]) if row["errors"] else ""
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
    table.add_column("Status")

    for device in alive_devices:
        table.add_row(
            device.ip,
            device.hostname or "-",
            "✅" if device.ssh else "❌",
            "✅" if device.snmp else "❌",
            "✅" if device.mysql else "❌",
            "[green]UP[/green]" if device.alive else "[red]DOWN[/red]"
        )

    console.print(table)

    # Summary
    ssh_count = sum(1 for d in alive_devices if d.ssh)
    snmp_count = sum(1 for d in alive_devices if d.snmp)
    mysql_count = sum(1 for d in alive_devices if d.mysql)

    console.print()
    console.print(f"[bold]Summary:[/bold]")
    console.print(f"  • SSH servers: {ssh_count}")
    console.print(f"  • SNMP devices: {snmp_count}")
    console.print(f"  • MySQL servers: {mysql_count}")


@app.command()
def scan(
    network: str = typer.Argument(..., help="Network CIDR (e.g., 192.168.1.0/24) or single IP"),
    output: Path = typer.Option(
        None,
        "--output", "-o",
        help="Output file (JSON or CSV, detected by extension)"
    ),
    format: Literal["json", "csv", "auto"] = typer.Option(
        "auto",
        "--format", "-f",
        help="Output format (auto-detects from filename)"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Enable verbose logging"
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet", "-q",
        help="Suppress table output"
    ),
):
    """
    🔍 Scan network for SSH, SNMP, and MySQL services.

    Examples:

        # Scan entire network
        netprobe scan 192.168.1.0/24

        # Scan single host with JSON output
        netprobe scan 192.168.1.1 -o results.json

        # Scan and save to CSV
        netprobe scan 10.0.0.0/24 --output report.csv

        # Quiet mode (no table, only file output)
        netprobe scan 192.168.1.0/24 -o results.json --quiet
    """
    # Set logging level
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Run scan
    scanner = NetworkScanner()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        devices = asyncio.run(scanner.scan_network(network, progress))

    # Print results (unless quiet)
    if not quiet:
        print_results(devices)

    # Save to file if requested
    if output:
        # Auto-detect format from extension
        if format == "auto":
            ext = output.suffix.lower()
            if ext == ".json":
                format = "json"
            elif ext == ".csv":
                format = "csv"
            else:
                logger.warning(f"Unknown extension {ext}, defaulting to JSON")
                format = "json"

        # Save based on format
        match format:
            case "json":
                save_json(devices, output)
            case "csv":
                save_csv(devices, output)


@app.command()
def version():
    """Show version information."""
    rprint("[bold cyan]netprobe[/bold cyan] [green]v2.0.0[/green]")
    rprint("Modern network scanner built with Python 3.12+")


if __name__ == "__main__":
    app()
