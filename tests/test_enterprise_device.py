"""Tests for the EnterpriseDevice class."""

from datetime import datetime
from datetime import timedelta

from network_discovery.domain.device import Device
from network_discovery.enterprise.device import DeviceCategory
from network_discovery.enterprise.device import DeviceStatus
from network_discovery.enterprise.device import EnterpriseDevice


class TestEnterpriseDevice:
    """Tests for the EnterpriseDevice class."""

    def test_init(self):
        """Test that an EnterpriseDevice can be initialized with the required parameters."""
        base_device = Device(id=1, host="example.com", ip="192.168.1.1")
        device = EnterpriseDevice(device=base_device)
        assert device.id == 1
        assert device.host == "example.com"
        assert device.ip == "192.168.1.1"
        assert device.device.snmp_group == "public"
        assert not device.alive
        assert not device.snmp
        assert not device.ssh
        assert not device.mysql
        assert device.device.mysql_user == ""
        assert device.device.mysql_password == ""
        assert device.device.uname == ""
        assert device.errors == ()
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
        assert device.compliance_issues == ()
        assert device.tags == frozenset()
        assert device.custom_attributes == {}
        assert device.last_scan_time is None
        assert device.uptime is None
        assert device.services == {}

    def test_add_tag(self):
        """Test that tags can be added to an EnterpriseDevice."""
        base_device = Device(id=1, host="example.com", ip="192.168.1.1")
        device = EnterpriseDevice(device=base_device)
        device = device.add_tag("production")
        assert device.tags == frozenset({"production"})
        device = device.add_tag("web-server")
        assert device.tags == frozenset({"production", "web-server"})
        # Test adding a duplicate tag
        device = device.add_tag("production")
        assert device.tags == frozenset({"production", "web-server"})

    def test_remove_tag(self):
        """Test that tags can be removed from an EnterpriseDevice."""
        base_device = Device(id=1, host="example.com", ip="192.168.1.1")
        device = EnterpriseDevice(device=base_device)
        device = device.add_tag("production")
        device = device.add_tag("web-server")
        assert device.tags == frozenset({"production", "web-server"})
        device = device.remove_tag("production")
        assert device.tags == frozenset({"web-server"})
        # Test removing a non-existent tag (should not raise an error)
        device = device.remove_tag("non-existent")
        assert device.tags == frozenset({"web-server"})

    def test_custom_attributes(self):
        """Test that custom attributes can be set and retrieved."""
        base_device = Device(id=1, host="example.com", ip="192.168.1.1")
        device = EnterpriseDevice(device=base_device)
        device = device.set_custom_attribute("rack", "A1")
        device = device.set_custom_attribute("power_supply", "redundant")
        assert device.custom_attributes == {
            "rack": "A1",
            "power_supply": "redundant",
        }
        assert device.get_custom_attribute("rack") == "A1"
        assert device.get_custom_attribute("power_supply") == "redundant"
        # Test getting a non-existent attribute
        assert device.get_custom_attribute("non-existent") is None
        # Test getting a non-existent attribute with a default value
        assert (
            device.get_custom_attribute("non-existent", "default") == "default"
        )
        # Test overwriting an existing attribute
        device = device.set_custom_attribute("rack", "B2")
        assert device.get_custom_attribute("rack") == "B2"

    def test_services(self):
        """Test that services can be added and retrieved."""
        base_device = Device(id=1, host="example.com", ip="192.168.1.1")
        device = EnterpriseDevice(device=base_device)
        device = device.add_service("http")
        device = device.add_service("https")
        device = device.add_service("ftp", False)
        assert device.services == {"http": True, "https": True, "ftp": False}
        assert device.get_service_status("http") is True
        assert device.get_service_status("https") is True
        assert device.get_service_status("ftp") is False
        # Test getting a non-existent service
        assert device.get_service_status("non-existent") is None
        # Test overwriting an existing service
        device = device.add_service("http", False)
        assert device.get_service_status("http") is False

    def test_update_scan_time(self):
        """Test that the last scan time can be updated."""
        base_device = Device(id=1, host="example.com", ip="192.168.1.1")
        device = EnterpriseDevice(device=base_device)
        assert device.last_scan_time is None
        device = device.update_scan_time()
        assert device.last_scan_time is not None
        assert isinstance(device.last_scan_time, datetime)

    def test_days_since_patched(self):
        """Test that the days since patched can be calculated."""
        base_device = Device(id=1, host="example.com", ip="192.168.1.1")
        device = EnterpriseDevice(device=base_device)
        # Test with no patch date
        assert device.days_since_patched() is None
        # Test with a patch date
        device = device.replace(
            last_patched=datetime.now() - timedelta(days=10)
        )
        assert (
            device.days_since_patched() >= 9
        )  # Allow for some flexibility due to timing
        assert device.days_since_patched() <= 11

    def test_days_until_warranty_expiry(self):
        """Test that the days until warranty expiry can be calculated."""
        base_device = Device(id=1, host="example.com", ip="192.168.1.1")
        device = EnterpriseDevice(device=base_device)
        # Test with no warranty expiry date
        assert device.days_until_warranty_expiry() is None
        # Test with a future warranty expiry date
        device = device.replace(
            warranty_expiry=datetime.now() + timedelta(days=100)
        )
        days = device.days_until_warranty_expiry()
        assert days >= 99  # Allow for some flexibility due to timing
        assert days <= 101
        # Test with a past warranty expiry date
        device = device.replace(
            warranty_expiry=datetime.now() - timedelta(days=50)
        )
        days = device.days_until_warranty_expiry()
        assert days >= -51  # Allow for some flexibility due to timing
        assert days <= -49

    def test_to_dict(self):
        """Test that an EnterpriseDevice can be converted to a dictionary."""
        now = datetime.now()
        purchase_date = now - timedelta(days=365)
        warranty_expiry = now + timedelta(days=365)
        last_patched = now - timedelta(days=30)
        last_scan_time = now - timedelta(hours=1)

        base_device = Device(
            id=1, host="example.com", ip="192.168.1.1", alive=True
        )
        device = EnterpriseDevice(
            device=base_device,
            category=DeviceCategory.SERVER,
            status=DeviceStatus.ACTIVE,
            asset_id="123456",
            location="Data Center",
            owner="IT Department",
            purchase_date=purchase_date,
            warranty_expiry=warranty_expiry,
            last_patched=last_patched,
            os_version="Ubuntu 20.04",
            firmware_version="1.2.3",
            compliance=True,
            compliance_issues=("Issue 1", "Issue 2"),
            tags=frozenset({"production", "web-server"}),
            custom_attributes={"rack": "A1", "power_supply": "redundant"},
            last_scan_time=last_scan_time,
            uptime=timedelta(days=30),
            services={"http": True, "https": True},
        )

        device_dict = device.to_dict()

        # Check base device properties
        assert device_dict["id"] == 1
        assert device_dict["host"] == "example.com"
        assert device_dict["ip"] == "192.168.1.1"
        assert device_dict["alive"] is True

        # Check EnterpriseDevice-specific properties
        assert device_dict["category"] == DeviceCategory.SERVER.value
        assert device_dict["status"] == DeviceStatus.ACTIVE.value
        assert device_dict["asset_id"] == "123456"
        assert device_dict["location"] == "Data Center"
        assert device_dict["owner"] == "IT Department"
        assert "purchase_date" in device_dict
        assert "warranty_expiry" in device_dict
        assert "last_patched" in device_dict
        assert device_dict["os_version"] == "Ubuntu 20.04"
        assert device_dict["firmware_version"] == "1.2.3"
        assert device_dict["compliance"] is True
        assert isinstance(device_dict["compliance_issues"], list)
        assert "Issue 1" in device_dict["compliance_issues"]
        assert "Issue 2" in device_dict["compliance_issues"]
        assert isinstance(device_dict["tags"], list)
        assert "production" in device_dict["tags"]
        assert "web-server" in device_dict["tags"]
        assert device_dict["custom_attributes"] == {
            "rack": "A1",
            "power_supply": "redundant",
        }
        assert "last_scan_time" in device_dict
        assert "uptime" in device_dict
        assert device_dict["services"] == {"http": True, "https": True}

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
            "alive": True,
            "category": DeviceCategory.SERVER.value,
            "status": DeviceStatus.ACTIVE.value,
            "asset_id": "123456",
            "location": "Data Center",
            "owner": "IT Department",
            "purchase_date": purchase_date.isoformat(),
            "warranty_expiry": warranty_expiry.isoformat(),
            "last_patched": last_patched.isoformat(),
            "os_version": "Ubuntu 20.04",
            "firmware_version": "1.2.3",
            "compliance": True,
            "compliance_issues": ["Issue 1", "Issue 2"],
            "tags": ["production", "web-server"],
            "custom_attributes": {"rack": "A1", "power_supply": "redundant"},
            "last_scan_time": last_scan_time.isoformat(),
            "uptime": str(timedelta(days=30)),
            "services": {"http": True, "https": True},
        }

        device = EnterpriseDevice.from_dict(device_dict)

        # Check base device properties
        assert device.id == 1
        assert device.host == "example.com"
        assert device.ip == "192.168.1.1"
        assert device.alive is True

        # Check EnterpriseDevice-specific properties
        assert device.category == DeviceCategory.SERVER
        assert device.status == DeviceStatus.ACTIVE
        assert device.asset_id == "123456"
        assert device.location == "Data Center"
        assert device.owner == "IT Department"
        assert isinstance(device.purchase_date, datetime)
        assert isinstance(device.warranty_expiry, datetime)
        assert isinstance(device.last_patched, datetime)
        assert device.os_version == "Ubuntu 20.04"
        assert device.firmware_version == "1.2.3"
        assert device.compliance is True
        assert device.compliance_issues == ("Issue 1", "Issue 2")
        assert device.tags == frozenset({"production", "web-server"})
        assert device.custom_attributes == {
            "rack": "A1",
            "power_supply": "redundant",
        }
        assert isinstance(device.last_scan_time, datetime)
        assert isinstance(device.uptime, timedelta)
        assert device.services == {"http": True, "https": True}
