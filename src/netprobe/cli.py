"""Typer command-line interface."""

from __future__ import annotations

import asyncio
import logging
from importlib.metadata import version as package_version
from pathlib import Path
from typing import Literal

import typer
from rich import print as rprint
from rich.logging import RichHandler
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn

from netprobe.output import console, print_results, save_csv, save_json
from netprobe.scanner import (
    DEFAULT_CONCURRENCY,
    DEFAULT_TIMEOUT,
    BackendUnavailableError,
    NetworkScanner,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
)
logger = logging.getLogger(__name__)

# Typer app for modern CLI
app = typer.Typer(
    name="netprobe",
    help="🔍 Modern network scanner for SSH/SNMP/MySQL discovery",
    add_completion=False,
)


@app.command()
def scan(
    network: str = typer.Argument(..., help="Network CIDR (e.g., 192.168.1.0/24) or single IP"),
    output: Path = typer.Option(
        None, "--output", "-o", help="Output file (JSON or CSV, detected by extension)"
    ),
    format: Literal["json", "csv", "auto"] = typer.Option(
        "auto", "--format", "-f", help="Output format (auto-detects from filename)"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress table output"),
    backend: Literal["asyncio", "nmap"] = typer.Option(
        "asyncio",
        "--backend",
        help="Host discovery: asyncio probes only, or an nmap ping sweep first",
    ),
    timeout: float = typer.Option(
        DEFAULT_TIMEOUT, "--timeout", min=0.05, help="Seconds to wait for each probe"
    ),
    concurrency: int = typer.Option(
        DEFAULT_CONCURRENCY, "--concurrency", min=1, help="Maximum probes in flight"
    ),
) -> None:
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

    try:
        scanner = NetworkScanner(backend=backend, timeout=timeout, concurrency=concurrency)
    except BackendUnavailableError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1) from e

    if format != "auto" and output is None:
        logger.warning("--format has no effect without --output")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        try:
            devices = asyncio.run(scanner.scan_network(network, progress))
        except ValueError as e:
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(2) from e

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

        try:
            match format:
                case "json":
                    save_json(devices, output)
                case "csv":
                    save_csv(devices, output)
        except OSError as e:
            typer.echo(f"Error: cannot write {output}: {e}", err=True)
            raise typer.Exit(1) from e


@app.command()
def version() -> None:
    """Show version information."""
    rprint(f"[bold cyan]netprobe[/bold cyan] [green]v{package_version('netprobe')}[/green]")
    rprint("Modern network scanner built with Python 3.12+")
