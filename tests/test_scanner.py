"""Tests for the NmapDeviceScanner class."""

import pytest
import gc
import nmap
from unittest.mock import patch, MagicMock, AsyncMock

from network_discovery.domain.device import Device
from network_discovery.infrastructure.scanner import NmapDeviceScanner


class MockPortScanner:
    """Mock implementation of nmap.PortScanner."""

    def __init__(self):
        self.scan_results = {}
        self.hosts = []
        self.last_hosts = None
        self.last_arguments = None

    def scan(self, hosts=None, arguments=None):
        self.last_hosts = hosts
        self.last_arguments = arguments
        return {}

    def all_hosts(self):
        return self.hosts

    def __getitem__(self, key):
        return self.scan_results.get(key, {})


@pytest.fixture
def mock_nmap(monkeypatch):
    """Mock the nmap module."""
    mock_scanner = MockPortScanner()
    monkeypatch.setattr(nmap, "PortScanner", lambda: mock_scanner)
    yield mock_scanner
    gc.collect()


@pytest.fixture
def scanner():
    return NmapDeviceScanner()


@pytest.fixture
def device():
    return Device(id=1, host="example.com", ip="192.168.1.1")


class TestNmapDeviceScanner:
    """Tests for NmapDeviceScanner."""

    @pytest.mark.asyncio
    async def test_check_mysql_no_env_user(self, scanner, device):
        scanner.is_port_open = AsyncMock(return_value=(True, []))
        with patch("os.getenv", return_value=""):
            result, errors = await scanner.check_mysql(device)
            assert not result
            assert any("No MySQL user provided" in err for err in errors)

    # Additional SSH tests
    @pytest.mark.asyncio
    async def test_check_ssh_success(self, scanner, device):
        """Test successful SSH connection."""
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        with patch("paramiko.SSHClient") as mock_ssh_client:
            mock_client = MagicMock()
            mock_ssh_client.return_value = mock_client

            # Mock successful connection and command execution
            mock_stdout = MagicMock()
            mock_stdout.read.return_value = b"Linux test 5.4.0-generic"
            mock_stderr = MagicMock()
            mock_stderr.read.return_value = b""
            mock_client.exec_command.return_value = (None, mock_stdout, mock_stderr)

            result, errors = await scanner.check_ssh(device)

            assert result is True
            assert len(errors) == 0
            mock_client.load_host_keys.assert_called_once()
            mock_client.connect.assert_called_once()
            mock_client.exec_command.assert_called_once_with("uname -a")
            mock_client.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_check_ssh_authentication_error(self, scanner, device):
        """Test SSH authentication error."""
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        with patch("paramiko.SSHClient") as mock_ssh_client:
            mock_client = MagicMock()
            mock_ssh_client.return_value = mock_client

            # Mock authentication error
            from paramiko.ssh_exception import AuthenticationException

            mock_client.connect.side_effect = AuthenticationException(
                "Authentication failed"
            )

            result, errors = await scanner.check_ssh(device)

            assert result is False
            assert len(errors) == 1
            assert "Authentication failed" in errors[0]
            mock_client.load_host_keys.assert_called_once()

    @pytest.mark.asyncio
    async def test_check_ssh_connection_timeout(self, scanner, device):
        """Test SSH connection timeout."""
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        with patch("paramiko.SSHClient") as mock_ssh_client:
            mock_client = MagicMock()
            mock_ssh_client.return_value = mock_client

            # Mock timeout error
            mock_client.connect.side_effect = TimeoutError("Connection timed out")

            result, errors = await scanner.check_ssh(device)

            assert result is False
            assert len(errors) == 1
            assert "Connection timeout" in errors[0]

    @pytest.mark.asyncio
    async def test_check_ssh_command_execution_error(self, scanner, device):
        """Test SSH command execution error."""
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        with patch("paramiko.SSHClient") as mock_ssh_client:
            mock_client = MagicMock()
            mock_ssh_client.return_value = mock_client

            # Mock successful connection but command execution error
            mock_client.exec_command.side_effect = Exception("Command execution failed")

            result, errors = await scanner.check_ssh(device)

            assert result is False
            assert len(errors) == 1
            assert "Command execution error" in errors[0]
            mock_client.close.assert_called_once()

    # Additional SNMP tests
    @pytest.mark.asyncio
    async def test_check_snmp_not_available(self, scanner, device):
        """Test SNMP check when snimpy is not available."""
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        with patch("network_discovery.infrastructure.scanner.SNMP_AVAILABLE", False):
            result, errors = await scanner.check_snmp(device)

            assert result is False
            assert len(errors) == 1
            assert "SNMP checks disabled" in errors[0]

    @pytest.mark.asyncio
    async def test_check_snmp_port_closed(self, scanner, device):
        """Test SNMP check when port 161 is closed."""
        scanner.is_port_open = AsyncMock(return_value=(False, ["Port 161 closed"]))

        result, errors = await scanner.check_snmp(device)

        assert result is False
        assert len(errors) == 1
        assert "Port 161 closed" in errors[0]

    @pytest.mark.asyncio
    async def test_check_snmp_success(self, scanner, device):
        """Test successful SNMP check."""
        # Only run this test if SNMP_AVAILABLE is True
        if not getattr(scanner, "SNMP_AVAILABLE", True):
            pytest.skip("SNMP not available")

        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Mock the SNMP functionality
        with patch(
            "network_discovery.infrastructure.scanner.SNMP_AVAILABLE", True
        ), patch(
            "network_discovery.infrastructure.scanner.snimpy_load"
        ) as mock_load, patch(
            "network_discovery.infrastructure.scanner.SnimpyManager"
        ) as mock_manager_cls:

            mock_manager = MagicMock()
            mock_manager_cls.return_value = mock_manager
            mock_manager.sysName = "Test Device"

            result, errors = await scanner.check_snmp(device)

            assert result is True
            assert len(errors) == 0
            mock_load.assert_called_once_with("SNMPv2-MIB")
            mock_manager_cls.assert_called_once()

    @pytest.mark.asyncio
    async def test_check_snmp_mib_load_error(self, scanner, device):
        """Test SNMP check with MIB loading error."""
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Mock the SNMP functionality with MIB loading error
        with patch(
            "network_discovery.infrastructure.scanner.SNMP_AVAILABLE", True
        ), patch("network_discovery.infrastructure.scanner.snimpy_load") as mock_load:

            mock_load.side_effect = Exception("Failed to load MIB")

            result, errors = await scanner.check_snmp(device)

            assert result is False
            assert len(errors) == 1
            assert "Failed to load MIB" in errors[0]

    @pytest.mark.asyncio
    async def test_check_snmp_query_error(self, scanner, device):
        """Test SNMP check with query error."""
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Mock the SNMP functionality with query error
        with patch(
            "network_discovery.infrastructure.scanner.SNMP_AVAILABLE", True
        ), patch(
            "network_discovery.infrastructure.scanner.snimpy_load"
        ), patch(
            "network_discovery.infrastructure.scanner.SnimpyManager"
        ) as mock_manager_cls:

            mock_manager = MagicMock()
            mock_manager_cls.return_value = mock_manager

            # Make accessing sysName raise an exception
            type(mock_manager).sysName = property(
                side_effect=Exception("Failed to query sysName")
            )

            result, errors = await scanner.check_snmp(device)

            assert result is False
            assert len(errors) == 1
            assert "Failed to query sysName" in errors[0]

    # Additional MySQL tests
    @pytest.mark.asyncio
    async def test_check_mysql_not_available(self, scanner, device):
        """Test MySQL check when pymysql is not available."""
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        with patch("network_discovery.infrastructure.scanner.MYSQL_AVAILABLE", False):
            result, errors = await scanner.check_mysql(device)

            assert result is False
            assert len(errors) == 1
            assert "MySQL support not available" in errors[0]

    @pytest.mark.asyncio
    async def test_check_mysql_success(self, scanner, device):
        """Test successful MySQL check."""
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Set MySQL credentials
        device = device.replace(mysql_user="testuser", mysql_password="testpass")

        # Mock the MySQL functionality
        with patch(
            "network_discovery.infrastructure.scanner.MYSQL_AVAILABLE", True
        ), patch(
            "network_discovery.infrastructure.scanner.pymysql.connect"
        ) as mock_connect:

            mock_connection = MagicMock()
            mock_connect.return_value = mock_connection
            mock_cursor = MagicMock()
            mock_connection.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = ("5.7.30",)

            result, errors = await scanner.check_mysql(device)

            assert result is True
            assert len(errors) == 0
            mock_connect.assert_called_once_with(
                host=device.host,
                user=device.mysql_user,
                password=device.mysql_password,
                database="mysql",
                connect_timeout=3,
            )
            mock_cursor.execute.assert_called_once_with("SELECT VERSION()")
            mock_connection.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_check_mysql_auth_error(self, scanner, device):
        """Test MySQL check with authentication error."""
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Set MySQL credentials
        device = device.replace(mysql_user="testuser", mysql_password="testpass")

        # Mock the MySQL functionality with auth error
        with patch(
            "network_discovery.infrastructure.scanner.MYSQL_AVAILABLE", True
        ), patch(
            "network_discovery.infrastructure.scanner.pymysql.connect"
        ) as mock_connect:

            from network_discovery.infrastructure.scanner import pymysql

            mock_connect.side_effect = pymysql.err.OperationalError(
                1045, "Access denied"
            )

            result, errors = await scanner.check_mysql(device)

            assert result is False
            assert len(errors) == 1
            assert "Authentication failed" in errors[0]

    @pytest.mark.asyncio
    async def test_check_mysql_connection_error(self, scanner, device):
        """Test MySQL check with connection error."""
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Set MySQL credentials
        device = device.replace(mysql_user="testuser", mysql_password="testpass")

        # Mock the MySQL functionality with connection error
        with patch(
            "network_discovery.infrastructure.scanner.MYSQL_AVAILABLE", True
        ), patch(
            "network_discovery.infrastructure.scanner.pymysql.connect"
        ) as mock_connect:

            from network_discovery.infrastructure.scanner import pymysql

            mock_connect.side_effect = pymysql.err.OperationalError(
                2003, "Can't connect"
            )

            result, errors = await scanner.check_mysql(device)

            assert result is False
            assert len(errors) == 1
            assert "Connection failed" in errors[0]

    @pytest.mark.asyncio
    async def test_check_mysql_query_error(self, scanner, device):
        """Test MySQL check with query error."""
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Set MySQL credentials
        device = device.replace(mysql_user="testuser", mysql_password="testpass")

        # Mock the MySQL functionality with query error
        with patch(
            "network_discovery.infrastructure.scanner.MYSQL_AVAILABLE", True
        ), patch(
            "network_discovery.infrastructure.scanner.pymysql.connect"
        ) as mock_connect:

            mock_connection = MagicMock()
            mock_connect.return_value = mock_connection
            mock_cursor = MagicMock()
            mock_connection.cursor.return_value = mock_cursor

            from network_discovery.infrastructure.scanner import pymysql

            mock_cursor.execute.side_effect = pymysql.err.ProgrammingError(
                "Query error"
            )

            result, errors = await scanner.check_mysql(device)

            assert result is False
            assert len(errors) == 1
            assert "Query error" in errors[0]
            mock_connection.close.assert_called_once()

    # Timeout and Error Handling Tests
    @pytest.mark.asyncio
    async def test_scan_device_with_exception(self, scanner, device, mock_nmap):
        """Test scan_device method with an exception."""
        mock_nmap.scan.side_effect = Exception("Nmap scan error")

        result = await scanner.scan_device(device)

        assert not result.alive
        assert result.scanned
        assert any("Exception: Nmap scan error" in err for err in result.errors)

    @pytest.mark.asyncio
    async def test_scan_device_with_service_check_errors(
        self, scanner, device, mock_nmap
    ):
        """Test scan_device method when service checks return errors."""
        mock_nmap.hosts = [str(device.ip)]

        class MockHostState:
            def state(self):
                return "up"

            def __getitem__(self, key):
                return (
                    {
                        22: {"state": "open"},
                        161: {"state": "open"},
                        3306: {"state": "open"},
                    }
                    if key == "tcp"
                    else {}
                )

        mock_nmap.scan_results[str(device.ip)] = MockHostState()

        # Configure service checks to return errors
        ssh_errors = ["SSH error: Connection refused"]
        snmp_errors = ["SNMP error: Timeout"]
        mysql_errors = ["MySQL error: Authentication failed"]

        scanner.check_ssh = AsyncMock(return_value=(False, ssh_errors))
        scanner.check_snmp = AsyncMock(return_value=(False, snmp_errors))
        scanner.check_mysql = AsyncMock(return_value=(False, mysql_errors))

        result = await scanner.scan_device(device)

        assert result.alive  # Device is up but services have errors
        assert result.scanned
        assert not result.ssh
        assert not result.snmp
        assert not result.mysql

        # Check if all service errors are included in the device errors
        for error in ssh_errors + snmp_errors + mysql_errors:
            assert error in result.errors

        def port_state(key):
            return (
                {22: {"state": "open"}, 161: {"state": "open"}, 3306: {"state": "open"}}
                if key == "tcp"
                else {}
            )

        mock_nmap.scan_results[str(device.ip)] = MockHostState()
        scanner.check_ssh = AsyncMock(return_value=(True, []))
        scanner.check_snmp = AsyncMock(return_value=(True, []))
        scanner.check_mysql = AsyncMock(return_value=(True, []))

        result = await scanner.scan_device(device)

        assert result.alive
        assert result.scanned
        assert not result.errors
        scanner.check_ssh.assert_called_once()
        scanner.check_snmp.assert_called_once()
        scanner.check_mysql.assert_called_once()

    @pytest.mark.asyncio
    async def test_scan_device_not_alive(self, scanner, device, mock_nmap):
        mock_nmap.hosts = [str(device.ip)]

        class MockHostState:
            def state(self):
                return "down"

        mock_nmap.scan_results[str(device.ip)] = MockHostState()
        scanner.check_ssh = AsyncMock()
        scanner.check_snmp = AsyncMock()
        scanner.check_mysql = AsyncMock()

        result = await scanner.scan_device(device)

        assert result.scanned
        assert not result.alive
        assert not result.ssh
        assert not result.snmp
        assert not result.mysql
        assert any("Host is down" in err for err in result.errors)
        scanner.check_ssh.assert_not_called()
        scanner.check_snmp.assert_not_called()
        scanner.check_mysql.assert_not_called()

    @pytest.mark.asyncio
    async def test_is_alive(self, scanner, device, mock_nmap):
        mock_nmap.hosts = [str(device.ip)]

        class MockHostState:
            def state(self):
                return "up"

        mock_nmap.scan_results[str(device.ip)] = MockHostState()
        result = await scanner.is_alive(device)
        assert result
        assert mock_nmap.last_hosts == str(device.ip)
        assert mock_nmap.last_arguments == "-sn"

    @pytest.mark.asyncio
    async def test_is_alive_not_up(self, scanner, device):
        with patch("nmap.PortScanner") as mock_port_scanner:
            mock_scanner = MagicMock()
            mock_scanner.all_hosts.return_value = [str(device.ip)]
            mock_scanner.__getitem__.return_value.state.return_value = "down"
            mock_port_scanner.return_value = mock_scanner

            result = await scanner.is_alive(device)
            assert not result

    @pytest.mark.asyncio
    async def test_is_alive_not_in_hosts(self, scanner, device):
        with patch("nmap.PortScanner") as mock_port_scanner:
            mock_scanner = MagicMock()
            mock_scanner.all_hosts.return_value = []
            mock_port_scanner.return_value = mock_scanner

            result = await scanner.is_alive(device)
            assert not result

    @pytest.mark.asyncio
    async def test_is_alive_exception(self, scanner, device):
        with patch("nmap.PortScanner") as mock_port_scanner:
            mock_scanner = MagicMock()
            mock_scanner.scan.side_effect = Exception("Test exception")
            mock_port_scanner.return_value = mock_scanner

            result = await scanner.is_alive(device)
            assert not result
            assert any("Test exception" in err for err in device.errors)

    @pytest.mark.asyncio
    async def test_is_port_open(self, scanner, device):
        with patch("nmap.PortScanner") as mock_port_scanner:
            mock_scanner = MagicMock()
            mock_scanner.all_hosts.return_value = [str(device.ip)]
            mock_scanner.__getitem__.return_value = {"tcp": {22: {"state": "open"}}}
            mock_port_scanner.return_value = mock_scanner

            result, errors = await scanner.is_port_open(device, 22)
            assert result
            assert errors == []

    @pytest.mark.asyncio
    async def test_is_port_open_closed(self, scanner, device):
        with patch("nmap.PortScanner") as mock_port_scanner:
            mock_scanner = MagicMock()
            mock_scanner.all_hosts.return_value = [str(device.ip)]
            mock_scanner.__getitem__.return_value = {"tcp": {22: {"state": "closed"}}}
            mock_port_scanner.return_value = mock_scanner

            result, errors = await scanner.is_port_open(device, 22)
            assert not result
            assert errors == []

    @pytest.mark.asyncio
    async def test_check_ssh_port_closed(self, scanner, device):
        scanner.is_port_open = AsyncMock(return_value=(False, []))
        result, errors = await scanner.check_ssh(device)
        assert not result
        assert any("Port closed" in err for err in errors)

    @pytest.mark.asyncio
    async def test_check_mysql_port_closed(self, scanner, device):
        scanner.is_port_open = AsyncMock(return_value=(False, []))
        result, errors = await scanner.check_mysql(device)
        assert not result
        assert any("Port closed" in err for err in errors)

    @pytest.mark.asyncio
    async def test_check_mysql_no_param_user(self, scanner, device):
        scanner.is_port_open = AsyncMock(return_value=(True, []))
        with patch("os.getenv", return_value=""):
            result, errors = await scanner.check_mysql(device)
            assert not result
            assert any("No MySQL user provided" in err for err in errors)
