"""Tests for the NmapDeviceScanner class."""

import asyncio
import pytest
from unittest.mock import patch, MagicMock, AsyncMock, call

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


class TestNmapDeviceScanner:
    """Tests for the NmapDeviceScanner class."""

    @pytest.mark.asyncio
    async def test_scan_device_alive(self, scanner, device):
        """Test that a device can be scanned when it's alive."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")
        
        # Mock the is_alive method to return True
        scanner.is_alive = AsyncMock(return_value=True)
        
        # Mock the service check methods
        scanner.check_ssh = AsyncMock(return_value=(True, []))
        scanner.check_snmp = AsyncMock(return_value=(False, ["SNMP error"]))
        scanner.check_mysql = AsyncMock(return_value=(True, []))

        # Scan the device
        await scanner.scan_device(test_device)

        # Check that the device was scanned
        assert test_device.scanned
        assert test_device.alive
        assert test_device.ssh
        assert not test_device.snmp
        assert test_device.mysql

        # Check that the methods were called
        scanner.is_alive.assert_called_once_with(test_device)
        scanner.check_ssh.assert_called_once_with(test_device)
        scanner.check_snmp.assert_called_once_with(test_device)
        scanner.check_mysql.assert_called_once_with(test_device)

    @pytest.mark.asyncio
    async def test_scan_device_not_alive(self, scanner, device):
        """Test that a device can be scanned when it's not alive."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")
        
        # Mock the is_alive method to return False
        scanner.is_alive = AsyncMock(return_value=False)
        
        # Mock the service check methods
        scanner.check_ssh = AsyncMock()
        scanner.check_snmp = AsyncMock()
        scanner.check_mysql = AsyncMock()

        # Scan the device
        await scanner.scan_device(test_device)

        # Check that the device was scanned
        assert test_device.scanned
        assert not test_device.alive
        assert not test_device.ssh
        assert not test_device.snmp
        assert not test_device.mysql
        
        # Check for the error message (partial match)
        assert any("Host is down" in error for error in test_device.errors)

        # Check that the methods were called
        scanner.is_alive.assert_called_once_with(test_device)
        scanner.check_ssh.assert_not_called()
        scanner.check_snmp.assert_not_called()
        scanner.check_mysql.assert_not_called()

    @pytest.mark.asyncio
    async def test_scan_device_exception(self, scanner, device):
        """Test that exceptions during scanning are handled."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")
        
        # Mock the is_alive method to raise an exception
        scanner.is_alive = AsyncMock(side_effect=Exception("Test exception"))

        # Scan the device
        await scanner.scan_device(test_device)

        # Check that the error was added (partial match)
        assert any("Test exception" in error for error in test_device.errors)

    @pytest.mark.asyncio
    async def test_is_alive(self, scanner, device):
        """Test that a device's alive status can be checked."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")
        
        # Mock the nmap.PortScanner class
        with patch("nmap.PortScanner") as mock_port_scanner:
            # Mock the scan method
            mock_scanner = MagicMock()
            mock_port_scanner.return_value = mock_scanner
            
            # Mock the all_hosts method to return the device's IP
            mock_scanner.all_hosts.return_value = [str(test_device.ip)]
            
            # Mock the state method to return 'up'
            mock_scanner.__getitem__.return_value.state.return_value = 'up'

            # Check if the device is alive
            result = await scanner.is_alive(test_device)

            # Check that the result is True
            assert result
            
            # Check that the methods were called
            mock_scanner.scan.assert_called_once_with(hosts=str(test_device.ip), arguments='-sn')
            mock_scanner.all_hosts.assert_called_once()
            mock_scanner.__getitem__.assert_called_once_with(str(test_device.ip))
            mock_scanner.__getitem__.return_value.state.assert_called_once()

    @pytest.mark.asyncio
    async def test_is_alive_not_up(self, scanner, device):
        """Test that a device's alive status can be checked when it's not up."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")
        
        # Mock the nmap.PortScanner class
        with patch("nmap.PortScanner") as mock_port_scanner:
            # Mock the scan method
            mock_scanner = MagicMock()
            mock_port_scanner.return_value = mock_scanner
            
            # Mock the all_hosts method to return the device's IP
            mock_scanner.all_hosts.return_value = [str(test_device.ip)]
            
            # Mock the state method to return 'down'
            mock_scanner.__getitem__.return_value.state.return_value = 'down'

            # Check if the device is alive
            result = await scanner.is_alive(test_device)

            # Check that the result is False
            assert not result

    @pytest.mark.asyncio
    async def test_is_alive_not_in_hosts(self, scanner, device):
        """Test that a device's alive status can be checked when it's not in the hosts list."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")
        
        # Mock the nmap.PortScanner class
        with patch("nmap.PortScanner") as mock_port_scanner:
            # Mock the scan method
            mock_scanner = MagicMock()
            mock_port_scanner.return_value = mock_scanner
            
            # Mock the all_hosts method to return an empty list
            mock_scanner.all_hosts.return_value = []

            # Check if the device is alive
            result = await scanner.is_alive(test_device)

            # Check that the result is False
            assert not result

    @pytest.mark.asyncio
    async def test_is_alive_exception(self, scanner, device):
        """Test that exceptions during alive checking are handled."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")
        
        # Mock the nmap.PortScanner class
        with patch("nmap.PortScanner") as mock_port_scanner:
            # Mock the scan method to raise an exception
            mock_scanner = MagicMock()
            mock_port_scanner.return_value = mock_scanner
            mock_scanner.scan.side_effect = Exception("Test exception")

            # Check if the device is alive
            result = await scanner.is_alive(test_device)

            # Check that the result is False
            assert not result
            
            # Check for the error message (partial match)
            assert any("Test exception" in error for error in test_device.errors)

    @pytest.mark.asyncio
    async def test_is_port_open(self, scanner, device):
        """Test that a port's open status can be checked."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")
        
        # Mock the nmap.PortScanner class
        with patch("nmap.PortScanner") as mock_port_scanner:
            # Mock the scan method
            mock_scanner = MagicMock()
            mock_port_scanner.return_value = mock_scanner
            
            # Mock the all_hosts method to return the device's IP
            mock_scanner.all_hosts.return_value = [str(test_device.ip)]
            
            # Mock the __getitem__ method to return a dictionary with the port
            mock_scanner.__getitem__.return_value = {
                'tcp': {
                    22: {
                        'state': 'open'
                    }
                }
            }

            # Check if the port is open
            result, errors = await scanner.is_port_open(test_device, 22)

            # Check that the result is True and errors is empty
            assert result
            assert errors == []
            
            # Check that the methods were called with the correct arguments
            mock_scanner.scan.assert_called_once()
            args, kwargs = mock_scanner.scan.call_args
            assert kwargs.get('hosts') == str(test_device.ip)
            assert '-p 22' in kwargs.get('arguments', '')
            
            mock_scanner.all_hosts.assert_called_once()
            mock_scanner.__getitem__.assert_called_once_with(str(test_device.ip))

    @pytest.mark.asyncio
    async def test_is_port_open_closed(self, scanner, device):
        """Test that a port's open status can be checked when it's closed."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")
        
        # Mock the nmap.PortScanner class
        with patch("nmap.PortScanner") as mock_port_scanner:
            # Mock the scan method
            mock_scanner = MagicMock()
            mock_port_scanner.return_value = mock_scanner
            
            # Mock the all_hosts method to return the device's IP
            mock_scanner.all_hosts.return_value = [str(test_device.ip)]
            
            # Mock the __getitem__ method to return a dictionary with the port
            mock_scanner.__getitem__.return_value = {
                'tcp': {
                    22: {
                        'state': 'closed'
                    }
                }
            }

            # Check if the port is open
            result, errors = await scanner.is_port_open(test_device, 22)

            # Check that the result is False and errors is empty
            assert not result
            assert errors == []

    @pytest.mark.asyncio
    async def test_check_ssh_port_closed(self, scanner, device):
        """Test that SSH can be checked when the port is closed."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")
        
        # Mock the is_port_open method to return False and empty errors list
        scanner.is_port_open = AsyncMock(return_value=(False, []))

        # Check SSH
        result, errors = await scanner.check_ssh(test_device)

        # Check that the result is False
        assert not result
        
        # Check for the error message (partial match)
        assert any("Port closed" in error for error in test_device.errors)
        assert any("Port closed" in error for error in errors)
        assert test_device.uname == "unknown"

    @pytest.mark.asyncio
    async def test_check_mysql_port_closed(self, scanner, device):
        """Test that MySQL can be checked when the port is closed."""
        # Create a fresh device for this test
        test_device = Device(id=1, host="example.com", ip="192.168.1.1")
        
        # Mock the is_port_open method to return False and empty errors list
        scanner.is_port_open = AsyncMock(return_value=(False, []))

        # Check MySQL
        result, errors = await scanner.check_mysql(test_device)

        # Check that the result is False
        assert not result
        
        # Check for the error message (partial match)
        assert any("Port closed" in error for error in test_device.errors)
        assert any("Port closed" in error for error in errors)

    @pytest.mark.asyncio
    async def test_check_mysql_no_user(self, scanner, device):
        """Test that MySQL can be checked when no user is provided."""
        # Create a fresh device for this test
        test_device = Device(
            id=1, 
            host="example.com", 
            ip="192.168.1.1",
            mysql_user=""
        )
        
        # Mock the is_port_open method to return True and empty errors list
        scanner.is_port_open = AsyncMock(return_value=(True, []))
        
        # Mock the environment variable to be empty
        with patch("os.getenv", return_value=""):
            # Check MySQL
            result, errors = await scanner.check_mysql(test_device)

            # Check that the result is False
            assert not result
            
            # Check for the error message (partial match)
            assert any("No MySQL user provided" in error for error in test_device.errors)
            assert any("No MySQL user provided" in error for error in errors)
