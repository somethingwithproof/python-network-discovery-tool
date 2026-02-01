"""Enterprise export module.

This module provides export functionality for enterprise devices in various formats.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import yaml


if TYPE_CHECKING:
    from network_discovery.enterprise.device import EnterpriseDevice


class EnterpriseExporter:
    """Exporter for enterprise devices in various formats."""

    def __init__(self, output_dir: str = "output") -> None:
        """Initialize a new EnterpriseExporter.

        Args:
            output_dir: The directory where export files will be saved.
        """
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    def export_to_json(
        self, devices: list[EnterpriseDevice], filename: str | None = None
    ) -> str:
        """Export devices to JSON format.

        Args:
            devices: The list of devices to export.
            filename: The name of the output file. If None, a default name will be used.

        Returns:
            The path to the generated JSON file.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"devices_{timestamp}.json"

        output_path = str(Path(self.output_dir) / filename)
        devices_data = [device.to_dict() for device in devices]

        with Path(output_path).open("w", encoding="utf-8") as f:
            json.dump(devices_data, f, indent=2)

        return output_path

    def export_to_yaml(
        self, devices: list[EnterpriseDevice], filename: str | None = None
    ) -> str:
        """Export devices to YAML format.

        Args:
            devices: The list of devices to export.
            filename: The name of the output file. If None, a default name will be used.

        Returns:
            The path to the generated YAML file.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"devices_{timestamp}.yaml"

        output_path = str(Path(self.output_dir) / filename)
        devices_data = [device.to_dict() for device in devices]

        with Path(output_path).open("w", encoding="utf-8") as f:
            yaml.dump(devices_data, f, default_flow_style=False, sort_keys=False)

        return output_path

    def export_to_csv(
        self, devices: list[EnterpriseDevice], filename: str | None = None
    ) -> str:
        """Export devices to CSV format.

        Args:
            devices: The list of devices to export.
            filename: The name of the output file. If None, a default name will be used.

        Returns:
            The path to the generated CSV file.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"devices_{timestamp}.csv"

        output_path = str(Path(self.output_dir) / filename)

        headers = [
            "ID",
            "Host",
            "IP",
            "Alive",
            "SSH",
            "SNMP",
            "MySQL",
            "Category",
            "Status",
            "Asset ID",
            "Location",
            "Owner",
            "OS Version",
            "Firmware Version",
            "Compliance",
            "Last Scan Time",
            "Uptime (seconds)",
            "Tags",
        ]

        with Path(output_path).open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for device in devices:
                writer.writerow(
                    [
                        device.id,
                        device.host,
                        device.ip,
                        device.alive,
                        device.ssh,
                        device.snmp,
                        device.mysql,
                        device.category.name,
                        device.status.name,
                        device.asset_id,
                        device.location,
                        device.owner,
                        device.os_version,
                        device.firmware_version,
                        device.compliance,
                        (
                            device.last_scan_time.isoformat()
                            if device.last_scan_time
                            else ""
                        ),
                        device.uptime if device.uptime is not None else "",
                        ", ".join(device.tags),
                    ]
                )

        return output_path

    def export_to_nagios(  # noqa: PLR0912
        self, devices: list[EnterpriseDevice], filename: str | None = None
    ) -> str:
        """Export devices to Nagios configuration format.

        Args:
            devices: The list of devices to export.
            filename: The name of the output file. If None, a default name will be used.

        Returns:
            The path to the generated Nagios configuration file.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"nagios_devices_{timestamp}.cfg"

        output_path = str(Path(self.output_dir) / filename)

        with Path(output_path).open("w", encoding="utf-8") as f:
            for device in devices:
                if not device.alive:
                    continue

                f.write("define host {\n")
                f.write(f"    host_name              {device.host}\n")
                f.write(f"    alias                  {device.host}\n")
                f.write(f"    address                {device.ip}\n")
                f.write("    use                    generic-host\n")

                for key, value in device.custom_attributes.items():
                    if isinstance(value, (str, int, float, bool)):
                        f.write(f"    _{key}                 {value}\n")

                if device.tags:
                    f.write(f"    hostgroups             {','.join(device.tags)}\n")

                notes = []
                if device.asset_id:
                    notes.append(f"Asset ID: {device.asset_id}")
                if device.location:
                    notes.append(f"Location: {device.location}")
                if device.owner:
                    notes.append(f"Owner: {device.owner}")

                if notes:
                    f.write(f"    notes                  {'; '.join(notes)}\n")

                f.write("}\n\n")

                if device.ssh:
                    f.write("define service {\n")
                    f.write(f"    host_name              {device.host}\n")
                    f.write("    service_description    SSH\n")
                    f.write("    check_command          check_ssh\n")
                    f.write("    use                    generic-service\n")
                    f.write("}\n\n")

                if device.snmp:
                    snmp_group = device.device.snmp_group
                    f.write("define service {\n")
                    f.write(f"    host_name              {device.host}\n")
                    f.write("    service_description    SNMP\n")
                    f.write(
                        f"    check_command          check_snmp!-C {snmp_group} -o sysDescr.0\n"
                    )
                    f.write("    use                    generic-service\n")
                    f.write("}\n\n")

                if device.mysql:
                    f.write("define service {\n")
                    f.write(f"    host_name              {device.host}\n")
                    f.write("    service_description    MySQL\n")
                    f.write("    check_command          check_mysql\n")
                    f.write("    use                    generic-service\n")
                    f.write("}\n\n")

        return output_path

    def export_to_zenoss(
        self, devices: list[EnterpriseDevice], filename: str | None = None
    ) -> str:
        """Export devices to Zenoss JSON format.

        Args:
            devices: The list of devices to export.
            filename: The name of the output file. If None, a default name will be used.

        Returns:
            The path to the generated Zenoss JSON file.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"zenoss_devices_{timestamp}.json"

        output_path = str(Path(self.output_dir) / filename)

        zenoss_devices = []
        for device in devices:
            if not device.alive:
                continue

            device_class = _map_category_to_zenoss_class(device.category.name)

            base_device = device.device

            zenoss_device = {
                "deviceName": device.host,
                "deviceClass": device_class,
                "manageIp": device.ip,
                "title": device.host,
                "snmpCommunity": base_device.snmp_group if device.snmp else "",
                "snmpMonitor": device.snmp,
                "pingMonitor": True,
                "sshMonitor": device.ssh,
                "productionState": 1000,
                "comments": device.status.name,
                "systems": list(device.tags),
                "groups": [],
                "location": device.location,
                "zProperties": {
                    "zCommandUsername": (
                        base_device.mysql_user if device.mysql else ""
                    ),
                    "zCommandPassword": (
                        base_device.mysql_password if device.mysql else ""
                    ),
                },
                "properties": {
                    "assetId": device.asset_id,
                    "owner": device.owner,
                    "osVersion": device.os_version,
                    "firmwareVersion": device.firmware_version,
                },
            }

            for key, value in device.custom_attributes.items():
                if isinstance(value, (str, int, float, bool)):
                    zenoss_device["properties"][key] = value

            zenoss_devices.append(zenoss_device)

        zenoss_data = {"devices": zenoss_devices}

        with Path(output_path).open("w", encoding="utf-8") as f:
            json.dump(zenoss_data, f, indent=2)

        return output_path

    def export(
        self,
        devices: list[EnterpriseDevice],
        format_type: str,
        filename: str | None = None,
    ) -> str:
        """Export devices to the specified format.

        Args:
            devices: The list of devices to export.
            format_type: The format to export to (json, yaml, csv, nagios, zenoss).
            filename: The name of the output file. If None, a default name will be used.

        Returns:
            The path to the generated file.

        Raises:
            ValueError: If the format type is not supported.
        """
        exporters = {
            "json": self.export_to_json,
            "yaml": self.export_to_yaml,
            "csv": self.export_to_csv,
            "nagios": self.export_to_nagios,
            "zenoss": self.export_to_zenoss,
        }

        format_lower = format_type.lower()
        exporter_fn = exporters.get(format_lower)
        if exporter_fn is None:
            raise ValueError(f"Unsupported export format: {format_type}")
        return exporter_fn(devices, filename)


def _map_category_to_zenoss_class(category_name: str) -> str:
    """Map a device category name to a Zenoss device class.

    Args:
        category_name: The device category name.

    Returns:
        The Zenoss device class path.
    """
    mapping = {
        "NETWORK": "/Devices/Network",
        "SERVER": "/Devices/Server",
        "STORAGE": "/Devices/Storage",
        "SECURITY": "/Devices/Security",
    }
    return mapping.get(category_name, "/Devices")
