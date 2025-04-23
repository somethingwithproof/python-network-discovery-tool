"""Tests for the EnterpriseExporter class."""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path

import pytest
import yaml

from network_discovery.domain.device import Device
from network_discovery.enterprise.device import EnterpriseDevice, DeviceCategory, DeviceStatus
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

    def test_export_to_json_default_filename(self, test_output_dir, sample_devices):
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

    def test_export_to_yaml_default_filename(self, test_output_dir, sample_devices):
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
        assert "1,server1.example.com,192.168.1.1,True,True,True,False" in lines[1]
        assert "2,router1.example.com,192.168.1.254,True,True,True,False" in lines[2]
        assert "3,storage1.example.com,192.168.1.10,True,True,False,False" in lines[3]
        assert "4,offline.example.com,192.168.1.20,False,False,False,False" in lines[4]

    def test_export_to_csv_default_filename(self, test_output_dir, sample_devices):
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

    def test_export_to_nagios_default_filename(self, test_output_dir, sample_devices):
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
        
        assert "server1.example.com" in devices
        assert devices["server1.example.com"]["deviceClass"] == "/Devices/Server"
        assert devices["server1.example.com"]["manageIp"] == "192.168.1.1"
        assert devices["server1.example.com"]["snmpMonitor"] is True
        assert devices["server1.example.com"]["sshMonitor"] is True
        assert "production" in devices["server1.example.com"]["systems"]
        assert "web-server" in devices["server1.example.com"]["systems"]
        assert devices["server1.example.com"]["location"] == "Data Center 1"
        assert devices["server1.example.com"]["properties"]["assetId"] == "ASSET001"
        assert devices["server1.example.com"]["properties"]["owner"] == "IT Department"
        assert devices["server1.example.com"]["properties"]["osVersion"] == "Ubuntu 22.04"
        assert devices["server1.example.com"]["properties"]["firmwareVersion"] == "1.2.3"
        assert devices["server1.example.com"]["properties"]["rack"] == "A1"
        assert devices["server1.example.com"]["properties"]["power_supply"] == "redundant"
        
        assert "router1.example.com" in devices
        assert devices["router1.example.com"]["deviceClass"] == "/Devices/Network"
        
        assert "storage1.example.com" in devices
        assert devices["storage1.example.com"]["deviceClass"] == "/Devices/Storage"
        
        # Offline device should not be included
        assert "offline.example.com" not in devices

    def test_export_to_zenoss_default_filename(self, test_output_dir, sample_devices):
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
        nagios_path = exporter.export(sample_devices, "nagios", "test_generic.cfg")
        assert os.path.exists(nagios_path)
        assert nagios_path.endswith(".cfg")
        
        # Test Zenoss export
        zenoss_path = exporter.export(sample_devices, "zenoss", "test_generic_zenoss.json")
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
