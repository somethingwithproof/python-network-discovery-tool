"""Tests for enterprise export functionality."""

import csv
from datetime import datetime
import json
import os
import tempfile
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch

import pytest
import yaml

from network_discovery.domain.device import Device
from network_discovery.enterprise.device import DeviceCategory
from network_discovery.enterprise.device import DeviceStatus
from network_discovery.enterprise.device import EnterpriseDevice
from network_discovery.enterprise.export import EnterpriseExporter


@pytest.fixture
def base_device():
    """Create a base Device instance."""
    return Device(
        id=1,
        host="device1.example.com",
        ip="192.168.1.100",
        snmp_group="public",
        alive=True,
        snmp=True,
        ssh=True,
        mysql=True,
        mysql_user="admin",
        mysql_password="password123",
        uname="Linux 5.4.0-generic",
        errors=("Test error",),
        scanned=True,
    )


@pytest.fixture
def enterprise_device(base_device):
    """Create an EnterpriseDevice instance."""
    device = EnterpriseDevice(
        device=base_device,
        category=DeviceCategory.SERVER,
        status=DeviceStatus.ACTIVE,
        asset_id="ASSET-001",
        location="Data Center 1",
        owner="IT Department",
        os_version="Ubuntu 20.04 LTS",
        firmware_version="2.1.3",
        compliance=True,
        last_scan_time=datetime(2025, 1, 1, 12, 0, 0),
        uptime=86400,  # 1 day in seconds
        tags=["production", "web-server"],
        custom_attributes={
            "maintenance_contract": "MAINT-123",
            "critical": True,
        },
    )
    return device


@pytest.fixture
def enterprise_devices(base_device):
    """Create a list of EnterpriseDevice instances."""
    devices = []

    # Create different types of devices
    categories = [
        DeviceCategory.SERVER,
        DeviceCategory.NETWORK,
        DeviceCategory.STORAGE,
        DeviceCategory.SECURITY,
    ]

    statuses = [
        DeviceStatus.ACTIVE,
        DeviceStatus.MAINTENANCE,
        DeviceStatus.PENDING_DECOMMISSION,
        DeviceStatus.DECOMMISSIONED,
    ]

    for i in range(4):
        # Create a base device
        base = Device(
            id=i + 1,
            host=f"device{i+1}.example.com",
            ip=f"192.168.1.{100+i}",
            snmp_group="public" if i % 2 == 0 else "private",
            alive=i != 3,  # All alive except the last one
            snmp=i % 2 == 0,
            ssh=i % 3 == 0,
            mysql=i % 4 == 0,
            mysql_user="admin" if i % 4 == 0 else "",
            mysql_password="password123" if i % 4 == 0 else "",
            uname=f"Linux {i+1}" if i != 3 else "",
            errors=(f"Error {i+1}",) if i == 3 else (),
            scanned=True,
        )

        # Create an enterprise device
        device = EnterpriseDevice(
            device=base,
            category=categories[i],
            status=statuses[i],
            asset_id=f"ASSET-00{i+1}",
            location=f"Location {i+1}",
            owner=f"Owner {i+1}",
            os_version=f"OS Version {i+1}" if i != 3 else "",
            firmware_version=f"Firmware {i+1}" if i != 3 else "",
            compliance=i != 3,
            last_scan_time=datetime(2025, 1, 1, 12, i, 0) if i != 3 else None,
            uptime=86400 * (i + 1) if i != 3 else None,
            tags=[f"tag-{i+1}", "enterprise"] if i != 3 else [],
            custom_attributes=(
                {"key1": f"value{i+1}", "key2": i + 1} if i != 3 else {}
            ),
        )

        devices.append(device)

    return devices


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture
def exporter(temp_dir):
    """Create an EnterpriseExporter instance."""
    return EnterpriseExporter(output_dir=temp_dir)


class TestEnterpriseExporter:
    """Tests for the EnterpriseExporter class."""

    def test_init(self, temp_dir):
        """Test initialization of EnterpriseExporter."""
        exporter = EnterpriseExporter(output_dir=temp_dir)
        assert exporter.output_dir == temp_dir

        # Test directory creation
        new_dir = os.path.join(temp_dir, "exports")
        exporter = EnterpriseExporter(output_dir=new_dir)
        assert os.path.exists(new_dir)

    def test_export_to_json(self, exporter, enterprise_devices):
        """Test exporting devices to JSON format."""
        output_path = exporter.export_to_json(enterprise_devices)

        # Verify the file exists
        assert os.path.exists(output_path)
        assert output_path.endswith(".json")

        # Verify file content
        with open(output_path, "r") as f:
            data = json.load(f)
            assert isinstance(data, list)
            assert len(data) == len(enterprise_devices)

            # Check content of first device
            first_device = data[0]
            assert first_device["id"] == 1
            assert first_device["host"] == "device1.example.com"
            assert first_device["category"] == "SERVER"
            assert first_device["status"] == "ACTIVE"
            assert first_device["asset_id"] == "ASSET-001"

            # Verify that custom attributes are included
            assert "custom_attributes" in first_device
            assert "key1" in first_device["custom_attributes"]

    def test_export_to_yaml(self, exporter, enterprise_devices):
        """Test exporting devices to YAML format."""
        output_path = exporter.export_to_yaml(enterprise_devices)

        # Verify the file exists
        assert os.path.exists(output_path)
        assert output_path.endswith(".yaml")

        # Verify file content
        with open(output_path, "r") as f:
            data = yaml.safe_load(f)
            assert isinstance(data, list)
            assert len(data) == len(enterprise_devices)

            # Check content of first device
            first_device = data[0]
            assert first_device["id"] == 1
            assert first_device["host"] == "device1.example.com"
            assert first_device["category"] == "SERVER"
            assert first_device["tags"] == ["tag-1", "enterprise"]

    def test_export_to_csv(self, exporter, enterprise_devices):
        """Test exporting devices to CSV format."""
        output_path = exporter.export_to_csv(enterprise_devices)

        # Verify the file exists
        assert os.path.exists(output_path)
        assert output_path.endswith(".csv")

        # Verify file content
        with open(output_path, "r", newline="") as f:
            reader = csv.reader(f)
            headers = next(reader)  # Get the headers

            # Verify headers
            assert "ID" in headers
            assert "Host" in headers
            assert "IP" in headers
            assert "Category" in headers
            assert "Status" in headers

            # Verify data
            rows = list(reader)
            assert len(rows) == len(enterprise_devices)

            # Check first row data
            first_row = rows[0]
            assert first_row[0] == "1"  # ID
            assert first_row[1] == "device1.example.com"  # Host
            assert first_row[2] == "192.168.1.100"  # IP
            assert first_row[7] == "SERVER"  # Category
            assert first_row[8] == "ACTIVE"  # Status
            assert "tag-1" in first_row[17]  # Tags

    def test_export_to_nagios(self, exporter, enterprise_devices):
        """Test exporting devices to Nagios configuration format."""
        output_path = exporter.export_to_nagios(enterprise_devices)

        # Verify the file exists
        assert os.path.exists(output_path)
        assert output_path.endswith(".cfg")

        # Read file content
        with open(output_path, "r") as f:
            content = f.read()

            # Check for Nagios host definitions
            assert "define host {" in content
            assert "    host_name              device1.example.com" in content
            assert "    address                192.168.1.100" in content

            # Check for service definitions
            assert "define service {" in content
            assert "    service_description    SSH" in content
            assert "    service_description    SNMP" in content

            # Verify that the decommissioned device is not included
            assert "device4.example.com" not in content

            # Verify that tags are included as hostgroups
            assert "    hostgroups             tag-1,enterprise" in content

    def test_export_to_zenoss(self, exporter, enterprise_devices):
        """Test exporting devices to Zenoss JSON format."""
        output_path = exporter.export_to_zenoss(enterprise_devices)

        # Verify the file exists
        assert os.path.exists(output_path)
        assert output_path.endswith(".json")

        # Verify file content
        with open(output_path, "r") as f:
            data = json.load(f)
            assert "devices" in data
            assert isinstance(data["devices"], list)

            # Only living devices should be included
            living_devices = [d for d in enterprise_devices if d.alive]
            assert len(data["devices"]) == len(living_devices)

            # Check first device
            first_device = data["devices"][0]
            assert first_device["deviceName"] == "device1.example.com"
            assert first_device["manageIp"] == "192.168.1.100"
            assert first_device["deviceClass"] == "/Devices/Server"
            assert first_device["snmpMonitor"] is True
            assert first_device["sshMonitor"] is True

            # Check for device properties
            assert "properties" in first_device
            assert first_device["properties"]["assetId"] == "ASSET-001"
            assert "key1" in first_device["properties"]

    def test_export_generic_method(self, exporter, enterprise_devices):
        """Test the generic export method with different formats."""
        # Test JSON format
        json_path = exporter.export(enterprise_devices, "json")
        assert os.path.exists(json_path)
        assert json_path.endswith(".json")

        # Test YAML format
        yaml_path = exporter.export(enterprise_devices, "yaml")
        assert os.path.exists(yaml_path)
        assert yaml_path.endswith(".yaml")

        # Test CSV format
        csv_path = exporter.export(enterprise_devices, "csv")
        assert os.path.exists(csv_path)
        assert csv_path.endswith(".csv")

        # Test Nagios format
        nagios_path = exporter.export(enterprise_devices, "nagios")
        assert os.path.exists(nagios_path)
        assert nagios_path.endswith(".cfg")

        # Test Zenoss format
        zenoss_path = exporter.export(enterprise_devices, "zenoss")
        assert os.path.exists(zenoss_path)
        assert zenoss_path.endswith(".json")

        # Test invalid format
        with pytest.raises(ValueError):
            exporter.export(enterprise_devices, "invalid_format")

    def test_custom_filename(self, exporter, enterprise_devices):
        """Test exporting with custom filenames."""
        # Test with custom filename
        custom_path = exporter.export_to_json(
            enterprise_devices, "custom_export.json"
        )
        assert os.path.exists(custom_path)
        assert os.path.basename(custom_path) == "custom_export.json"

        # Test with None filename (should generate default)
        default_path = exporter.export_to_json(enterprise_devices)
        assert os.path.exists(default_path)
        assert "devices_" in os.path.basename(default_path)
        assert default_path.endswith(".json")

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_json_export_error(
        self, mock_json_dump, mock_file, exporter, enterprise_devices
    ):
        """Test error handling during JSON export."""
        # Mock json.dump to raise an exception
        mock_json_dump.side_effect = IOError("Test IO error")

        # Attempt to export should raise the IOError
        with pytest.raises(IOError) as exc_info:
            exporter.export_to_json(enterprise_devices)

        assert "Test IO error" in str(exc_info.value)

    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.dump")
    def test_yaml_export_error(
        self, mock_yaml_dump, mock_file, exporter, enterprise_devices
    ):
        """Test error handling during YAML export."""
        # Mock yaml.dump to raise an exception
        mock_yaml_dump.side_effect = yaml.YAMLError("Test YAML error")

        # Attempt to export should raise the YAMLError
        with pytest.raises(yaml.YAMLError) as exc_info:
            exporter.export_to_yaml(enterprise_devices)

        assert "Test YAML error" in str(exc_info.value)

    def test_empty_device_list(self, exporter):
        """Test exporting an empty device list."""
        # Export should work with empty list
        json_path = exporter.export_to_json([])
        assert os.path.exists(json_path)

        # Verify empty list is exported
        with open(json_path, "r") as f:
            data = json.load(f)
            assert data == []


class TestEnterpriseExportIntegration:
    """Integration tests for the enterprise export functionality."""

    def test_integration_workflow(self, exporter, enterprise_devices, temp_dir):
        """Test a complete export workflow with multiple formats."""
        # Create a subdirectory for this test
        test_dir = os.path.join(temp_dir, "integration_test")
        os.makedirs(test_dir, exist_ok=True)
        exporter.output_dir = test_dir

        # Export all formats
        formats = ["json", "yaml", "csv", "nagios", "zenoss"]
        paths = {}


"""Tests for the EnterpriseExporter class."""

import json
import os
import shutil

import pytest
import yaml

from network_discovery.domain.device import Device
from network_discovery.enterprise.device import DeviceCategory
from network_discovery.enterprise.device import DeviceStatus
from network_discovery.enterprise.device import EnterpriseDevice
from network_discovery.enterprise.export import EnterpriseExporter


@pytest.fixture
def test_output_dir():
    """Create a temporary output directory for tests."""
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)
    yield output_dir
    # Clean up after tests
    shutil.rmtree(output_dir)


@pytest.fixture
def sample_devices():
    """Create a list of sample devices for testing."""
    base_device1 = Device(
        id=1,
        host="server1.example.com",
        ip="192.168.1.1",
        alive=True,
        ssh=True,
        snmp=True,
        mysql=False,
    )

    device1 = EnterpriseDevice(
        device=base_device1,
        category=DeviceCategory.SERVER,
        status=DeviceStatus.OPERATIONAL,
        asset_id="ASSET001",
        location="Data Center 1",
        owner="IT Department",
        os_version="Ubuntu 22.04",
        firmware_version="1.2.3",
        tags=frozenset({"production", "web-server"}),
        custom_attributes={"rack": "A1", "power_supply": "redundant"},
    )

    base_device2 = Device(
        id=2,
        host="router1.example.com",
        ip="192.168.1.254",
        alive=True,
        ssh=True,
        snmp=True,
        mysql=False,
    )

    device2 = EnterpriseDevice(
        device=base_device2,
        category=DeviceCategory.NETWORK,
        status=DeviceStatus.OPERATIONAL,
        asset_id="ASSET002",
        location="Data Center 1",
        owner="Network Team",
        os_version="IOS 15.2",
        firmware_version="2.1.0",
        tags=frozenset({"production", "network", "core"}),
        custom_attributes={"rack": "B3", "model": "Cisco 3850"},
    )

    base_device3 = Device(
        id=3,
        host="storage1.example.com",
        ip="192.168.1.10",
        alive=True,
        ssh=True,
        snmp=False,
        mysql=False,
    )

    device3 = EnterpriseDevice(
        device=base_device3,
        category=DeviceCategory.STORAGE,
        status=DeviceStatus.DEGRADED,
        asset_id="ASSET003",
        location="Data Center 2",
        owner="Storage Team",
        os_version="Storage OS 5.1",
        firmware_version="3.0.2",
        tags=frozenset({"production", "storage"}),
        custom_attributes={"rack": "C2", "capacity": "100TB"},
    )

    # A device that is not alive
    base_device4 = Device(
        id=4,
        host="offline.example.com",
        ip="192.168.1.20",
        alive=False,
    )

    device4 = EnterpriseDevice(
        device=base_device4,
        category=DeviceCategory.SERVER,
        status=DeviceStatus.CRITICAL,
        asset_id="ASSET004",
        location="Data Center 1",
        owner="IT Department",
    )

    return [device1, device2, device3, device4]


class TestEnterpriseExporter:
    """Tests for the EnterpriseExporter class."""

    def test_init(self, test_output_dir):
        """Test that an EnterpriseExporter can be initialized."""
        exporter = EnterpriseExporter(output_dir=test_output_dir)
        assert exporter.output_dir == test_output_dir
        assert os.path.exists(test_output_dir)

    def test_export_to_json(self, test_output_dir, sample_devices):
        """Test exporting devices to JSON format."""
        exporter = EnterpriseExporter(output_dir=test_output_dir)
        filename = "test_devices.json"
        output_path = exporter.export_to_json(sample_devices, filename)

        # Check that the file was created
        assert os.path.exists(output_path)
        assert output_path == os.path.join(test_output_dir, filename)

        # Check the file contents
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 4
        assert data[0]["id"] == 1
        assert data[0]["host"] == "server1.example.com"
        assert data[0]["category"] == "SERVER"
        assert data[1]["id"] == 2
        assert data[1]["host"] == "router1.example.com"
        assert data[1]["category"] == "NETWORK"
        assert data[2]["id"] == 3
        assert data[2]["host"] == "storage1.example.com"
        assert data[2]["category"] == "STORAGE"
        assert data[3]["id"] == 4
        assert data[3]["host"] == "offline.example.com"
        assert data[3]["alive"] is False

    def test_export_to_json_default_filename(
        self, test_output_dir, sample_devices
    ):
        """Test exporting devices to JSON format with a default filename."""
        exporter = EnterpriseExporter(output_dir=test_output_dir)
        output_path = exporter.export_to_json(sample_devices)

        # Check that the file was created with a timestamp in the name
        assert os.path.exists(output_path)
        assert "devices_" in output_path
        assert output_path.endswith(".json")

        # Check the file contents
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 4

    def test_export_to_yaml(self, test_output_dir, sample_devices):
        """Test exporting devices to YAML format."""
        exporter = EnterpriseExporter(output_dir=test_output_dir)
        filename = "test_devices.yaml"
        output_path = exporter.export_to_yaml(sample_devices, filename)

        # Check that the file was created
        assert os.path.exists(output_path)
        assert output_path == os.path.join(test_output_dir, filename)

        # Check the file contents
        with open(output_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert len(data) == 4
        assert data[0]["id"] == 1
        assert data[0]["host"] == "server1.example.com"
        assert data[0]["category"] == "SERVER"
        assert data[1]["id"] == 2
        assert data[1]["host"] == "router1.example.com"
        assert data[1]["category"] == "NETWORK"
        assert data[2]["id"] == 3
        assert data[2]["host"] == "storage1.example.com"
        assert data[2]["category"] == "STORAGE"
        assert data[3]["id"] == 4
        assert data[3]["host"] == "offline.example.com"
        assert data[3]["alive"] is False

    def test_export_to_yaml_default_filename(
        self, test_output_dir, sample_devices
    ):
        """Test exporting devices to YAML format with a default filename."""
        exporter = EnterpriseExporter(output_dir=test_output_dir)
        output_path = exporter.export_to_yaml(sample_devices)

        # Check that the file was created with a timestamp in the name
        assert os.path.exists(output_path)
        assert "devices_" in output_path
        assert output_path.endswith(".yaml")

        # Check the file contents
        with open(output_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert len(data) == 4

    def test_export_to_csv(self, test_output_dir, sample_devices):
        """Test exporting devices to CSV format."""
        exporter = EnterpriseExporter(output_dir=test_output_dir)
        filename = "test_devices.csv"
        output_path = exporter.export_to_csv(sample_devices, filename)

        # Check that the file was created
        assert os.path.exists(output_path)
        assert output_path == os.path.join(test_output_dir, filename)

        # Check the file contents
        with open(output_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Check header
        assert "ID,Host,IP,Alive,SSH,SNMP,MySQL" in lines[0]

        # Check data rows
        assert len(lines) == 5  # Header + 4 devices
        assert (
            "1,server1.example.com,192.168.1.1,True,True,True,False" in lines[1]
        )
        assert (
            "2,router1.example.com,192.168.1.254,True,True,True,False"
            in lines[2]
        )
        assert (
            "3,storage1.example.com,192.168.1.10,True,True,False,False"
            in lines[3]
        )
        assert (
            "4,offline.example.com,192.168.1.20,False,False,False,False"
            in lines[4]
        )

    def test_export_to_csv_default_filename(
        self, test_output_dir, sample_devices
    ):
        """Test exporting devices to CSV format with a default filename."""
        exporter = EnterpriseExporter(output_dir=test_output_dir)
        output_path = exporter.export_to_csv(sample_devices)

        # Check that the file was created with a timestamp in the name
        assert os.path.exists(output_path)
        assert "devices_" in output_path
        assert output_path.endswith(".csv")

        # Check the file contents
        with open(output_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) == 5  # Header + 4 devices

    def test_export_to_nagios(self, test_output_dir, sample_devices):
        """Test exporting devices to Nagios configuration format."""
        exporter = EnterpriseExporter(output_dir=test_output_dir)
        filename = "test_nagios.cfg"
        output_path = exporter.export_to_nagios(sample_devices, filename)

        # Check that the file was created
        assert os.path.exists(output_path)
        assert output_path == os.path.join(test_output_dir, filename)

        # Check the file contents
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Only alive devices should be included
        assert "server1.example.com" in content
        assert "router1.example.com" in content
        assert "storage1.example.com" in content
        assert "offline.example.com" not in content

        # Check host definitions
        assert "define host {" in content
        assert "host_name              server1.example.com" in content
        assert "address                192.168.1.1" in content

        # Check service definitions
        assert "define service {" in content
        assert "service_description    SSH" in content
        assert "service_description    SNMP" in content

        # Check custom attributes
        assert "_rack" in content
        assert "_power_supply" in content

        # Check tags as hostgroups
        assert "hostgroups" in content
        assert "production" in content
        assert "web-server" in content

        # Check notes
        assert "notes" in content
        assert "Asset ID: ASSET001" in content
        assert "Location: Data Center 1" in content
        assert "Owner: IT Department" in content

    def test_export_to_nagios_default_filename(
        self, test_output_dir, sample_devices
    ):
        """Test exporting devices to Nagios format with a default filename."""
        exporter = EnterpriseExporter(output_dir=test_output_dir)
        output_path = exporter.export_to_nagios(sample_devices)

        # Check that the file was created with a timestamp in the name
        assert os.path.exists(output_path)
        assert "nagios_devices_" in output_path
        assert output_path.endswith(".cfg")

        # Check the file contents
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Only alive devices should be included
        assert "server1.example.com" in content
        assert "router1.example.com" in content
        assert "storage1.example.com" in content
        assert "offline.example.com" not in content

    def test_export_to_zenoss(self, test_output_dir, sample_devices):
        """Test exporting devices to Zenoss JSON format."""
        exporter = EnterpriseExporter(output_dir=test_output_dir)
        filename = "test_zenoss.json"
        output_path = exporter.export_to_zenoss(sample_devices, filename)

        # Check that the file was created
        assert os.path.exists(output_path)
        assert output_path == os.path.join(test_output_dir, filename)

        # Check the file contents
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Only alive devices should be included
        assert len(data["devices"]) == 3

        # Check device data
        devices = {d["deviceName"]: d for d in data["devices"]}

        assert "server1.example.com" in devices.keys()
        assert (
            devices["server1.example.com"]["deviceClass"] == "/Devices/Server"
        )
        assert devices["server1.example.com"]["manageIp"] == "192.168.1.1"
        assert devices["server1.example.com"]["snmpMonitor"] is True
        assert devices["server1.example.com"]["sshMonitor"] is True
        assert "production" in devices["server1.example.com"]["systems"]
        assert "web-server" in devices["server1.example.com"]["systems"]
        assert devices["server1.example.com"]["location"] == "Data Center 1"
        assert (
            devices["server1.example.com"]["properties"]["assetId"]
            == "ASSET001"
        )
        assert (
            devices["server1.example.com"]["properties"]["owner"]
            == "IT Department"
        )
        assert (
            devices["server1.example.com"]["properties"]["osVersion"]
            == "Ubuntu 22.04"
        )
        assert (
            devices["server1.example.com"]["properties"]["firmwareVersion"]
            == "1.2.3"
        )
        assert devices["server1.example.com"]["properties"]["rack"] == "A1"
        assert (
            devices["server1.example.com"]["properties"]["power_supply"]
            == "redundant"
        )

        assert "router1.example.com" in devices.keys()
        assert (
            devices["router1.example.com"]["deviceClass"] == "/Devices/Network"
        )

        assert "storage1.example.com" in devices.keys()
        assert (
            devices["storage1.example.com"]["deviceClass"] == "/Devices/Storage"
        )

        # Offline device should not be included
        assert "offline.example.com" not in devices

    def test_export_to_zenoss_default_filename(
        self, test_output_dir, sample_devices
    ):
        """Test exporting devices to Zenoss format with a default filename."""
        exporter = EnterpriseExporter(output_dir=test_output_dir)
        output_path = exporter.export_to_zenoss(sample_devices)

        # Check that the file was created with a timestamp in the name
        assert os.path.exists(output_path)
        assert "zenoss_devices_" in output_path
        assert output_path.endswith(".json")

        # Check the file contents
        with open(output_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Only alive devices should be included
        assert len(data["devices"]) == 3

    def test_export_generic(self, test_output_dir, sample_devices):
        """Test the generic export method with different formats."""
        exporter = EnterpriseExporter(output_dir=test_output_dir)

        # Test JSON export
        json_path = exporter.export(sample_devices, "json", "test_generic.json")
        assert os.path.exists(json_path)
        assert json_path.endswith(".json")

        # Test YAML export
        yaml_path = exporter.export(sample_devices, "yaml", "test_generic.yaml")
        assert os.path.exists(yaml_path)
        assert yaml_path.endswith(".yaml")

        # Test CSV export
        csv_path = exporter.export(sample_devices, "csv", "test_generic.csv")
        assert os.path.exists(csv_path)
        assert csv_path.endswith(".csv")

        # Test Nagios export
        nagios_path = exporter.export(
            sample_devices, "nagios", "test_generic.cfg"
        )
        assert os.path.exists(nagios_path)
        assert nagios_path.endswith(".cfg")

        # Test Zenoss export
        zenoss_path = exporter.export(
            sample_devices, "zenoss", "test_generic_zenoss.json"
        )
        assert os.path.exists(zenoss_path)
        assert zenoss_path.endswith(".json")

    def test_export_invalid_format(self, test_output_dir, sample_devices):
        """Test that exporting with an invalid format raises a ValueError."""
        exporter = EnterpriseExporter(output_dir=test_output_dir)

        with pytest.raises(ValueError) as excinfo:
            exporter.export(sample_devices, "invalid_format")

        assert "Unsupported export format: invalid_format" in str(excinfo.value)

    def test_export_case_insensitive(self, test_output_dir, sample_devices):
        """Test that the format type is case-insensitive."""
        exporter = EnterpriseExporter(output_dir=test_output_dir)

        # Test with uppercase format
        json_path = exporter.export(sample_devices, "JSON", "test_case.json")
        assert os.path.exists(json_path)

        # Test with mixed case format
        yaml_path = exporter.export(sample_devices, "YaMl", "test_case.yaml")
        assert os.path.exists(yaml_path)
