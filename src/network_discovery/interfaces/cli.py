"""Improved command-line interface for the network discovery tool.

This module provides an improved command-line interface for the application with
better input validation and error handling.
"""

import argparse
import asyncio
import ipaddress
import logging
import os
import sys
from typing import List, Optional, Union, Tuple

from network_discovery.core.discovery import DeviceDiscoveryService
from network_discovery.infrastructure.scanner import NmapDeviceScanner
from network_discovery.infrastructure.repository import JsonFileRepository
from network_discovery.infrastructure.notification import (
    ConsoleNotificationService,
    EmailNotificationService,
)
from network_discovery.infrastructure.report import ReportGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def validate_network(
    network: str,
) -> Tuple[bool, Union[ipaddress.IPv4Network, ipaddress.IPv4Address, None], str]:
    """Validate a network or IP address string.

    Args:
        network: The network to validate, in CIDR notation (e.g., "192.168.1.0/24"), or a single IP address.

    Returns:
        A tuple containing:
        - A boolean indicating whether the input is a network (True) or a single IP address (False)
        - The parsed network or IP address object, or None if invalid
        - An error message if the input is invalid, or an empty string if valid
    """
    try:
        if "/" in network:
            # Try to parse as a network
            network_obj = ipaddress.ip_network(network, strict=False)
            return True, network_obj, ""
        else:
            # Try to parse as a single IP address
            ip_obj = ipaddress.ip_address(network)
            return False, ip_obj, ""
    except ValueError as e:
        return False, None, f"Invalid network or IP address format: {e}"


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        args: The command-line arguments to parse. If None, sys.argv is used.

    Returns:
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Network discovery tool using Nmap to identify SSH, Ping, and SNMP on connected devices.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
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


async def run_discovery(args: argparse.Namespace) -> int:
    """Run the device discovery process.

    Args:
        args: The command-line arguments.

    Returns:
        An exit code (0 for success, non-zero for failure).
    """
    # Validate network input
    is_network, network_obj, error = validate_network(args.network)
    if error:
        logger.error(error)
        return 1

    # Configure services
    scanner = NmapDeviceScanner()

    # Configure repository
    repository = None
    if not args.no_repository:
        try:
            repository = JsonFileRepository(args.repository_file)
            logger.info("Using JSON file repository: %s", args.repository_file)
        except Exception as e:
            logger.error("Error initializing repository: %s", e)
            return 1

    # Configure notification service
    notification_service = None
    if not args.no_notification:
        if args.email:
            # Validate email parameters
            if (
                not args.smtp_username
                or not args.smtp_password
                or not args.email_recipient
            ):
                logger.error(
                    "Email notifications require --smtp-username, --smtp-password, and --email-recipient"
                )
                return 1

            try:
                notification_service = EmailNotificationService(
                    args.smtp_server,
                    args.smtp_port,
                    args.smtp_username,
                    args.smtp_password,
                )
                logger.info(
                    "Using email notification service: %s", args.email_recipient
                )
            except Exception as e:
                logger.error("Error initializing email notification service: %s", e)
                return 1
        else:
            notification_service = ConsoleNotificationService()
            logger.info("Using console notification service")

    # Configure report service
    report_service = None
    if not args.no_report:
        try:
            # Create output directory if it doesn't exist
            os.makedirs(args.output_dir, exist_ok=True)

            # Validate template directory for HTML reports
            if args.format == "html" and not os.path.exists(args.template_dir):
                logger.error("Template directory not found: %s", args.template_dir)
                return 1

            report_service = ReportGenerator(args.output_dir, args.template_dir)
            logger.info(
                "Using report generator: %s format, output to %s",
                args.format,
                args.output_dir,
            )
        except Exception as e:
            logger.error("Error initializing report service: %s", e)
            return 1

    # Create discovery service
    discovery_service = DeviceDiscoveryService(
        scanner, repository, notification_service, report_service
    )

    # Run discovery
    try:
        if is_network:
            # Network scan
            logger.info("Starting network discovery for %s", args.network)
            devices = await discovery_service.discover_network(args.network)
            alive_count = sum(1 for d in devices if d.alive)
            logger.info(
                "Discovered %d devices, %d are alive", len(devices), alive_count
            )
        else:
            # Single device scan
            logger.info("Starting device discovery for %s", args.network)
            device = await discovery_service.discover_device(args.network)
            logger.info("Device status: %s", device.status())
    except ValueError as e:
        logger.error("Invalid network format: %s", e)
        return 1
    except Exception as e:
        logger.error("Error during discovery: %s", e)
        return 1

    # Generate report
    if report_service:
        try:
            report_path = discovery_service.generate_report(args.format)
            if report_path:
                logger.info("Report generated at %s", report_path)
            else:
                logger.warning("No report was generated")
        except Exception as e:
            logger.error("Error generating report: %s", e)
            return 1

    return 0


def cli(args: Optional[List[str]] = None) -> int:
    """Run the command-line interface.

    Args:
        args: The command-line arguments to parse. If None, sys.argv is used.

    Returns:
        An exit code (0 for success, non-zero for failure).
    """
    try:
        parsed_args = parse_args(args)

        # Configure logging
        if parsed_args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Verbose logging enabled")

        # Run discovery
        return asyncio.run(run_discovery(parsed_args))
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 130  # Standard exit code for SIGINT
    except Exception as e:
        logger.error("Unexpected error: %s", e, exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(cli())
