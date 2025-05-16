"""Command-line interface for the network discovery tool.

This module provides a Typer-based command-line interface for the network
discovery tool with Pydantic-based settings validation and async execution.

It also includes backward compatibility functions for the legacy argparse-based CLI.
"""

import argparse
import asyncio
import ipaddress
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple, Union

import typer
from pydantic import Field

from network_discovery.core.discovery import DeviceDiscoveryService
from network_discovery.infrastructure.notification import (
    ConsoleNotificationService,
    EmailNotificationService,
)
from network_discovery.infrastructure.repository import JsonFileRepository
from network_discovery.infrastructure.report import ReportGenerator
from network_discovery.infrastructure.scanner import NmapDeviceScanner
from .settings import Settings

# Create Typer app
app = typer.Typer(help="Network discovery tool to identify running services on devices")

def configure_logging(verbose: bool) -> None:
    """Configure logging system based on verbosity level.
    
    Args:
        verbose: If True, set log level to DEBUG; otherwise, set to INFO.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


def validate_network(
    network: str,
) -> Tuple[bool, Union[ipaddress.IPv4Network, ipaddress.IPv4Address, None], str]:
    """Validate a network or IP address string.
    
    Args:
        network: Network CIDR (e.g., "192.168.1.0/24") or IP address.
        
    Returns:
        A tuple containing:
        - Boolean indicating if input is a network (True) or single IP (False)
        - Parsed network/IP object or None if invalid
        - Error message if invalid, or empty string if valid
    """
    try:
        if "/" in network:
            # Parse as a network (CIDR notation)
            network_obj = ipaddress.ip_network(network, strict=False)
            return True, network_obj, ""
        else:
            # Parse as a single IP address
            ip_obj = ipaddress.ip_address(network)
            return False, ip_obj, ""
    except ValueError as e:
        return False, None, f"Invalid network or IP address format: {e}"


def init_repository(settings: Settings):
    """Initialize the device repository based on settings.
    
    Args:
        settings: Application settings containing repository configuration.
        
    Returns:
        Initialized repository service or None if disabled.
        
    Raises:
        Exception: If repository initialization fails.
    """
    if settings.no_repository:
        return None
    
    try:
        repo = JsonFileRepository(settings.repository_file)
        logging.info("Using JSON file repository: %s", settings.repository_file)
        return repo
    except Exception as e:
        logging.getLogger(__name__).error("Error initializing repository: %s", e)
        raise


def init_notification(settings: Settings):
    """Initialize the notification service based on settings.
    
    Args:
        settings: Application settings containing notification configuration.
        
    Returns:
        Initialized notification service or None if disabled.
        
    Raises:
        ValueError: If email notifications are enabled but required settings
            are missing.
    """
    if settings.no_notification:
        return None
    
    if settings.email:
        # Validate email notification settings
        if not settings.smtp_username or not settings.smtp_password or not settings.email_recipient:
            raise ValueError(
                "Email notifications require smtp_username, smtp_password, and email_recipient"
            )
        return EmailNotificationService(
            settings.smtp_server,
            settings.smtp_port,
            settings.smtp_username,
            settings.smtp_password,
        )
    
    return ConsoleNotificationService()


def init_report(settings: Settings):
    """Initialize the report service based on settings.
    
    Args:
        settings: Application settings containing report configuration.
        
    Returns:
        Initialized report service or None if disabled.
        
    Raises:
        ValueError: If HTML reports are enabled but template directory doesn't exist.
    """
    if settings.no_report:
        return None
    
    # Create output directory if it doesn't exist
    settings.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Validate template directory for HTML reports
    if settings.format == "html" and not settings.template_dir.exists():
        raise ValueError(f"Template directory not found: {settings.template_dir}")
    
    return ReportGenerator(settings.output_dir, settings.template_dir)

async def run_discovery(settings: Settings) -> int:
    """Run the network discovery process using the provided settings.
    
    Args:
        settings: Application settings for the discovery process.
        
    Returns:
        int: Exit code (0 for success, 1 for failure).
    """
    # Validate network input
    is_network, network_obj, error = validate_network(settings.network)
    if error:
        logging.getLogger(__name__).error(error)
        return 1

    # Initialize required services
    scanner = NmapDeviceScanner()
    repository = init_repository(settings)
    notification_service = init_notification(settings)
    report_service = init_report(settings)

    # Create discovery service
    discovery_service = DeviceDiscoveryService(
        scanner, repository, notification_service, report_service
    )

    # Run discovery based on input type (network or single device)
    try:
        if is_network:
            # Network scan
            logging.info("Starting network discovery for %s", settings.network)
            devices = await discovery_service.discover_network(settings.network)
            alive_count = sum(1 for d in devices if d.alive)
            logging.info(
                "Discovered %d devices, %d are alive", len(devices), alive_count
            )
        else:
            # Single device scan
            logging.info("Starting device discovery for %s", settings.network)
            device = await discovery_service.discover_device(settings.network)
            logging.info("Device status: %s", device.status())
    except Exception as e:
        logging.getLogger(__name__).error("Error during discovery: %s", e)
        return 1

    # Generate report if enabled
    if report_service:
        try:
            report_path = discovery_service.generate_report(settings.format)
            if report_path:
                logging.info("Report generated at %s", report_path)
            else:
                logging.warning("No report was generated")
        except Exception as e:
            logging.getLogger(__name__).error("Error generating report: %s", e)
            return 1

    return 0

@app.command()
def discover(
    network: str = typer.Argument(
        ..., 
        help="Network CIDR (e.g., 192.168.1.0/24) or single IP address"
    ),
    config: Path = typer.Option(
        Path(".env"), 
        "--config", 
        help="Path to env file with configuration"
    ),
    output_dir: Path = typer.Option(
        Path("./output"), 
        "--output-dir", "-o",
        help="Directory where reports will be saved"
    ),
    format: str = typer.Option(
        "html", 
        "--format", "-f",
        help="Report format (html, csv, xlsx, json)"
    ),
    template_dir: Path = typer.Option(
        Path("./templates"), 
        "--template-dir", "-t",
        help="Directory containing HTML templates"
    ),
    verbose: bool = typer.Option(
        False, 
        "--verbose", "-v", 
        help="Enable verbose logging output"
    ),
    no_report: bool = typer.Option(
        False, 
        "--no-report", 
        help="Disable report generation"
    ),
    no_notification: bool = typer.Option(
        False, 
        "--no-notification", 
        help="Disable notifications"
    ),
    no_repository: bool = typer.Option(
        False, 
        "--no-repository", 
        help="Disable device storage"
    ),
    repository_file: Path = typer.Option(
        Path("./devices.json"), 
        help="File where device data will be stored"
    ),
    email: bool = typer.Option(
        False, 
        "--email", 
        help="Enable email notifications instead of console"
    ),
    smtp_server: str = typer.Option(
        "smtp.gmail.com", 
        "--smtp-server", 
        help="SMTP server for email notifications"
    ),
    smtp_port: int = typer.Option(
        587, 
        "--smtp-port", 
        help="SMTP port for email notifications"
    ),
    smtp_username: str = typer.Option(
        "", 
        "--smtp-username", 
        help="SMTP username for email notifications"
    ),
    smtp_password: str = typer.Option(
        "", 
        "--smtp-password", 
        help="SMTP password for email notifications"
    ),
    email_recipient: str = typer.Option(
        "", 
        "--email-recipient", 
        help="Email address to send notifications to"
    ),
) -> None:
    """Discover network devices and check for running services.
    
    This command scans a network or single device for running services like
    SSH, SNMP, and MySQL. It can generate reports in various formats.
    """
    # Initialize settings from command line arguments and config file
    settings = Settings(
        _env_file=str(config),
        network=network,
        output_dir=output_dir,
        format=format,
        template_dir=template_dir,
        verbose=verbose,
        no_report=no_report,
        no_notification=no_notification,
        no_repository=no_repository,
        repository_file=repository_file,
        email=email,
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        smtp_username=smtp_username,
        smtp_password=smtp_password,
        email_recipient=email_recipient,
    )
    
    # Configure logging based on verbosity setting
    configure_logging(settings.verbose)
    
    # Run the discovery process
    code = asyncio.run(run_discovery(settings))
    sys.exit(code)


def cli() -> None:
    """Run the command-line interface.
    
    This is the main entry point for the command-line interface when the package
    is run as a script.
    """
    app()


# Legacy CLI support functions for backward compatibility with tests
def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        args: The command-line arguments to parse. If None, sys.argv is used.

    Returns:
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Network discovery tool using Nmap to identify SSH, Ping, and SNMP"
        " on connected devices.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "network",
        help="The network to scan in CIDR notation (e.g., 192.168.1.0/24),"
        " or a single IP address.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="./output",
        help="The directory where reports will be saved.",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["html", "csv", "xlsx", "json"],
        default="html",
        help="The format of the report.",
    )
    parser.add_argument(
        "-t",
        "--template-dir",
        default="./templates",
        help="The directory containing HTML templates.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output."
    )
    parser.add_argument(
        "--no-report", action="store_true", help="Disable report generation."
    )
    parser.add_argument(
        "--no-notification", action="store_true", help="Disable notifications."
    )
    parser.add_argument(
        "--no-repository", action="store_true", help="Disable device storage."
    )
    parser.add_argument(
        "--repository-file",
        default="./devices.json",
        help="The file where devices will be stored.",
    )

    # Email notification options
    email_group = parser.add_argument_group("Email Notification Options")
    email_group.add_argument(
        "--email",
        action="store_true",
        help="Enable email notifications instead of console notifications.",
    )
    email_group.add_argument(
        "--smtp-server",
        default="smtp.gmail.com",
        help="The SMTP server to use for email notifications.",
    )
    email_group.add_argument(
        "--smtp-port",
        type=int,
        default=587,
        help="The SMTP port to use for email notifications.",
    )
    email_group.add_argument(
        "--smtp-username",
        help="The SMTP username to use for email notifications.",
    )
    email_group.add_argument(
        "--smtp-password",
        help="The SMTP password to use for email notifications.",
    )
    email_group.add_argument(
        "--email-recipient",
        help="The email address to send notifications to.",
    )

    return parser.parse_args(args)


if __name__ == "__main__":
    cli()