"""
SQLite database storage module for network device management.

This module provides persistent storage for network device data using SQLite,
with support for import/export in various formats (CSV, Excel, HTML).

Security Note:
    Credentials (MySQL passwords, SNMP communities) are NOT persisted to the
    database. They are read from the input Excel file at scan time only.

Requires Python 3.12+
"""

from __future__ import annotations

import csv
import logging
import sqlite3
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from devices import Device, ValidationError

# Type aliases using Python 3.12+ syntax
type DeviceList = list[Device]

logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Raised when a database operation fails."""

    __slots__ = ('operation', 'details')

    def __init__(
        self,
        message: str,
        *,
        operation: str | None = None,
        details: str | None = None,
    ) -> None:
        super().__init__(message)
        self.operation = operation
        self.details = details


@dataclass(slots=True, frozen=True)
class DatabaseConfig:
    """Immutable configuration for database operations."""

    database_path: Path
    template_dir: Path = Path("templates")
    journal_mode: str = "WAL"
    synchronous: str = "NORMAL"
    foreign_keys: bool = True


class Database:
    """
    SQLite database for storing network device information.

    Uses context manager protocol for safe resource management.
    Supports connection pooling and WAL mode for better concurrency.
    """

    __slots__ = ('_path', '_config')

    # SQL statements as class constants for clarity
    _CREATE_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            host TEXT NOT NULL,
            ip TEXT,
            snmp_community TEXT DEFAULT 'public',
            alive INTEGER DEFAULT 0,
            snmp INTEGER DEFAULT 0,
            ssh INTEGER DEFAULT 0,
            mysql INTEGER DEFAULT 0,
            errors TEXT,
            mysql_user TEXT,
            mysql_password TEXT,
            uname TEXT,
            scanned INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        )
    """

    _CREATE_INDEX_SQL = """
        CREATE INDEX IF NOT EXISTS idx_devices_host ON devices(host)
    """

    def __init__(self, database_path: str | Path, *, config: DatabaseConfig | None = None) -> None:
        """Initialize database connection."""
        self._path = Path(database_path)
        self._config = config or DatabaseConfig(database_path=self._path)

    @property
    def path(self) -> Path:
        """Get the database file path."""
        return self._path

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        """Get a database connection with automatic cleanup and configuration."""
        conn = sqlite3.connect(
            str(self._path),
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        conn.row_factory = sqlite3.Row

        try:
            # Configure connection for better performance
            conn.execute(f"PRAGMA journal_mode={self._config.journal_mode}")
            conn.execute(f"PRAGMA synchronous={self._config.synchronous}")
            conn.execute(f"PRAGMA foreign_keys={'ON' if self._config.foreign_keys else 'OFF'}")

            yield conn
            conn.commit()

        except sqlite3.Error as e:
            conn.rollback()
            raise DatabaseError(f"Database error: {e}", operation="transaction") from e

        finally:
            conn.close()

    def create_table(self, *, drop_existing: bool = False) -> None:
        """
        Create the devices table.

        Args:
            drop_existing: If True, drop existing table first (destructive!)
        """
        with self._connection() as conn:
            cursor = conn.cursor()

            if drop_existing:
                logger.warning("Dropping existing devices table - data will be lost!")
                cursor.execute("DROP TABLE IF EXISTS devices")

            cursor.execute(self._CREATE_TABLE_SQL)
            cursor.execute(self._CREATE_INDEX_SQL)

        logger.info("Database table initialized: %s", self._path)

    def _row_to_device(self, row: sqlite3.Row) -> Device:
        """Convert a database row to a Device object."""
        try:
            return Device(
                id=row['id'],
                host=row['host'],
                ip=row['ip'] or row['host'],
                snmp_community=row['snmp_community'] or 'public',
                alive=bool(row['alive']),
                snmp=bool(row['snmp']),
                ssh=bool(row['ssh']),
                mysql=bool(row['mysql']),
                errors=row['errors'].split(', ') if row['errors'] else [],
                mysql_user=row['mysql_user'] or '',
                _mysql_password=row['mysql_password'] or '',
                uname=row['uname'] or '',
                scanned=bool(row['scanned']),
            )
        except ValidationError as e:
            logger.error("Invalid device data in row %s: %s", row['id'], e)
            raise DatabaseError(
                f"Invalid device data: {e}",
                operation="row_to_device",
                details=str(row['id']),
            ) from e

    def get_all_devices(self) -> DeviceList:
        """Retrieve all devices from the database."""
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM devices ORDER BY id")

            devices: DeviceList = []
            for row in cursor.fetchall():
                try:
                    devices.append(self._row_to_device(row))
                except DatabaseError as e:
                    logger.warning("Skipping invalid device: %s", e.details)

            return devices

    def get_device(self, device_id: int) -> Device | None:
        """Retrieve a single device by ID."""
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))

            if row := cursor.fetchone():
                return self._row_to_device(row)
            return None

    def get_device_by_host(self, host: str) -> Device | None:
        """Retrieve a device by hostname."""
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM devices WHERE host = ?", (host,))

            if row := cursor.fetchone():
                return self._row_to_device(row)
            return None

    def insert_device(self, device: Device) -> int:
        """Insert a new device and return its ID.

        Note: Credentials are NOT stored for security reasons.
        """
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO devices (
                    host, ip, snmp_community, alive, snmp, ssh, mysql,
                    errors, mysql_user, mysql_password, uname, scanned
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    device.host,
                    device.ip,
                    '',  # snmp_community not stored for security
                    int(device.alive),
                    int(device.snmp),
                    int(device.ssh),
                    int(device.mysql),
                    ', '.join(device.errors),
                    device.mysql_user,
                    '',  # mysql_password not stored for security
                    device.uname,
                    int(device.scanned),
                ),
            )
            return cursor.lastrowid or 0

    def insert_devices(self, devices: Sequence[Device]) -> int:
        """Bulk insert devices and return count of inserted rows.

        Note: Credentials are NOT stored for security reasons.
        """
        if not devices:
            return 0

        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(
                """
                INSERT INTO devices (
                    host, ip, snmp_community, alive, snmp, ssh, mysql,
                    errors, mysql_user, mysql_password, uname, scanned
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        d.host, d.ip, '',  # snmp_community not stored
                        int(d.alive), int(d.snmp), int(d.ssh), int(d.mysql),
                        ', '.join(d.errors), d.mysql_user, '',  # password not stored
                        d.uname, int(d.scanned),
                    )
                    for d in devices
                ],
            )
            return cursor.rowcount

    def update_device(self, device: Device) -> bool:
        """Update an existing device. Returns True if updated.

        Note: Credentials are NOT stored for security reasons.
        """
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE devices SET
                    host = ?, ip = ?, snmp_community = ?,
                    alive = ?, snmp = ?, ssh = ?, mysql = ?,
                    errors = ?, mysql_user = ?, mysql_password = ?,
                    uname = ?, scanned = ?,
                    updated_at = datetime('now')
                WHERE id = ?
                """,
                (
                    device.host, device.ip, '',  # snmp_community not stored
                    int(device.alive), int(device.snmp), int(device.ssh), int(device.mysql),
                    ', '.join(device.errors), device.mysql_user, '',  # password not stored
                    device.uname, int(device.scanned),
                    device.id,
                ),
            )
            return cursor.rowcount > 0

    def delete_device(self, device_id: int) -> bool:
        """Delete a device by ID. Returns True if deleted."""
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM devices WHERE id = ?", (device_id,))
            return cursor.rowcount > 0

    def count_devices(self) -> int:
        """Get total count of devices."""
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM devices")
            return cursor.fetchone()[0]


@dataclass(slots=True)
class Exporter:
    """Export device data to various formats."""

    devices: DeviceList
    template_dir: Path = field(default_factory=lambda: Path("templates"))

    def to_csv(self, filename: str | Path) -> Path:
        """Export devices to CSV format."""
        filepath = Path(filename)

        with filepath.open('w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'id', 'host', 'ip', 'snmp_community', 'alive',
                'snmp', 'ssh', 'mysql', 'uname', 'errors', 'scanned', 'status',
            ])
            for device in self.devices:
                writer.writerow([
                    device.id, device.host, device.ip, device.snmp_community,
                    device.alive, device.snmp, device.ssh, device.mysql,
                    device.uname, '; '.join(device.errors), device.scanned,
                    device.status.value,
                ])

        logger.info("Exported %d devices to %s", len(self.devices), filepath)
        return filepath

    def to_html(self, filename: str | Path) -> Path:
        """Export devices to HTML using Jinja2 template."""
        filepath = Path(filename)

        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory not found: {self.template_dir}")

        env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(['html', 'xml']),
        )
        template = env.get_template('layout.html')

        # Convert devices to safe dictionaries (credentials masked)
        device_data = [d.to_dict(mask_credentials=True) for d in self.devices]
        output = template.render(devices=device_data)

        filepath.write_text(output, encoding='utf-8')
        logger.info("Exported %d devices to %s", len(self.devices), filepath)
        return filepath


@dataclass(slots=True)
class Importer:
    """Import device data from various formats."""

    database: Database

    def from_csv(self, filename: str | Path) -> int:
        """Import devices from CSV file. Returns count of imported devices."""
        filepath = Path(filename)

        if not filepath.exists():
            raise FileNotFoundError(f"CSV file not found: {filepath}")

        devices: DeviceList = []

        with filepath.open('r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    device = Device(
                        id=0,  # Will be assigned by database
                        host=row.get('host', ''),
                        ip=row.get('ip', row.get('host', '')),
                        snmp_community=row.get('snmp_community', 'public'),
                        mysql_user=row.get('mysql_user', ''),
                        _mysql_password=row.get('mysql_password', ''),
                    )
                    devices.append(device)
                except ValidationError as e:
                    logger.warning("Skipping invalid row: %s", e)

        count = self.database.insert_devices(devices)
        logger.info("Imported %d devices from %s", count, filepath)
        return count


# Convenience functions for backward compatibility and simple usage
def create(database_path: str | Path) -> Database:
    """Create a database and initialize the schema."""
    db = Database(database_path)
    db.create_table()
    return db


def get_all_devices(database_path: str | Path) -> DeviceList:
    """Get all devices from a database."""
    return Database(database_path).get_all_devices()


def update_device(database_path: str | Path, device: Device) -> bool:
    """Update a device in the database."""
    return Database(database_path).update_device(device)


def import_excel(database_path: str | Path, excel_path: str | Path) -> int:
    """Import devices from Excel file."""
    import spreadsheet

    db = Database(database_path)
    db.create_table(drop_existing=True)

    devices = spreadsheet.import_from_excel(excel_path)
    return db.insert_devices(devices)


def export_excel(devices: DeviceList, filename: str | Path | None = None) -> Path:
    """Export devices to Excel file."""
    import spreadsheet
    return spreadsheet.export_to_excel(devices, filename)


if __name__ == '__main__':
    import sys

    print("Database module for network device management")
    print()
    print("Usage:")
    print("  from database import Database")
    print("  db = Database('devices.db')")
    print("  db.create_table()")
    print("  devices = db.get_all_devices()")

    if len(sys.argv) > 1:
        db_path = sys.argv[1]
        db = Database(db_path)
        db.create_table()
        devices = db.get_all_devices()
        print(f"\nDatabase: {db_path}")
        print(f"Devices: {len(devices)}")
        for device in devices:
            print(f"  - {device}")
