"""Command-line interface for the network discovery tool.

This module provides the command-line interface for the application.
"""

import argparse
import asyncio
import logging
import os
import sys
from typing import List, Optional

from network_discovery.core.discovery import DeviceDiscoveryService
from network_discovery.infrastructure.scanner import NmapDeviceScanner
from network_discovery.infrastructure.repository import JsonFileRepository
from network_discovery.infrastructure.notification import ConsoleNotificationService
from network_discovery.infrastructure.report import ReportGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        args: The command-line arguments to parse. If None, sys.argv is used.

    Returns:
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Network discovery tool using Nmap to identify SSH, Ping, and SNMP on connected devices."
    )
    parser.add_argument(
        "network",
        help="The network to scan, in CIDR notation (e.g., 192.168.1.0/24), or a single IP address.",
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

    return parser.parse_args(args)


async def run_discovery(args: argparse.Namespace) -> None:
    """Run the device discovery process.

    Args:
        args: The command-line arguments.
    """
    # Configure services
    scanner = NmapDeviceScanner()
    repository = None if args.no_repository else JsonFileRepository(args.repository_file)
    notification_service = None if args.no_notification else ConsoleNotificationService()
    report_service = None
    if not args.no_report:
        report_service = ReportGenerator(args.output_dir, args.template_dir)

    # Create discovery service
    discovery_service = DeviceDiscoveryService(
        scanner, repository, notification_service, report_service
    )

    # Run discovery
    try:
        if "/" in args.network:
            # Network scan
            devices = await discovery_service.discover_network(args.network)
            logger.info("Discovered %d devices", len(devices))
        else:
            # Single device scan
            device = await discovery_service.discover_device(args.network)
            logger.info("Device status: %s", device.status())
    except Exception as e:
        logger.error("Error during discovery: %s", e)
        sys.exit(1)

    # Generate report
    if report_service:
        try:
            report_path = discovery_service.generate_report(args.format)
            logger.info("Report generated at %s", report_path)
        except Exception as e:
            logger.error("Error generating report: %s", e)


def cli(args: Optional[List[str]] = None) -> None:
    """Run the command-line interface.

    Args:
        args: The command-line arguments to parse. If None, sys.argv is used.
    """
    parsed_args = parse_args(args)

    # Configure logging
    if parsed_args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create output directory if it doesn't exist
    os.makedirs(parsed_args.output_dir, exist_ok=True)

    # Run discovery
    asyncio.run(run_discovery(parsed_args))


if __name__ == "__main__":
    cli()
