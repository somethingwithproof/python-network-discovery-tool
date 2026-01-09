#!/usr/bin/env python3
"""
Network device discovery orchestrator.

This script coordinates the scanning of network devices imported from an Excel file,
stores results in a SQLite database, and exports the results.

Requires Python 3.12+
"""

from __future__ import annotations

import argparse
import logging
import sys
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

import database
import spreadsheet
from devices import Device, ScanConfig

# Type alias
type DeviceList = list[Device]

# Configure logging
logging.basicConfig(
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class ExitCode(StrEnum):
    """Exit codes for the CLI."""
    SUCCESS = "0"
    ERROR = "1"
    CONFIG_ERROR = "2"
    INPUT_ERROR = "3"


@dataclass(slots=True)
class DiscoveryStats:
    """Statistics from a discovery run."""

    total: int = 0
    alive: int = 0
    ssh: int = 0
    snmp: int = 0
    mysql: int = 0
    errors: int = 0

    @classmethod
    def from_devices(cls, devices: Sequence[Device]) -> DiscoveryStats:
        """Calculate statistics from a list of devices."""
        return cls(
            total=len(devices),
            alive=sum(1 for d in devices if d.alive),
            ssh=sum(1 for d in devices if d.ssh),
            snmp=sum(1 for d in devices if d.snmp),
            mysql=sum(1 for d in devices if d.mysql),
            errors=sum(1 for d in devices if d.errors),
        )

    def __str__(self) -> str:
        return (
            f"Total: {self.total}, Alive: {self.alive}, "
            f"SSH: {self.ssh}, SNMP: {self.snmp}, MySQL: {self.mysql}, "
            f"Errors: {self.errors}"
        )


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog='network-discover',
        description='Discover network device services (SSH, SNMP, MySQL).',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s devices.xlsx
  %(prog)s devices.xlsx -o results.xlsx -w 20
  %(prog)s devices.xlsx --no-ssh-strict -v
  %(prog)s devices.xlsx --no-ping-gate --keep-db

Environment Variables:
  SSH_USER                SSH username (default: root)
  SSH_KNOWN_HOSTS_FILE    Path to SSH known_hosts file
  SSH_STRICT_HOST_KEY     Enable strict host key checking (default: true)
        """,
    )

    parser.add_argument(
        'inputfile',
        type=Path,
        help='Excel file with hosts to scan',
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output Excel file (default: <date>_check.xlsx)',
    )
    parser.add_argument(
        '-w', '--workers',
        type=int,
        default=10,
        metavar='N',
        help='Maximum concurrent workers (default: 10)',
    )
    parser.add_argument(
        '-d', '--database',
        type=Path,
        default=Path('devices.db'),
        help='SQLite database file (default: devices.db)',
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose (debug) logging',
    )
    parser.add_argument(
        '--no-ssh-strict',
        action='store_true',
        help='Disable strict SSH host key checking (less secure)',
    )
    parser.add_argument(
        '--no-ping-gate',
        action='store_true',
        help='Scan SSH/SNMP/MySQL even if ping fails (recommended for firewalled networks)',
    )
    parser.add_argument(
        '--keep-db',
        action='store_true',
        help='Preserve existing database instead of recreating it',
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.3.0',
    )

    return parser.parse_args(args)


def scan_device(device: Device, config: ScanConfig) -> Device:
    """
    Scan a single device for all services.

    This function is designed to be called from a thread pool.
    """
    logger.debug("Starting scan: %s", device.host)

    try:
        device.scan_all(config)
        logger.info("Completed: %s", device)
    except Exception as e:
        logger.error("Failed: %s - %s", device.host, e)
        device.add_error(f"Scan failed: {e}")

    return device


def scan_devices(
    devices: DeviceList,
    config: ScanConfig,
    *,
    max_workers: int = 10,
) -> DeviceList:
    """
    Scan multiple devices concurrently.

    Uses ThreadPoolExecutor for concurrent I/O operations.
    """
    if not devices:
        logger.warning("No devices to scan")
        return []

    workers = min(len(devices), max_workers)
    logger.info("Scanning %d devices with %d workers", len(devices), workers)

    scanned: DeviceList = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Submit all scan tasks
        future_to_device = {
            executor.submit(scan_device, device, config): device
            for device in devices
        }

        # Collect results as they complete
        for future in as_completed(future_to_device):
            original = future_to_device[future]
            try:
                scanned.append(future.result())
            except Exception as e:
                logger.exception("Unexpected error scanning %s", original.host)
                original.add_error(f"Unexpected error: {e}")
                scanned.append(original)

    logger.info("Scan complete: %d devices processed", len(scanned))
    return scanned


def print_summary(stats: DiscoveryStats) -> None:
    """Print a formatted summary of the discovery results."""
    width = 50
    print()
    print("=" * width)
    print("Discovery Summary".center(width))
    print("=" * width)
    print(f"  {'Total devices:':<20} {stats.total:>10}")
    print(f"  {'Alive (ping):':<20} {stats.alive:>10}")
    print(f"  {'SSH accessible:':<20} {stats.ssh:>10}")
    print(f"  {'SNMP accessible:':<20} {stats.snmp:>10}")
    print(f"  {'MySQL accessible:':<20} {stats.mysql:>10}")
    print(f"  {'With errors:':<20} {stats.errors:>10}")
    print("=" * width)


def main(argv: Sequence[str] | None = None) -> int:
    """Main entry point."""
    args = parse_args(argv)

    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate input file
    input_path: Path = args.inputfile
    if not input_path.exists():
        logger.error("Input file not found: %s", input_path)
        return int(ExitCode.INPUT_ERROR)

    if input_path.suffix.lower() not in ('.xlsx', '.xls'):
        logger.warning("Input file may not be an Excel file: %s", input_path)

    # Create configuration
    config = ScanConfig(
        ssh_strict_host_key=not args.no_ssh_strict,
        skip_ping_gate=args.no_ping_gate,
    )

    # Initialize database
    db_path: Path = args.database
    logger.info("Initializing database: %s", db_path)
    db = database.Database(db_path)
    db.create_table(drop_existing=not args.keep_db)

    # Import devices from Excel
    logger.info("Importing devices from: %s", input_path)
    try:
        devices = spreadsheet.import_from_excel(input_path)
    except Exception as e:
        logger.error("Failed to import devices: %s", e)
        return int(ExitCode.INPUT_ERROR)

    if not devices:
        logger.warning("No devices found in input file")
        return int(ExitCode.SUCCESS)

    logger.info("Imported %d devices", len(devices))

    # Store devices in database
    db.insert_devices(devices)

    # Scan devices
    scanned = scan_devices(devices, config, max_workers=args.workers)

    # Update database with results
    logger.info("Updating database with scan results")
    for device in scanned:
        db.update_device(device)

    # Export results
    logger.info("Exporting results")
    try:
        # Export to new Excel file
        output_path = spreadsheet.export_to_excel(scanned, args.output)
        logger.info("Results exported to: %s", output_path)

        # Update original input file with results
        if args.output != input_path:
            spreadsheet.export_to_excel(scanned, input_path)
            logger.info("Updated input file: %s", input_path)

    except Exception as e:
        logger.error("Failed to export results: %s", e)
        return int(ExitCode.ERROR)

    # Print summary
    stats = DiscoveryStats.from_devices(scanned)
    print_summary(stats)

    return int(ExitCode.SUCCESS)


if __name__ == "__main__":
    sys.exit(main())
