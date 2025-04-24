"""Tests for the Device class."""

from network_discovery.domain.device import Device


class TestDevice:
    """Tests for the Device class."""

    def test_hash(self):
        """Test that a Device can be hashed and used in sets."""
        device1 = Device(id=1, host="example.com", ip="192.168.1.1")
        device2 = Device(id=1, host="example.com", ip="192.168.1.1")
        device3 = Device(id=2, host="example.com", ip="192.168.1.1")

        assert hash(device1) == hash(device2)
        assert hash(device1) != hash(device3)

        device_set = {device1, device2, device3}
        assert len(device_set) == 2

    # Error handling and validation tests
    def test_invalid_id_type(self):
        """Test that a Device with an invalid ID type raises an error."""
        import pytest
        with pytest.raises(ValueError):
            Device(id="not_an_int", host="example.com", ip="192.168.1.1")

    def test_empty_host(self):
        """Test that a Device with an empty hostname raises an error."""
        import pytest
        with pytest.raises(ValueError):
            Device(id=1, host="", ip="192.168.1.1")

    def test_empty_ip(self):
        """Test that a Device with an empty IP raises an error."""
        import pytest
        with pytest.raises(ValueError):
            Device(id=1, host="example.com", ip="")

    def test_invalid_ip_format(self):
        """Test that a Device with an invalid IP format raises an error."""
        import pytest
        with pytest.raises(ValueError):
            Device(id=1, host="example.com", ip="not_an_ip")

    def test_negative_id(self):
        """Test that a Device with a negative ID raises an error."""
        import pytest
        with pytest.raises(ValueError):
            Device(id=-1, host="example.com", ip="192.168.1.1")

    # Device state transition tests
    def test_set_alive_state(self):
        """Test that a Device's alive state can be toggled."""
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        assert not device.alive

        # Set to alive
        alive_device = device.replace(alive=True)
        assert alive_device.alive

        # Set back to not alive
        not_alive_device = alive_device.replace(alive=False)
        assert not not_alive_device.alive

    def test_service_state_transitions(self):
        """Test transitioning between service states."""
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        
        # All services initially off
        assert not device.ssh
        assert not device.snmp
        assert not device.mysql
        
        # Turn on SSH
        ssh_device = device.replace(ssh=True)
        assert ssh_device.ssh
        assert not ssh_device.snmp
        assert not ssh_device.mysql
        
        # Turn on SNMP
        snmp_device = ssh_device.replace(snmp=True)
        assert snmp_device.ssh
        assert snmp_device.snmp
        assert not snmp_device.mysql
        
        # Turn on MySQL
        all_services_device = snmp_device.replace(mysql=True)
        assert all_services_device.ssh
        assert all_services_device.snmp
        assert all_services_device.mysql
        
        # Reset all services
        reset_device = all_services_device.reset_services()
        assert not reset_device.ssh
        assert not reset_device.snmp
        assert not reset_device.mysql

    def test_error_state_transitions(self):
        """Test adding and clearing errors."""
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        assert device.errors == ()
        
        # Add first error
        device_with_error = device.add_error("Error 1")
        assert device_with_error.errors == ("Error 1",)
        
        # Add second error
        device_with_two_errors = device_with_error.add_error("Error 2")
        assert device_with_two_errors.errors == ("Error 1", "Error 2")
        
        # Clear errors
        cleared_device = device_with_two_errors.replace(errors=())
        assert cleared_device.errors == ()

    def test_scan_state_transitions(self):
        """Test changing the scanned state."""
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        assert not device.scanned
        
        # Mark as scanned
        scanned_device = device.replace(scanned=True)
        assert scanned_device.scanned
        
        # Mark as not scanned
        unscanned_device = scanned_device.replace(scanned=False)
        assert not unscanned_device.scanned

    # Property validation tests
    def test_ip_validation(self):
        """Test IP address validation."""
        # Valid IPv4 addresses
        valid_ips = ["192.168.1.1", "10.0.0.1", "172.16.0.1", "127.0.0.1"]
        for ip in valid_ips:
            device = Device(id=1, host="example.com", ip=ip)
            assert device.ip == ip
        
        # Valid IPv6 addresses (if supported)
        try:
            device = Device(id=1, host="example.com", ip="::1")
            assert device.ip == "::1"
            
            device = Device(id=1, host="example.com", ip="2001:db8::1")
            assert device.ip == "2001:db8::1"
        except ValueError:
            # If IPv6 is not supported, this test will pass
            pass

    def test_snmp_group_validation(self):
        """Test SNMP group validation."""
        import pytest
        
        # Valid SNMP groups
        valid_groups = ["public", "private", "community1"]
        for group in valid_groups:
            device = Device(id=1, host="example.com", ip="192.168.1.1", snmp_group=group)
            assert device.snmp_group == group
        
        # Invalid SNMP groups (too long)
        with pytest.raises(ValueError):
            Device(id=1, host="example.com", ip="192.168.1.1", 
                   snmp_group="a" * 256)  # Assuming max length is 255

    def test_complex_state_machine(self):
        """Test a complex sequence of state transitions."""
        # Start with a base device
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        
        # Step 1: Mark device as alive and turn on SSH
        device = device.replace(alive=True, ssh=True)
        assert device.alive
        assert device.ssh
        
        # Step 2: Add some errors during scanning
        device = device.add_error("SSH connection timed out")
        assert "SSH connection timed out" in device.errors
        
        # Step 3: Turn on SNMP
        device = device.replace(snmp=True)
        assert device.snmp
        
        # Step 4: Add another error
        device = device.add_error("SNMP community string incorrect")
        assert len(device.errors) == 2
        
        # Step 5: Mark device as scanned
        device = device.replace(scanned=True)
        assert device.scanned
        
        # Step 6: Change hostname
        device = device.replace(host="new.example.com")
        assert device.host == "new.example.com"
        
        # Step 7: Reset services
        device = device.reset_services()
        assert not device.ssh
        assert not device.snmp
        assert not device.mysql
        assert device.uname == "unknown"
        
        # Step 8: Turn device offline
        device = device.replace(alive=False)
        assert not device.alive
        
        # Verify the final state contains all accumulated errors
        assert len(device.errors) == 2
        assert "SSH connection timed out" in device.errors
        assert "SNMP community string incorrect" in device.errors

    def test_immutability(self):
        """Test that Device instances are actually immutable."""
        import pytest
        
        device = Device(id=1, host="example.com", ip="192.168.1.1", 
                        alive=True, ssh=True)
        
        # Attempt to modify attributes directly should fail
        with pytest.raises(AttributeError):
            device.alive = False
            
        with pytest.raises(AttributeError):
            device.host = "new.example.com"
            
        with pytest.raises(AttributeError):
            device.ssh = False
            
        # The device should remain unchanged
        assert device.alive
        assert device.host == "example.com"
        assert device.ssh
        assert device.mysql_user == ""
        assert device.mysql_password == ""
        assert device.uname == ""
        assert device.errors == ()
        assert not device.scanned

    def test_add_error(self):
        """Test that errors can be added to a Device."""
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        device = device.add_error("Test error")
        assert device.errors == ("Test error",)
        device = device.add_error("Another error")
        assert device.errors == ("Test error", "Another error")

    def test_reset_services(self):
        """Test that services can be reset."""
        device = Device(
            id=1,
            host="example.com",
            ip="192.168.1.1",
            ssh=True,
            snmp=True,
            mysql=True,
            uname="Linux",
        )
        device = device.reset_services()
        assert not device.ssh
        assert not device.snmp
        assert not device.mysql
        assert device.uname == "unknown"

    def test_to_dict(self):
        """Test that a Device can be converted to a dictionary."""
        device = Device(
            id=1,
            host="example.com",
            ip="192.168.1.1",
            snmp_group="private",
            alive=True,
            snmp=True,
            ssh=True,
            mysql=True,
            mysql_user="user",
            mysql_password="password",
            uname="Linux",
            errors=("Error 1", "Error 2"),
            scanned=True,
        )
        d = device.to_dict()
        assert d["id"] == 1
        assert d["host"] == "example.com"
        assert d["ip"] == "192.168.1.1"
        assert d["snmp_group"] == "private"
        assert d["alive"] is True
        assert d["snmp"] is True
        assert d["ssh"] is True
        assert d["mysql"] is True
        assert d["mysql_user"] == "user"
        assert d["mysql_password"] == "password"
        assert d["uname"] == "Linux"
        assert d["errors"] == ["Error 1", "Error 2"]
        assert d["scanned"] is True

    def test_from_dict(self):
        """Test that a Device can be created from a dictionary."""
        d = {
            "id": 1,
            "host": "example.com",
            "ip": "192.168.1.1",
            "snmp_group": "private",
            "alive": True,
            "snmp": True,
            "ssh": True,
            "mysql": True,
            "mysql_user": "user",
            "mysql_password": "password",
            "uname": "Linux",
            "errors": ["Error 1", "Error 2"],
            "scanned": True,
        }
        device = Device.from_dict(d)
        assert device.id == 1
        assert device.host == "example.com"
        assert device.ip == "192.168.1.1"
        assert device.snmp_group == "private"
        assert device.alive is True
        assert device.snmp is True
        assert device.ssh is True
        assert device.mysql is True
        assert device.mysql_user == "user"
        assert device.mysql_password == "password"
        assert device.uname == "Linux"
        assert device.errors == ("Error 1", "Error 2")
        assert device.scanned is True

    def test_status(self):
        """Test that a Device's status can be retrieved."""
        device = Device(
            id=1,
            host="example.com",
            ip="192.168.1.1",
            alive=True,
            ssh=True,
            snmp=False,
            mysql=True,
            errors=("Error 1", "Error 2"),
        )
        status = device.status()
        assert "example.com" in status
        assert "alive: True" in status
        assert "ssh: True" in status
        assert "snmp: False" in status
        assert "mysql: True" in status
        assert "Error 1, Error 2" in status

    def test_repr(self):
        """Test that a Device's string representation is correct."""
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        assert repr(device) == "example.com (192.168.1.1)"

    def test_str(self):
        """Test that a Device's string representation is its dict."""
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        assert str(device) == str(device.to_dict())

    def test_replace(self):
        """Test that a Device's fields can be replaced."""
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        new_device = device.replace(host="new.example.com", alive=True)
        assert new_device.id == 1
        assert new_device.host == "new.example.com"
        assert new_device.ip == "192.168.1.1"
        assert new_device.alive is True

    def test_hash(self):
        """Test that a Device can be hashed and used in sets."""
        device1 = Device(id=1, host="example.com", ip="192.168.1.1")
        device2 = Device(id=1, host="example.com", ip="192.168.1.1")
        device3 = Device(id=2, host="example.com", ip="192.168.1.1")

        assert hash(device1) == hash(device2)
        assert hash(device1) != hash(device3)

        device_set = {device1, device2, device3}
        assert len(device_set) == 2