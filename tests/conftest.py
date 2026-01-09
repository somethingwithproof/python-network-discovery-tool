"""
Pytest configuration and shared fixtures for network device discovery tests.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from devices import Device, ScanConfig, ScanType, ScanResult
from database import Database


@pytest.fixture
def sample_device() -> Device:
    """Create a sample device for testing."""
    return Device(
        id=1,
        host="192.168.1.1",
        ip="192.168.1.1",
        snmp_community="public",
    )


@pytest.fixture
def sample_device_with_mysql() -> Device:
    """Create a sample device with MySQL credentials."""
    device = Device(
        id=2,
        host="192.168.1.2",
        ip="192.168.1.2",
        snmp_community="private",
        mysql_user="admin",
    )
    device.mysql_password = "secret123"
    return device


@pytest.fixture
def sample_devices() -> list[Device]:
    """Create a list of sample devices for testing."""
    return [
        Device(id=1, host="192.168.1.1", ip="192.168.1.1"),
        Device(id=2, host="192.168.1.2", ip="192.168.1.2"),
        Device(id=3, host="server.example.com", ip="10.0.0.1"),
    ]


@pytest.fixture
def scan_config() -> ScanConfig:
    """Create a test scan configuration."""
    return ScanConfig(
        ssh_user="testuser",
        ssh_timeout=1,
        ping_timeout=1,
        ping_count=1,
        snmp_timeout=1,
        ssh_strict_host_key=False,
    )


@pytest.fixture
def temp_database() -> Generator[Database, None, None]:
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    db = Database(db_path)
    db.create_table()

    yield db

    # Cleanup
    try:
        os.unlink(db_path)
    except OSError:
        pass


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_subprocess_ping_success():
    """Mock subprocess.run for successful ping."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout=b"PING success")
        yield mock_run


@pytest.fixture
def mock_subprocess_ping_failure():
    """Mock subprocess.run for failed ping."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stdout=b"")
        yield mock_run


@pytest.fixture
def mock_paramiko_success():
    """Mock paramiko for successful SSH connection."""
    with patch('paramiko.SSHClient') as mock_client:
        instance = mock_client.return_value
        instance.connect.return_value = None

        # Mock exec_command
        mock_stdout = MagicMock()
        mock_stdout.read.return_value = b"Linux server 5.4.0 #1 SMP x86_64"
        instance.exec_command.return_value = (MagicMock(), mock_stdout, MagicMock())

        yield mock_client


@pytest.fixture
def mock_paramiko_auth_failure():
    """Mock paramiko for authentication failure."""
    import paramiko
    with patch('paramiko.SSHClient') as mock_client:
        instance = mock_client.return_value
        instance.connect.side_effect = paramiko.AuthenticationException("Auth failed")
        yield mock_client


@pytest.fixture
def mock_snmp_success():
    """Mock SNMP for successful connection."""
    with patch('devices.load_mib'), \
         patch('devices.SnmpManager') as mock_manager:
        instance = mock_manager.return_value
        instance.sysName = "test-device"
        yield mock_manager


@pytest.fixture
def mock_snmp_failure():
    """Mock SNMP for failed connection."""
    with patch('devices.load_mib'), \
         patch('devices.SnmpManager') as mock_manager:
        mock_manager.side_effect = Exception("SNMP timeout")
        yield mock_manager


@pytest.fixture
def mock_mysql_success():
    """Mock MySQL for successful connection."""
    with patch('MySQLdb.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("8.0.32",)
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        yield mock_connect


@pytest.fixture
def mock_mysql_failure():
    """Mock MySQL for failed connection."""
    import MySQLdb
    with patch('MySQLdb.connect') as mock_connect:
        mock_connect.side_effect = MySQLdb.Error("Connection refused")
        yield mock_connect


@pytest.fixture
def sample_csv_file(temp_dir: Path) -> Path:
    """Create a sample CSV file for testing."""
    csv_file = temp_dir / "devices.csv"
    csv_file.write_text(
        "host,ip,snmp_community,mysql_user,mysql_password\n"
        "192.168.1.1,192.168.1.1,public,,\n"
        "192.168.1.2,192.168.1.2,private,admin,secret\n"
    )
    return csv_file
