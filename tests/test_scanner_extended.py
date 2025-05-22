"""Extended tests for the NmapDeviceScanner class to improve coverage."""

from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

from paramiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
import pymysql
import pytest

from network_discovery.domain.device import Device
from network_discovery.infrastructure.scanner import NmapDeviceScanner


@pytest.fixture
def scanner():
    """Return a scanner instance."""
    return NmapDeviceScanner()


@pytest.fixture
def device():
    """Return a device instance."""
    return Device(id=1, host="example.com", ip="192.168.1.1")


class TestNmapDeviceScannerExtended:
    """Extended tests for the NmapDeviceScanner class."""

    @pytest.mark.asyncio
    async def test_check_ssh_authentication_error(self, scanner, device):
        """Test that SSH authentication errors are handled."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")

        # Mock the is_port_open method to return True and empty errors list
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Mock the SSHClient
        with patch("paramiko.SSHClient") as mock_ssh_client:
            # Mock the connect method to raise an AuthenticationException
            mock_instance = mock_ssh_client.return_value
            mock_instance.connect.side_effect = AuthenticationException(
                "Authentication failed"
            )

            # Check SSH
            result, errors = await scanner.check_ssh(test_device)

            # Check that the result is False
            assert not result

            # Check for the error message (partial match)
            assert any("Authentication failed" in error for error in errors)

    @pytest.mark.asyncio
    async def test_check_ssh_protocol_error(self, scanner, device):
        """Test that SSH protocol errors are handled."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")

        # Mock the is_port_open method to return True and empty errors list
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Mock the SSHClient
        with patch("paramiko.SSHClient") as mock_ssh_client:
            # Mock the connect method to raise an SSHException
            mock_instance = mock_ssh_client.return_value
            mock_instance.connect.side_effect = SSHException("Protocol error")

            # Check SSH
            result, errors = await scanner.check_ssh(test_device)

            # Check that the result is False
            assert not result

            # Check for the error message (partial match)
            assert any("Protocol error" in error for error in errors)

    @pytest.mark.asyncio
    async def test_check_ssh_timeout_error(self, scanner, device):
        """Test that SSH timeout errors are handled."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")

        # Mock the is_port_open method to return True and empty errors list
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Mock the SSHClient
        with patch("paramiko.SSHClient") as mock_ssh_client:
            # Mock the connect method to raise a TimeoutError
            mock_instance = mock_ssh_client.return_value
            mock_instance.connect.side_effect = TimeoutError(
                "Connection timed out"
            )

            # Check SSH
            result, errors = await scanner.check_ssh(test_device)

            # Check that the result is False
            assert not result

            # Check for the error message (partial match)
            assert any("Connection timeout" in error for error in errors)

    @pytest.mark.asyncio
    async def test_check_ssh_connection_refused_error(self, scanner, device):
        """Test that SSH connection refused errors are handled."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")

        # Mock the is_port_open method to return True and empty errors list
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Mock the SSHClient
        with patch("paramiko.SSHClient") as mock_ssh_client:
            # Mock the connect method to raise a ConnectionRefusedError
            mock_instance = mock_ssh_client.return_value
            mock_instance.connect.side_effect = ConnectionRefusedError(
                "Connection refused"
            )

            # Check SSH
            result, errors = await scanner.check_ssh(test_device)

            # Check that the result is False
            assert not result

            # Check for the error message (partial match)
            assert any("Connection refused" in error for error in errors)

    @pytest.mark.asyncio
    async def test_check_ssh_command_execution_error(self, scanner, device):
        """Test that SSH command execution errors are handled."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")

        # Mock the is_port_open method to return True and empty errors list
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Mock the SSHClient
        with patch("paramiko.SSHClient") as mock_ssh_client:
            # Mock the connect method
            mock_instance = mock_ssh_client.return_value
            # Mock the exec_command method to raise an exception
            mock_instance.exec_command.side_effect = Exception(
                "Command execution error"
            )

            # Check SSH
            result, errors = await scanner.check_ssh(test_device)

            # Check that the result is False
            assert not result

            # Check for the error message (partial match)
            assert any("Command execution error" in error for error in errors)

    @pytest.mark.asyncio
    async def test_check_snmp_mib_loading_error(self, scanner, device):
        """Test that SNMP MIB loading errors are handled."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")

        # Mock the is_port_open method to return True and empty errors list
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Mock the snimpy_load function
        with (
            patch(
                "network_discovery.infrastructure.scanner.SNMP_AVAILABLE", True
            ),
            patch(
                "network_discovery.infrastructure.scanner.snimpy_load"
            ) as mock_load,
        ):
            # Mock the load function to raise an exception
            mock_load.side_effect = Exception("Failed to load MIB")

            # Check SNMP
            result, errors = await scanner.check_snmp(test_device)

            # Check that the result is False
            assert not result

            # Check for the error message (partial match)
            assert any("Failed to load MIB" in error for error in errors)

    @pytest.mark.asyncio
    async def test_check_mysql_authentication_error(self, scanner, device):
        """Test that MySQL authentication errors are handled."""
        # Create a fresh device for this test
        test_device = Device(
            id=1,
            host="example.com",
            ip="192.168.1.1",
            mysql_user="user",
            mysql_password="pass",
        )

        # Mock the is_port_open method to return True and empty errors list
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Mock pymysql.connect
        with (
            patch(
                "network_discovery.infrastructure.scanner.MYSQL_AVAILABLE", True
            ),
            patch("pymysql.connect") as mock_connect,
        ):
            # Mock connect to raise an OperationalError
            # with error code 1045 (Access denied)
            error = pymysql.err.OperationalError(1045, "Access denied")
            mock_connect.side_effect = error

            # Check MySQL
            result, errors = await scanner.check_mysql(test_device)

            # Check that the result is False
            assert not result

            # Check for the error message (partial match)
            assert any("Authentication failed" in error for error in errors)

    @pytest.mark.asyncio
    async def test_check_mysql_connection_error(self, scanner, device):
        """Test that MySQL connection errors are handled."""
        # Create a fresh device for this test
        test_device = Device(
            id=1,
            host="example.com",
            ip="192.168.1.1",
            mysql_user="user",
            mysql_password="pass",
        )

        # Mock the is_port_open method to return True and empty errors list
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Mock pymysql.connect
        with (
            patch(
                "network_discovery.infrastructure.scanner.MYSQL_AVAILABLE", True
            ),
            patch("pymysql.connect") as mock_connect,
        ):
            # Mock connect to raise an OperationalError
            # with error code 2003 (Can't connect)
            error = pymysql.err.OperationalError(2003, "Can't connect")
            mock_connect.side_effect = error

            # Check MySQL
            result, errors = await scanner.check_mysql(test_device)

            # Check that the result is False
            assert not result

            # Check for the error message (partial match)
            assert any("Connection failed" in error for error in errors)

    @pytest.mark.asyncio
    async def test_check_mysql_database_error(self, scanner, device):
        """Test that MySQL database errors are handled."""
        # Create a fresh device for this test
        test_device = Device(
            id=1,
            host="example.com",
            ip="192.168.1.1",
            mysql_user="user",
            mysql_password="pass",
        )

        # Mock the is_port_open method to return True and empty errors list
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Mock pymysql.connect
        with (
            patch(
                "network_discovery.infrastructure.scanner.MYSQL_AVAILABLE", True
            ),
            patch("pymysql.connect") as mock_connect,
        ):
            # Mock connect to raise an OperationalError
            # with error code 1049 (Unknown database)
            error = pymysql.err.OperationalError(1049, "Unknown database")
            mock_connect.side_effect = error

            # Check MySQL
            result, errors = await scanner.check_mysql(test_device)

            # Check that the result is False
            assert not result

            # Check for the error message (partial match)
            assert any("Database not found" in error for error in errors)

    @pytest.mark.asyncio
    async def test_check_mysql_query_error(self, scanner, device):
        """Test that MySQL query errors are handled."""
        # Create a fresh device for this test
        test_device = Device(
            id=1,
            host="example.com",
            ip="192.168.1.1",
            mysql_user="user",
            mysql_password="pass",
        )

        # Mock the is_port_open method to return True and empty errors list
        scanner.is_port_open = AsyncMock(return_value=(True, []))

        # Mock pymysql.connect and cursor
        with (
            patch(
                "network_discovery.infrastructure.scanner.MYSQL_AVAILABLE", True
            ),
            patch("pymysql.connect") as mock_connect,
        ):
            # Mock the connection and cursor
            mock_connection = MagicMock()
            mock_cursor = MagicMock()
            mock_connect.return_value = mock_connection
            mock_connection.cursor.return_value = mock_cursor

            # Mock execute to raise a ProgrammingError
            mock_cursor.execute.side_effect = pymysql.err.ProgrammingError(
                "Query error"
            )

            # Check MySQL
            result, errors = await scanner.check_mysql(test_device)

            # Check that the result is False
            assert not result

            # Check for the error message (partial match)
            assert any("Query error" in error for error in errors)
