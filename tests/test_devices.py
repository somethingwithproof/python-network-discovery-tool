"""
Tests for the devices module.
"""

from __future__ import annotations

import subprocess
from unittest.mock import MagicMock, patch

import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from devices import (
    Device,
    ScanConfig,
    ScanResult,
    ScanType,
    ValidationError,
    validate_host,
)


class TestValidateHost:
    """Tests for the validate_host function."""

    def test_valid_ipv4(self):
        """Test validation of valid IPv4 addresses."""
        assert validate_host("192.168.1.1") == "192.168.1.1"
        assert validate_host("10.0.0.1") == "10.0.0.1"
        assert validate_host("127.0.0.1") == "127.0.0.1"

    def test_valid_ipv6(self):
        """Test validation of valid IPv6 addresses."""
        assert validate_host("::1") == "::1"
        assert validate_host("fe80::1") == "fe80::1"

    def test_valid_hostname(self):
        """Test validation of valid hostnames."""
        assert validate_host("server") == "server"
        assert validate_host("server.example.com") == "server.example.com"
        assert validate_host("my-server-01") == "my-server-01"

    def test_invalid_none(self):
        """Test that None raises ValidationError."""
        with pytest.raises(ValidationError, match="cannot be None"):
            validate_host(None)

    def test_invalid_empty(self):
        """Test that empty string raises ValidationError."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_host("")
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_host("   ")

    def test_invalid_shell_metacharacters(self):
        """Test that shell metacharacters are rejected."""
        dangerous_inputs = [
            "192.168.1.1; rm -rf /",
            "192.168.1.1 | cat /etc/passwd",
            "$(whoami)",
            "`id`",
            "host&",
            "host\ninjected",
        ]
        for dangerous_input in dangerous_inputs:
            with pytest.raises(ValidationError, match="invalid characters"):
                validate_host(dangerous_input)

    def test_strips_whitespace(self):
        """Test that whitespace is stripped."""
        assert validate_host("  192.168.1.1  ") == "192.168.1.1"


class TestScanConfig:
    """Tests for the ScanConfig dataclass."""

    def test_default_values(self):
        """Test default configuration values."""
        config = ScanConfig()
        assert config.ssh_timeout == 3
        assert config.ping_timeout == 20
        assert config.ping_count == 1
        assert config.snmp_timeout == 2
        assert config.snmp_version == 2
        assert config.snmp_default_community == "public"

    def test_custom_values(self):
        """Test custom configuration values."""
        config = ScanConfig(
            ssh_user="admin",
            ssh_timeout=5,
            ping_timeout=10,
        )
        assert config.ssh_user == "admin"
        assert config.ssh_timeout == 5
        assert config.ping_timeout == 10

    def test_ssh_policy_strict(self):
        """Test that strict host key policy returns RejectPolicy."""
        import paramiko
        config = ScanConfig(ssh_strict_host_key=True)
        policy = config.ssh_policy
        assert isinstance(policy, paramiko.RejectPolicy)

    def test_ssh_policy_non_strict(self):
        """Test that non-strict host key policy returns WarningPolicy."""
        import paramiko
        config = ScanConfig(ssh_strict_host_key=False)
        policy = config.ssh_policy
        assert isinstance(policy, paramiko.WarningPolicy)


class TestDevice:
    """Tests for the Device dataclass."""

    def test_creation_valid(self, sample_device: Device):
        """Test creating a valid device."""
        assert sample_device.id == 1
        assert sample_device.host == "192.168.1.1"
        assert sample_device.ip == "192.168.1.1"
        assert sample_device.snmp_community == "public"
        assert sample_device.alive is False
        assert sample_device.scanned is False

    def test_creation_with_hostname(self):
        """Test creating device with hostname."""
        device = Device(id=1, host="server.example.com", ip="10.0.0.1")
        assert device.host == "server.example.com"
        assert device.ip == "10.0.0.1"

    def test_creation_invalid_host(self):
        """Test that invalid host raises ValidationError."""
        with pytest.raises(ValidationError):
            Device(id=1, host="", ip="192.168.1.1")

    def test_mysql_password_property(self, sample_device_with_mysql: Device):
        """Test MySQL password getter/setter."""
        assert sample_device_with_mysql.mysql_password == "secret123"
        sample_device_with_mysql.mysql_password = "newpassword"
        assert sample_device_with_mysql.mysql_password == "newpassword"

    def test_add_error(self, sample_device: Device):
        """Test adding errors to device."""
        sample_device.add_error("Test error 1")
        sample_device.add_error("Test error 2")
        assert len(sample_device.errors) == 2
        assert "Test error 1" in sample_device.errors
        assert "Test error 2" in sample_device.errors

    def test_to_dict_masks_credentials(self, sample_device_with_mysql: Device):
        """Test that to_dict masks credentials by default."""
        data = sample_device_with_mysql.to_dict()
        assert data["mysql_password"] == "***"
        assert data["snmp_community"] == "***"

    def test_to_dict_exposes_credentials(self, sample_device_with_mysql: Device):
        """Test that to_dict can expose credentials."""
        data = sample_device_with_mysql.to_dict(mask_credentials=False)
        assert data["mysql_password"] == "secret123"
        assert data["snmp_community"] == "private"

    def test_from_dict(self):
        """Test creating device from dictionary."""
        data = {
            "id": 5,
            "host": "192.168.1.5",
            "ip": "192.168.1.5",
            "snmp_community": "secret",
            "alive": True,
            "ssh": True,
            "snmp": False,
            "mysql": False,
            "errors": ["error1"],
            "uname": "Linux test",
            "scanned": True,
        }
        device = Device.from_dict(data)
        assert device.id == 5
        assert device.host == "192.168.1.5"
        assert device.alive is True
        assert device.ssh is True
        assert device.scanned is True

    def test_repr(self, sample_device: Device):
        """Test device string representation."""
        repr_str = repr(sample_device)
        assert "Device" in repr_str
        assert "192.168.1.1" in repr_str

    def test_str_not_scanned(self, sample_device: Device):
        """Test device string output when not scanned."""
        str_output = str(sample_device)
        assert "not scanned" in str_output

    def test_str_scanned(self, sample_device: Device):
        """Test device string output when scanned."""
        sample_device.scanned = True
        sample_device.alive = True
        sample_device.ssh = True
        str_output = str(sample_device)
        assert "alive" in str_output
        assert "ssh" in str_output


class TestDeviceScanPing:
    """Tests for Device.scan_ping method."""

    def test_scan_ping_success(self, sample_device: Device, mock_subprocess_ping_success):
        """Test successful ping scan."""
        result = sample_device.scan_ping()
        assert result.scan_type == ScanType.PING
        assert result.success is True
        assert sample_device.alive is True

    def test_scan_ping_failure(self, sample_device: Device, mock_subprocess_ping_failure):
        """Test failed ping scan."""
        result = sample_device.scan_ping()
        assert result.scan_type == ScanType.PING
        assert result.success is False
        assert sample_device.alive is False
        assert len(sample_device.errors) > 0

    def test_scan_ping_timeout(self, sample_device: Device):
        """Test ping scan timeout."""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="ping", timeout=1)
            result = sample_device.scan_ping()
            assert result.success is False
            assert "Timeout" in result.error


class TestDeviceScanSSH:
    """Tests for Device.scan_ssh method."""

    def test_scan_ssh_success(self, sample_device: Device, mock_paramiko_success):
        """Test successful SSH scan."""
        result = sample_device.scan_ssh()
        assert result.scan_type == ScanType.SSH
        assert result.success is True
        assert sample_device.ssh is True
        assert "Linux" in sample_device.uname

    def test_scan_ssh_auth_failure(self, sample_device: Device, mock_paramiko_auth_failure):
        """Test SSH authentication failure."""
        result = sample_device.scan_ssh()
        assert result.scan_type == ScanType.SSH
        assert result.success is False
        assert sample_device.ssh is False


class TestDeviceScanSNMP:
    """Tests for Device.scan_snmp method."""

    def test_scan_snmp_success(self, sample_device: Device, mock_snmp_success):
        """Test successful SNMP scan."""
        result = sample_device.scan_snmp()
        assert result.scan_type == ScanType.SNMP
        assert result.success is True
        assert sample_device.snmp is True

    def test_scan_snmp_failure(self, sample_device: Device, mock_snmp_failure):
        """Test failed SNMP scan."""
        result = sample_device.scan_snmp()
        assert result.scan_type == ScanType.SNMP
        assert result.success is False
        assert sample_device.snmp is False


class TestDeviceScanMySQL:
    """Tests for Device.scan_mysql method."""

    def test_scan_mysql_no_credentials(self, sample_device: Device):
        """Test MySQL scan without credentials."""
        result = sample_device.scan_mysql()
        assert result.success is False
        assert "No MySQL credentials" in result.error

    def test_scan_mysql_success(self, sample_device_with_mysql: Device, mock_mysql_success):
        """Test successful MySQL scan."""
        result = sample_device_with_mysql.scan_mysql()
        assert result.scan_type == ScanType.MYSQL
        assert result.success is True
        assert sample_device_with_mysql.mysql is True
        assert result.data["version"] == "8.0.32"

    def test_scan_mysql_failure(self, sample_device_with_mysql: Device, mock_mysql_failure):
        """Test failed MySQL scan."""
        result = sample_device_with_mysql.scan_mysql()
        assert result.scan_type == ScanType.MYSQL
        assert result.success is False
        assert sample_device_with_mysql.mysql is False


class TestDeviceScanAll:
    """Tests for Device.scan_all method."""

    def test_scan_all_host_down(self, sample_device: Device, mock_subprocess_ping_failure):
        """Test scan_all when host is down (only ping runs)."""
        results = sample_device.scan_all()
        assert len(results) == 1  # Only ping
        assert results[0].scan_type == ScanType.PING
        assert sample_device.scanned is True

    def test_scan_all_host_up(
        self,
        sample_device: Device,
        mock_subprocess_ping_success,
        mock_paramiko_success,
        mock_snmp_success,
    ):
        """Test scan_all when host is up."""
        results = sample_device.scan_all()
        assert len(results) == 3  # Ping, SNMP, SSH
        assert sample_device.scanned is True
        scan_types = {r.scan_type for r in results}
        assert ScanType.PING in scan_types
        assert ScanType.SNMP in scan_types
        assert ScanType.SSH in scan_types


class TestScanResult:
    """Tests for the ScanResult dataclass."""

    def test_creation(self):
        """Test creating a ScanResult."""
        result = ScanResult(
            scan_type=ScanType.PING,
            success=True,
            data={"output": "PING success"},
        )
        assert result.scan_type == ScanType.PING
        assert result.success is True
        assert result.error is None
        assert result.data["output"] == "PING success"

    def test_creation_with_error(self):
        """Test creating a ScanResult with error."""
        result = ScanResult(
            scan_type=ScanType.SSH,
            success=False,
            error="Connection refused",
        )
        assert result.success is False
        assert result.error == "Connection refused"
