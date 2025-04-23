"""Tests for the EnterpriseDevice class."""

from datetime import datetime, timedelta

from network_discovery.enterprise.device import EnterpriseDevice, DeviceCategory, DeviceStatus


class TestEnterpriseDevice:
    """Tests for the EnterpriseDevice class."""

    def test_init(self):
        """Test that an EnterpriseDevice can be initialized with the required parameters."""
        device = EnterpriseDevice(id=1, host="example.com", ip="192.168.1.1")
        assert device.id == 1
        assert device.host == "example.com"
        assert device.ip == "192.168.1.1"
        assert device.snmp_group == "public"
        assert not device.alive
        assert not device.snmp
        assert not device.ssh
        assert not device.mysql
        assert device.mysql_user == ""
        assert device.mysql_password == ""
        assert device.uname == ""
        assert device.errors == []
        assert not device.scanned
        assert device.category == DeviceCategory.UNKNOWN
        assert device.status == DeviceStatus.UNKNOWN
        assert device.asset_id == ""
        assert device.location == ""
        assert device.owner == ""
        assert device.purchase_date is None
        assert device.warranty_expiry is None
        assert device.last_patched is None
        assert device.os_version == ""
        assert device.firmware_version == ""
        assert not device.compliance
        assert device.compliance_issues == []
        assert device.tags == set()
        assert device.custom_attributes == {}
        assert device.last_scan_time is None
        assert device.uptime is None
        assert device.services == {}

    def test_add_tag(self):
        """Test that tags can be added to an EnterpriseDevice."""
        device = EnterpriseDevice(id=1, host="example.com", ip="192.168.1.1")
        device.add_tag("production")
        assert device.tags == {"production"}
        device.add_tag("web-server")
        assert device.tags == {"production", "web-server"}
        # Test adding a duplicate tag
        device.add_tag("production")
        assert device.tags == {"production", "web-server"}

    def test_remove_tag(self):
        """Test that tags can be removed from an EnterpriseDevice."""
        device = EnterpriseDevice(id=1, host="example.com", ip="192.168.1.1")
        device.add_tag("production")
        device.add_tag("web-server")
        assert device.tags == {"production", "web-server"}
        device.remove_tag("production")
        assert device.tags == {"web-server"}
        # Test removing a non-existent tag (should not raise an error)
        device.remove_tag("non-existent")
        assert device.tags == {"web-server"}

    def test_custom_attributes(self):
        """Test that custom attributes can be set and retrieved."""
        device = EnterpriseDevice(id=1, host="example.com", ip="192.168.1.1")
        device.set_custom_attribute("rack", "A1")
        device.set_custom_attribute("power_supply", "redundant")
        assert device.custom_attributes == {"rack": "A1", "power_supply": "redundant"}
        assert device.get_custom_attribute("rack") == "A1"
        assert device.get_custom_attribute("power_supply") == "redundant"
        # Test getting a non-existent attribute
        assert device.get_custom_attribute("non-existent") is None
        # Test getting a non-existent attribute with a default value
        assert device.get_custom_attribute("non-existent", "default") == "default"
        # Test overwriting an existing attribute
        device.set_custom_attribute("rack", "B2")
        assert device.get_custom_attribute("rack") == "B2"

    def test_services(self):
        """Test that services can be added and retrieved."""
        device = EnterpriseDevice(id=1, host="example.com", ip="192.168.1.1")
        device.add_service("http")
        device.add_service("https")
        device.add_service("ftp", False)
        assert device.services == {"http": True, "https": True, "ftp": False}
        assert device.get_service_status("http") is True
        assert device.get_service_status("https") is True
        assert device.get_service_status("ftp") is False
        # Test getting a non-existent service
        assert device.get_service_status("non-existent") is None
        # Test overwriting an existing service
        device.add_service("http", False)
        assert device.get_service_status("http") is False

    def test_update_scan_time(self):
        """Test that the last scan time can be updated."""
        device = EnterpriseDevice(id=1, host="example.com", ip="192.168.1.1")
        assert device.last_scan_time is None
        device.update_scan_time()
        assert device.last_scan_time is not None
        assert isinstance(device.last_scan_time, datetime)

    def test_days_since_patched(self):
        """Test that the days since patched can be calculated."""
        device = EnterpriseDevice(id=1, host="example.com", ip="192.168.1.1")
        # Test with no patch date
        assert device.days_since_patched() is None
        # Test with a patch date
        device.last_patched = datetime.now() - timedelta(days=10)
        assert device.days_since_patched() == 10

    def test_days_until_warranty_expiry(self):
        """Test that the days until warranty expiry can be calculated."""
        device = EnterpriseDevice(id=1, host="example.com", ip="192.168.1.1")
        # Test with no warranty expiry date
        assert device.days_until_warranty_expiry() is None
        # Test with a future warranty expiry date
        device.warranty_expiry = datetime.now() + timedelta(days=100)
        assert device.days_until_warranty_expiry() == 100
        # Test with a past warranty expiry date
        device.warranty_expiry = datetime.now() - timedelta(days=50)
        assert device.days_until_warranty_expiry() == -50

    def test_to_dict(self):
        """Test that an EnterpriseDevice can be converted to a dictionary."""
        now = datetime.now()
        purchase_date = now - timedelta(days=365)
        warranty_expiry = now + timedelta(days=365)
        last_patched = now - timedelta(days=30)
        last_scan_time = now - timedelta(hours=1)

        device = EnterpriseDevice(
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
            errors=["Error 1", "Error 2"],
            scanned=True,
            category=DeviceCategory.SERVER,
            status=DeviceStatus.OPERATIONAL,
            asset_id="ASSET123",
            location="Data Center 1",
            owner="IT Department",
            purchase_date=purchase_date,
            warranty_expiry=warranty_expiry,
            last_patched=last_patched,
            os_version="Ubuntu 22.04",
            firmware_version="1.2.3",
            compliance=True,
            compliance_issues=[],
            tags={"production", "web-server"},
            custom_attributes={"rack": "A1", "power_supply": "redundant"},
            last_scan_time=last_scan_time,
            uptime=86400,
            services={"http": True, "https": True, "ftp": False},
        )

        device_dict = device.to_dict()
        
        # Check base Device attributes
        assert device_dict["id"] == 1
        assert device_dict["host"] == "example.com"
        assert device_dict["ip"] == "192.168.1.1"
        assert device_dict["snmp_group"] == "private"
        assert device_dict["alive"] is True
        assert device_dict["snmp"] is True
        assert device_dict["ssh"] is True
        assert device_dict["mysql"] is True
        assert device_dict["mysql_user"] == "user"
        assert device_dict["mysql_password"] == "password"
        assert device_dict["uname"] == "Linux"
        assert device_dict["errors"] == ["Error 1", "Error 2"]
        assert device_dict["scanned"] is True
        
        # Check EnterpriseDevice attributes
        assert device_dict["category"] == "SERVER"
        assert device_dict["status"] == "OPERATIONAL"
        assert device_dict["asset_id"] == "ASSET123"
        assert device_dict["location"] == "Data Center 1"
        assert device_dict["owner"] == "IT Department"
        assert device_dict["purchase_date"] == purchase_date.isoformat()
        assert device_dict["warranty_expiry"] == warranty_expiry.isoformat()
        assert device_dict["last_patched"] == last_patched.isoformat()
        assert device_dict["os_version"] == "Ubuntu 22.04"
        assert device_dict["firmware_version"] == "1.2.3"
        assert device_dict["compliance"] is True
        assert device_dict["compliance_issues"] == []
        assert sorted(device_dict["tags"]) == sorted(["production", "web-server"])
        assert device_dict["custom_attributes"] == {"rack": "A1", "power_supply": "redundant"}
        assert device_dict["last_scan_time"] == last_scan_time.isoformat()
        assert device_dict["uptime"] == 86400
        assert device_dict["services"] == {"http": True, "https": True, "ftp": False}

    def test_from_dict(self):
        """Test that an EnterpriseDevice can be created from a dictionary."""
        now = datetime.now()
        purchase_date = now - timedelta(days=365)
        warranty_expiry = now + timedelta(days=365)
        last_patched = now - timedelta(days=30)
        last_scan_time = now - timedelta(hours=1)

        device_dict = {
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
            "category": "SERVER",
            "status": "OPERATIONAL",
            "asset_id": "ASSET123",
            "location": "Data Center 1",
            "owner": "IT Department",
            "purchase_date": purchase_date.isoformat(),
            "warranty_expiry": warranty_expiry.isoformat(),
            "last_patched": last_patched.isoformat(),
            "os_version": "Ubuntu 22.04",
            "firmware_version": "1.2.3",
            "compliance": True,
            "compliance_issues": [],
            "tags": ["production", "web-server"],
            "custom_attributes": {"rack": "A1", "power_supply": "redundant"},
            "last_scan_time": last_scan_time.isoformat(),
            "uptime": 86400,
            "services": {"http": True, "https": True, "ftp": False},
        }

        device = EnterpriseDevice.from_dict(device_dict)
        
        # Check base Device attributes
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
        assert device.errors == ["Error 1", "Error 2"]
        assert device.scanned is True
        
        # Check EnterpriseDevice attributes
        assert device.category == DeviceCategory.SERVER
        assert device.status == DeviceStatus.OPERATIONAL
        assert device.asset_id == "ASSET123"
        assert device.location == "Data Center 1"
        assert device.owner == "IT Department"
        assert device.purchase_date.isoformat() == purchase_date.isoformat()
        assert device.warranty_expiry.isoformat() == warranty_expiry.isoformat()
        assert device.last_patched.isoformat() == last_patched.isoformat()
        assert device.os_version == "Ubuntu 22.04"
        assert device.firmware_version == "1.2.3"
        assert device.compliance is True
        assert device.compliance_issues == []
        assert device.tags == {"production", "web-server"}
        assert device.custom_attributes == {"rack": "A1", "power_supply": "redundant"}
        assert device.last_scan_time.isoformat() == last_scan_time.isoformat()
        assert device.uptime == 86400
        assert device.services == {"http": True, "https": True, "ftp": False}

    def test_from_dict_with_invalid_enum_values(self):
        """Test that an EnterpriseDevice can be created from a dictionary with invalid enum values."""
        device_dict = {
            "id": 1,
            "host": "example.com",
            "ip": "192.168.1.1",
            "category": "INVALID_CATEGORY",
            "status": "INVALID_STATUS",
        }

        device = EnterpriseDevice.from_dict(device_dict)
        assert device.category == DeviceCategory.UNKNOWN
        assert device.status == DeviceStatus.UNKNOWN

    def test_from_dict_with_missing_dates(self):
        """Test that an EnterpriseDevice can be created from a dictionary with missing dates."""
        device_dict = {
            "id": 1,
            "host": "example.com",
            "ip": "192.168.1.1",
        }

        device = EnterpriseDevice.from_dict(device_dict)
        assert device.purchase_date is None
        assert device.warranty_expiry is None
        assert device.last_patched is None
        assert device.last_scan_time is None

    def test_str(self):
        """Test that an EnterpriseDevice's string representation is correct."""
        device = EnterpriseDevice(
            id=1,
            host="example.com",
            ip="192.168.1.1",
            category=DeviceCategory.SERVER,
            status=DeviceStatus.OPERATIONAL,
        )
        assert str(device) == "example.com (192.168.1.1) - SERVER - OPERATIONAL"
