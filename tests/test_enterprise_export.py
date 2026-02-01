"""Tests for enterprise export functionality."""

import csv
import json
import tempfile
from datetime import datetime
from pathlib import Path

import pytest
import yaml

from network_discovery.domain.device import Device
from network_discovery.enterprise.device import (
    DeviceCategory,
    DeviceStatus,
    EnterpriseDevice,
)
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
    return EnterpriseDevice(
        device=base_device,
        category=DeviceCategory.SERVER,
        status=DeviceStatus.OPERATIONAL,
        asset_id="ASSET-001",
        location="Data Center 1",
        owner="IT Department",
        os_version="Ubuntu 20.04 LTS",
        firmware_version="2.1.3",
        compliance=True,
        last_scan_time=datetime(2025, 1, 1, 12, 0, 0),
        uptime=86400,  # 1 day in seconds
        tags=frozenset(["production", "web-server"]),
        custom_attributes={
            "maintenance_contract": "MAINT-123",
            "critical": True,
        },
    )


@pytest.fixture
def enterprise_devices():
    """Create a list of EnterpriseDevice instances."""
    devices = []

    categories = [
        DeviceCategory.SERVER,
        DeviceCategory.NETWORK,
        DeviceCategory.STORAGE,
        DeviceCategory.SECURITY,
    ]

    statuses = [
        DeviceStatus.OPERATIONAL,
        DeviceStatus.MAINTENANCE,
        DeviceStatus.DEGRADED,
        DeviceStatus.CRITICAL,
    ]

    for i in range(4):
        base = Device(
            id=i + 1,
            host=f"device{i + 1}.example.com",
            ip=f"192.168.1.{100 + i}",
            snmp_group="public" if i % 2 == 0 else "private",
            alive=i != 3,
            snmp=i % 2 == 0,
            ssh=i % 3 == 0,
            mysql=i % 4 == 0,
            mysql_user="admin" if i % 4 == 0 else "",
            mysql_password="password123" if i % 4 == 0 else "",
            uname=f"Linux {i + 1}" if i != 3 else "",
            errors=(f"Error {i + 1}",) if i == 3 else (),
            scanned=True,
        )

        device = EnterpriseDevice(
            device=base,
            category=categories[i],
            status=statuses[i],
            asset_id=f"ASSET-00{i + 1}",
            location=f"Location {i + 1}",
            owner=f"Owner {i + 1}",
            os_version=f"OS Version {i + 1}" if i != 3 else "",
            firmware_version=f"Firmware {i + 1}" if i != 3 else "",
            compliance=i != 3,
            last_scan_time=datetime(2025, 1, 1, 12, i, 0) if i != 3 else None,
            uptime=86400 * (i + 1) if i != 3 else None,
            tags=frozenset([f"tag-{i + 1}", "enterprise"]) if i != 3 else frozenset(),
            custom_attributes=(
                {"key1": f"value{i + 1}", "key2": i + 1} if i != 3 else {}
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

        new_dir = str(Path(temp_dir) / "exports")
        exporter = EnterpriseExporter(output_dir=new_dir)
        assert Path(new_dir).exists()

    def test_export_to_json(self, exporter, enterprise_devices):
        """Test exporting devices to JSON format."""
        output_path = exporter.export_to_json(enterprise_devices)

        assert Path(output_path).exists()
        assert output_path.endswith(".json")

        with Path(output_path).open() as f:
            data = json.load(f)
            assert isinstance(data, list)
            assert len(data) == len(enterprise_devices)

            first_device = data[0]
            assert first_device["id"] == 1
            assert first_device["host"] == "device1.example.com"
            assert first_device["category"] == "SERVER"
            assert first_device["status"] == "OPERATIONAL"
            assert first_device["asset_id"] == "ASSET-001"

    def test_export_to_json_default_filename(self, exporter, enterprise_devices):
        """Test exporting devices to JSON format with a default filename."""
        output_path = exporter.export_to_json(enterprise_devices)

        assert Path(output_path).exists()
        assert "devices_" in output_path
        assert output_path.endswith(".json")

    def test_export_to_yaml(self, exporter, enterprise_devices):
        """Test exporting devices to YAML format."""
        output_path = exporter.export_to_yaml(enterprise_devices)

        assert Path(output_path).exists()
        assert output_path.endswith(".yaml")

        with Path(output_path).open() as f:
            data = yaml.safe_load(f)
            assert isinstance(data, list)
            assert len(data) == len(enterprise_devices)

            first_device = data[0]
            assert first_device["id"] == 1
            assert first_device["host"] == "device1.example.com"
            assert first_device["category"] == "SERVER"

    def test_export_to_yaml_default_filename(self, exporter, enterprise_devices):
        """Test exporting devices to YAML format with a default filename."""
        output_path = exporter.export_to_yaml(enterprise_devices)

        assert Path(output_path).exists()
        assert "devices_" in output_path
        assert output_path.endswith(".yaml")

    def test_export_to_csv(self, exporter, enterprise_devices):
        """Test exporting devices to CSV format."""
        output_path = exporter.export_to_csv(enterprise_devices)

        assert Path(output_path).exists()
        assert output_path.endswith(".csv")

        with Path(output_path).open(newline="") as f:
            reader = csv.reader(f)
            headers = next(reader)

            assert "ID" in headers or "id" in headers.lower() if headers else False

            rows = list(reader)
            assert len(rows) == len(enterprise_devices)

    def test_export_to_csv_default_filename(self, exporter, enterprise_devices):
        """Test exporting devices to CSV format with a default filename."""
        output_path = exporter.export_to_csv(enterprise_devices)

        assert Path(output_path).exists()
        assert output_path.endswith(".csv")

    def test_export_to_nagios(self, exporter, enterprise_devices):
        """Test exporting devices to Nagios configuration format."""
        output_path = exporter.export_to_nagios(enterprise_devices)

        assert Path(output_path).exists()
        assert output_path.endswith(".cfg")

        content = Path(output_path).read_text()
        assert "define host {" in content
        assert "device1.example.com" in content

    def test_export_to_nagios_default_filename(self, exporter, enterprise_devices):
        """Test exporting devices to Nagios format with a default filename."""
        output_path = exporter.export_to_nagios(enterprise_devices)

        assert Path(output_path).exists()
        assert output_path.endswith(".cfg")

    def test_export_to_zenoss(self, exporter, enterprise_devices):
        """Test exporting devices to Zenoss JSON format."""
        output_path = exporter.export_to_zenoss(enterprise_devices)

        assert Path(output_path).exists()
        assert output_path.endswith(".json")

        with Path(output_path).open() as f:
            data = json.load(f)
            assert "devices" in data
            assert isinstance(data["devices"], list)

    def test_export_to_zenoss_default_filename(self, exporter, enterprise_devices):
        """Test exporting devices to Zenoss format with a default filename."""
        output_path = exporter.export_to_zenoss(enterprise_devices)

        assert Path(output_path).exists()
        assert output_path.endswith(".json")

    def test_export_generic(self, exporter, enterprise_devices):
        """Test the generic export method with different formats."""
        json_path = exporter.export(enterprise_devices, "json")
        assert Path(json_path).exists()
        assert json_path.endswith(".json")

        yaml_path = exporter.export(enterprise_devices, "yaml")
        assert Path(yaml_path).exists()
        assert yaml_path.endswith(".yaml")

        csv_path = exporter.export(enterprise_devices, "csv")
        assert Path(csv_path).exists()
        assert csv_path.endswith(".csv")

        nagios_path = exporter.export(enterprise_devices, "nagios")
        assert Path(nagios_path).exists()
        assert nagios_path.endswith(".cfg")

        zenoss_path = exporter.export(enterprise_devices, "zenoss")
        assert Path(zenoss_path).exists()
        assert zenoss_path.endswith(".json")

    def test_export_invalid_format(self, exporter, enterprise_devices):
        """Test that exporting with an invalid format raises a ValueError."""
        with pytest.raises(ValueError):
            exporter.export(enterprise_devices, "invalid_format")

    def test_export_case_insensitive(self, exporter, enterprise_devices):
        """Test that the format type is case-insensitive."""
        json_path = exporter.export(enterprise_devices, "JSON")
        assert Path(json_path).exists()

        yaml_path = exporter.export(enterprise_devices, "YaMl")
        assert Path(yaml_path).exists()


class TestEnterpriseExportIntegration:
    """Integration tests for the enterprise export functionality."""

    def test_integration_workflow(self, exporter, enterprise_devices, temp_dir):
        """Test a complete export workflow with multiple formats."""
        test_dir = Path(temp_dir) / "integration_test"
        test_dir.mkdir(parents=True, exist_ok=True)
        exporter.output_dir = str(test_dir)

        formats = ["json", "yaml", "csv", "nagios", "zenoss"]
        paths = {}

        for fmt in formats:
            paths[fmt] = exporter.export(enterprise_devices, fmt)
            assert Path(paths[fmt]).exists()

        assert len(paths) == len(formats)
