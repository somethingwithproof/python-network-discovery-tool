"""Typer command-line interface."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sqlite3
from dataclasses import asdict
from importlib.metadata import version as package_version
from pathlib import Path
from typing import Literal

import typer
from rich import print as rprint
from rich.logging import RichHandler
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn

from netprobe.config import DEFAULT_SERVICES, ConfigError, load_services, select_services
from netprobe.diff import SnapshotError, compare, load_inventory, print_diff, write_snapshot
from netprobe.export import ExportError, KadupulOptions, kadupul_script, write_script
from netprobe.history import HistoryStore, compare_scans, utc_now
from netprobe.output import console, print_results, save_csv, save_json
from netprobe.preflight import check_plan, paths_overlap
from netprobe.probes import SnmpCredentials
from netprobe.profiles import load_profiles, resolve_profile
from netprobe.scanner import (
    DEFAULT_CONCURRENCY,
    DEFAULT_TIMEOUT,
    MAX_CONCURRENCY,
    MAX_HOSTS,
    BackendUnavailableError,
    NetworkScanner,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False)],
)
logger = logging.getLogger(__name__)

# Mirrors probes.AUTH_PROTOCOLS / PRIV_PROTOCOLS; Typer needs the literal types.
AuthProtocol = Literal["MD5", "SHA", "SHA224", "SHA256", "SHA384", "SHA512"]
PrivProtocol = Literal["DES", "AES", "AES128", "AES192", "AES192C", "AES256", "AES256C"]

# Typer app for modern CLI
app = typer.Typer(
    name="netprobe",
    help="🔍 Network scanner for SSH, SNMP, MySQL, HTTP and HTTPS discovery",
    # Locals of scan() include SNMP secrets; never print them in a traceback.
    pretty_exceptions_show_locals=False,
    add_completion=False,
)


def explicit_option(ctx: typer.Context, name: str) -> bool:
    source = ctx.get_parameter_source(name)
    return source is not None and source.name == "COMMANDLINE"


@app.command()
def scan(
    ctx: typer.Context,
    network: str | None = typer.Argument(
        None, help="Network CIDR (e.g., 192.168.1.0/24) or single IP"
    ),
    output: Path = typer.Option(
        None, "--output", "-o", help="Output file (JSON or CSV, detected by extension)"
    ),
    format: Literal["json", "csv", "kadupul", "auto"] = typer.Option(
        "auto",
        "--format",
        "-f",
        help="Output format (auto-detects from filename; .sh means kadupul)",
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
        DEFAULT_CONCURRENCY,
        "--concurrency",
        min=1,
        max=MAX_CONCURRENCY,
        help="Maximum probes in flight",
    ),
    config: Path | None = typer.Option(
        None, "--config", help="TOML file whose [services] table extends the defaults"
    ),
    services: str | None = typer.Option(
        None, "--services", help="Comma list of service names to check (default: all)"
    ),
    ports: str | None = typer.Option(
        None, "--ports", help="Comma list of NAME=PORT overrides or extra TCP PORTs"
    ),
    snmp_community: str | None = typer.Option(
        None,
        "--snmp-community",
        envvar="NETPROBE_SNMP_COMMUNITY",
        help="SNMPv2c community for the system MIB query (prefer the env var)",
        show_default=False,
    ),
    snmp_user: str | None = typer.Option(
        None, "--snmp-user", envvar="NETPROBE_SNMP_USER", help="SNMPv3 user name"
    ),
    snmp_auth_protocol: AuthProtocol = typer.Option(
        "SHA", "--snmp-auth-protocol", envvar="NETPROBE_SNMP_AUTH_PROTOCOL"
    ),
    snmp_auth_key: str | None = typer.Option(
        None,
        "--snmp-auth-key",
        envvar="NETPROBE_SNMP_AUTH_KEY",
        help="SNMPv3 authentication passphrase (prefer the env var)",
        show_default=False,
    ),
    snmp_priv_protocol: PrivProtocol = typer.Option(
        "AES", "--snmp-priv-protocol", envvar="NETPROBE_SNMP_PRIV_PROTOCOL"
    ),
    snmp_priv_key: str | None = typer.Option(
        None,
        "--snmp-priv-key",
        envvar="NETPROBE_SNMP_PRIV_KEY",
        help="SNMPv3 privacy passphrase (prefer the env var)",
        show_default=False,
    ),
    save_snapshot: Path | None = typer.Option(
        None, "--save-snapshot", help="Also write a versioned snapshot for `netprobe diff`"
    ),
    profile: str | None = typer.Option(None, "--profile", help="Named inventory profile"),
    exclude: list[str] | None = typer.Option(
        None, "--exclude", help="Excluded IP/CIDR; repeat as needed"
    ),
    max_hosts: int = typer.Option(MAX_HOSTS, "--max-hosts", min=1, max=MAX_HOSTS),
    history: Path | None = typer.Option(None, "--history", help="Opt-in SQLite scan history"),
    tls_ca_file: Path | None = typer.Option(
        None,
        "--tls-ca-file",
        envvar="NETPROBE_TLS_CA_FILE",
        help="PEM bundle to verify HTTPS certificates against instead of the system store",
    ),
) -> None:
    """
    🔍 Scan network for SSH, SNMP, MySQL, HTTP and HTTPS services.

    Examples:

        # Scan entire network
        netprobe scan 192.168.1.0/24

        # Scan single host with JSON output
        netprobe scan 192.168.1.1 -o results.json

        # Scan and save to CSV
        netprobe scan 10.0.0.0/24 --output report.csv

        # Quiet mode (no table, only file output)
        netprobe scan 192.168.1.0/24 -o results.json --quiet

        # Only SSH, on a non-standard port, plus a plain check of 8080
        netprobe scan 10.0.0.0/24 --services ssh --ports ssh=2222,8080
    """
    # Set logging level
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    for name in ("snmp_community", "snmp_auth_key", "snmp_priv_key"):
        source = ctx.get_parameter_source(name)
        if source is not None and source.name == "COMMANDLINE":
            logger.warning(
                f"--{name.replace('_', '-')} on the command line is visible in the process "
                f"list; prefer NETPROBE_{name.upper()}"
            )

    snmp = None
    try:
        if snmp_community or snmp_user or snmp_auth_key or snmp_priv_key:
            snmp = SnmpCredentials(
                community=snmp_community,
                user=snmp_user,
                auth_protocol=snmp_auth_protocol,
                auth_key=snmp_auth_key,
                priv_protocol=snmp_priv_protocol,
                priv_key=snmp_priv_key,
            )
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(2) from e

    try:
        if profile is not None and config is None:
            config = Path("netprobe.toml")
        settings = resolve_profile(
            network,
            config,
            profile,
            {
                "backend": backend if explicit_option(ctx, "backend") else None,
                "timeout": timeout if explicit_option(ctx, "timeout") else None,
                "concurrency": concurrency if explicit_option(ctx, "concurrency") else None,
                "max_hosts": max_hosts if explicit_option(ctx, "max_hosts") else None,
                "services": services,
                "ports": ports,
                "exclusions": exclude,
            },
        )
        network = str(settings["network"])
        backend = settings.get("backend", backend)
        timeout = settings.get("timeout", timeout)
        concurrency = settings.get("concurrency", concurrency)
        max_hosts = settings.get("max_hosts", max_hosts)
        services, ports = settings.get("services", services), settings.get("ports", ports)
        exclusions = settings.get("exclusions", [])
    except ConfigError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(2) from e

    try:
        specs = select_services(
            load_services(config) if config else DEFAULT_SERVICES, services, ports
        )
    except ConfigError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(2) from e

    try:
        preflight = check_plan(
            network,
            specs,
            backend,
            max_hosts,
            exclusions,
            [path for path in (output, save_snapshot, history) if path is not None],
            config=config,
            history=history,
            tls_ca_file=tls_ca_file,
        )
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(2) from e
    failed = [check for check in preflight["checks"] if check["status"] == "error"]
    if failed:
        for check in failed:
            typer.echo(f"Preflight failed ({check['check']}): {check['detail']}", err=True)
        raise typer.Exit(1)
    store = HistoryStore(history) if history is not None else None
    if store is not None:
        try:
            store.initialize()
        except (OSError, ValueError, sqlite3.Error) as e:
            typer.echo(f"History failed: {e}", err=True)
            raise typer.Exit(1) from e
    started_at = utc_now()

    try:
        scanner = NetworkScanner(
            backend=backend,
            timeout=timeout,
            concurrency=concurrency,
            services=specs,
            snmp=snmp,
            tls_ca_file=str(tls_ca_file) if tls_ca_file else None,
            max_hosts=max_hosts,
            exclusions=exclusions,
        )
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
        disable=quiet,
    ) as progress:
        try:
            devices = asyncio.run(scanner.scan_network(network, progress))
        except (ValueError, BackendUnavailableError) as e:
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(1 if isinstance(e, BackendUnavailableError) else 2) from e

    if store is not None:
        observations = []
        for device in devices:
            record = asdict(device)
            record["status"] = (
                "up"
                if device.alive
                else (
                    "unresponsive"
                    if device.errors == ["Host is down"]
                    else "error"
                    if device.errors
                    else "unknown"
                )
            )
            record["port_states"] = {
                f"{service.port}/{service.protocol}": service.state for service in device.services
            }
            observations.append(record)
        metadata = {
            "schema_version": 1,
            "netprobe_version": package_version("netprobe"),
            "profile": profile,
            "target": network,
            "backend": backend,
            "timeout": timeout,
            "concurrency": concurrency,
            "max_hosts": max_hosts,
            "exclusions": exclusions,
            "services": [asdict(spec) for spec in specs],
            "ports": sorted({f"{spec.port}/{spec.protocol}" for spec in specs}),
        }
        try:
            scan_id = store.save(metadata, observations, started_at)
        except (OSError, ValueError, sqlite3.Error) as e:
            typer.echo(f"History failed: {e}", err=True)
            raise typer.Exit(1) from e
        if not quiet:
            typer.echo(f"Saved history scan {scan_id}")

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
            elif ext == ".sh":
                format = "kadupul"
            else:
                logger.warning(f"Unknown extension {ext}, defaulting to JSON")
                format = "json"

        try:
            match format:
                case "json":
                    save_json(devices, output)
                case "csv":
                    save_csv(devices, output)
                case "kadupul":
                    opts = KadupulOptions(
                        snmp_user=snmp_user,
                        auth_protocol=snmp_auth_protocol,
                        priv_protocol=snmp_priv_protocol,
                    )
                    script = kadupul_script((asdict(d) for d in devices), opts, f"scan {network}")
                    write_script(output, script, secret=False)
        except ExportError as e:
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(2) from e
        except OSError as e:
            typer.echo(f"Error: cannot write {output}: {e}", err=True)
            raise typer.Exit(1) from e

    if save_snapshot:
        try:
            write_snapshot(save_snapshot, network, specs, devices)
        except OSError as e:
            typer.echo(f"Error: cannot write {save_snapshot}: {e}", err=True)
            raise typer.Exit(1) from e


@app.command()
def export(
    source: Path = typer.Argument(..., help="Snapshot or scan -o JSON report"),
    output: Path = typer.Option(..., "--output", "-o", help="Script to write"),
    template: int = typer.Option(
        0,
        "--template",
        min=0,
        help="Kadupul host template id (see add_device.php --list-host-templates)",
    ),
    snmp_user: str | None = typer.Option(None, "--snmp-user", envvar="NETPROBE_SNMP_USER"),
    snmp_auth_protocol: AuthProtocol = typer.Option(
        "SHA", "--snmp-auth-protocol", envvar="NETPROBE_SNMP_AUTH_PROTOCOL"
    ),
    snmp_priv_protocol: PrivProtocol = typer.Option(
        "AES", "--snmp-priv-protocol", envvar="NETPROBE_SNMP_PRIV_PROTOCOL"
    ),
    include_credentials: bool = typer.Option(
        False,
        "--include-credentials",
        help="Write SNMP secrets from NETPROBE_SNMP_* into the script instead of env references",
    ),
) -> None:
    """
    Write a Kadupul import script: one `php cli/add_device.php` call per host.

    Run the result on the Kadupul server: KADUPUL_ROOT=/path sh SCRIPT
    """
    try:
        inventory = load_inventory(source)
        opts = KadupulOptions(
            template=template,
            snmp_user=snmp_user,
            auth_protocol=snmp_auth_protocol,
            priv_protocol=snmp_priv_protocol,
            # Secrets only ever come from the environment here, never argv.
            community=os.environ.get("NETPROBE_SNMP_COMMUNITY") if include_credentials else None,
            auth_key=os.environ.get("NETPROBE_SNMP_AUTH_KEY") if include_credentials else None,
            priv_key=os.environ.get("NETPROBE_SNMP_PRIV_KEY") if include_credentials else None,
            include_credentials=include_credentials,
        )
        script = kadupul_script(inventory.devices, opts, str(source))
    except (SnapshotError, ExportError) as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(2) from e
    if include_credentials:
        logger.warning(
            f"{output} contains SNMP credentials; keep it private and delete it after use"
        )
    try:
        write_script(output, script, secret=include_credentials)
    except OSError as e:
        typer.echo(f"Error: cannot write {output}: {e}", err=True)
        raise typer.Exit(1) from e


# Distinct from 1 (error) and 2 (usage), so scripts can branch on "changed".
EXIT_CHANGED = 3


@app.command()
def diff(
    old: Path = typer.Argument(..., help="Earlier snapshot (or scan -o JSON report)"),
    new: Path = typer.Argument(..., help="Later snapshot (or scan -o JSON report)"),
    format: Literal["table", "json"] = typer.Option("table", "--format", "-f"),
    output: Path | None = typer.Option(
        None, "--output", "-o", help="Also write the diff as JSON here"
    ),
) -> None:
    """
    Compare two snapshots: new and vanished hosts, opened and closed ports,
    changed service versions.

    Exit status: 0 no changes, 3 changes found, 2 unreadable input, 1 write error.
    """
    try:
        result = compare(load_inventory(old), load_inventory(new))
    except SnapshotError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(2) from e

    if format == "json":
        text = json.dumps(result.to_dict(), indent=2) + "\n"
        if output is None:
            typer.echo(text, nl=False)
    else:
        print_diff(result, console)
    if output is not None:
        try:
            output.write_text(json.dumps(result.to_dict(), indent=2) + "\n")
        except OSError as e:
            typer.echo(f"Error: cannot write {output}: {e}", err=True)
            raise typer.Exit(1) from e
    raise typer.Exit(EXIT_CHANGED if result.changed else 0)


@app.command(name="history")
def history_command(
    history_path: Path = typer.Option(Path("netprobe-history.sqlite3"), "--history"),
    limit: int = typer.Option(20, min=1, max=1000),
) -> None:
    """List saved inventory IDs and summaries, newest first; never creates a database."""
    try:
        summaries = HistoryStore(history_path).list_summaries(limit)
        typer.echo(json.dumps(summaries, indent=2))
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error) as exc:
        typer.echo(f"History failed: {exc}", err=True)
        raise typer.Exit(1) from exc


@app.command(name="compare")
def history_compare(
    before: int = typer.Argument(..., min=1, help="Earlier scan ID"),
    after: int = typer.Argument(..., min=1, help="Later scan ID"),
    history_path: Path = typer.Option(Path("netprobe-history.sqlite3"), "--history"),
    output: Path | None = typer.Option(None, "--output", "-o", help="Write comparison JSON"),
) -> None:
    """Compare equal-scope snapshots without scanning or claiming failed hosts disappeared."""
    try:
        store = HistoryStore(history_path)
        report = compare_scans(store.get(before), store.get(after))
        rendered = json.dumps(report, indent=2)
        if output is not None:
            if paths_overlap(output, history_path):
                raise ValueError("Comparison output must not overwrite history")
            from netprobe.history import check_writable_path

            check_writable_path(output)
            output.write_text(rendered + "\n", encoding="utf-8")
        else:
            typer.echo(rendered)
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error) as exc:
        typer.echo(f"Comparison failed: {exc}", err=True)
        raise typer.Exit(1) from exc


@app.command()
def version() -> None:
    """Show version information."""
    rprint(f"[bold cyan]netprobe[/bold cyan] [green]v{package_version('netprobe')}[/green]")
    rprint("Modern network scanner built with Python 3.12+")


@app.command()
def profiles(config: Path = typer.Option(Path("netprobe.toml"), "--config")) -> None:
    """List validated named profiles without target traffic."""
    try:
        entries = load_profiles(config)
        for profile in entries.values():
            select_services(load_services(config), profile.services, profile.ports)
        typer.echo(
            json.dumps({name: asdict(profile) for name, profile in entries.items()}, indent=2)
        )
    except ConfigError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(2) from e


@app.command()
def preflight(
    network: str | None = typer.Argument(None),
    profile: str | None = typer.Option(None, "--profile"),
    config: Path | None = typer.Option(None, "--config"),
    backend: Literal["asyncio", "nmap"] | None = typer.Option(None, "--backend"),
    services: str | None = typer.Option(None, "--services"),
    ports: str | None = typer.Option(None, "--ports"),
    exclude: list[str] | None = typer.Option(None, "--exclude"),
    max_hosts: int | None = typer.Option(None, "--max-hosts", min=1, max=MAX_HOSTS),
    output: Path | None = typer.Option(None, "--output", "-o"),
    save_snapshot: Path | None = typer.Option(None, "--save-snapshot"),
    history: Path | None = typer.Option(None, "--history"),
    tls_ca_file: Path | None = typer.Option(None, "--tls-ca-file", envvar="NETPROBE_TLS_CA_FILE"),
) -> None:
    """Check target limits, backend availability and destinations without scanning."""
    try:
        if profile is not None and config is None:
            config = Path("netprobe.toml")
        settings = resolve_profile(
            network,
            config,
            profile,
            {
                "backend": backend,
                "services": services,
                "ports": ports,
                "exclusions": exclude,
                "max_hosts": max_hosts,
            },
        )
        specs = select_services(
            load_services(config) if config else DEFAULT_SERVICES,
            settings.get("services"),
            settings.get("ports"),
        )
        result = check_plan(
            settings["network"],
            specs,
            settings.get("backend", "asyncio"),
            settings.get("max_hosts", MAX_HOSTS),
            settings.get("exclusions", []),
            [path for path in (output, save_snapshot, history) if path is not None],
            config=config,
            history=history,
            tls_ca_file=tls_ca_file,
        )
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(2) from e
    typer.echo(json.dumps(result, indent=2))
    if any(check["status"] == "error" for check in result["checks"]):
        raise typer.Exit(1)
