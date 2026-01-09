"""
Excel spreadsheet import/export module for network device management.

This module provides functionality for importing device data from Excel files
and exporting scan results back to Excel format.

Requires Python 3.12+
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

from devices import Device, ValidationError

# Type aliases using Python 3.12+ syntax
type FilePath = str | Path
type DeviceList = list[Device]
type CellValue = str | int | float | bool | None

logger = logging.getLogger(__name__)


class SpreadsheetError(Exception):
    """Raised when spreadsheet operations fail."""

    __slots__ = ("file_path", "row")

    def __init__(
        self,
        message: str,
        *,
        file_path: Path | None = None,
        row: int | None = None,
    ) -> None:
        super().__init__(message)
        self.file_path = file_path
        self.row = row


@dataclass(slots=True, frozen=True)
class ColumnConfig:
    """Configuration for spreadsheet column mappings."""

    host: str = "A"
    ip: str = "C"
    snmp_community: str = "D"
    mysql_user: str = "I"
    mysql_password: str = "J"
    header_row: int = 1
    data_start_row: int = 2


@dataclass(slots=True, frozen=True)
class ExportConfig:
    """Configuration for export operations."""

    include_header: bool = True
    auto_width: bool = True
    max_column_width: int = 50


@dataclass(slots=True)
class SpreadsheetImporter:
    """Import device data from Excel spreadsheets."""

    file_path: Path
    column_config: ColumnConfig = field(default_factory=ColumnConfig)

    def __post_init__(self) -> None:
        """Validate file path."""
        self.file_path = Path(self.file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Spreadsheet not found: {self.file_path}")

    def import_devices(self) -> DeviceList:
        """
        Import device data from the Excel spreadsheet.

        Returns:
            List of Device objects

        Raises:
            SpreadsheetError: If import fails
        """
        wb = openpyxl.load_workbook(self.file_path, read_only=True)
        sheet = wb.active

        if sheet is None:
            wb.close()
            raise SpreadsheetError(
                "No active worksheet found",
                file_path=self.file_path,
            )

        devices: DeviceList = []
        device_id = 1  # Sequential ID counter

        for row_num in range(self.column_config.data_start_row, sheet.max_row + 1):
            device = self._parse_row(sheet, row_num, device_id)
            if device is not None:
                devices.append(device)
                device_id += 1

        wb.close()
        logger.info("Imported %d devices from %s", len(devices), self.file_path)
        return devices

    def _parse_row(self, sheet: Worksheet, row_num: int, device_id: int) -> Device | None:
        """Parse a single row into a Device object."""
        try:
            host = self._get_cell_value(sheet, self.column_config.host, row_num)

            # Skip empty rows
            if not host:
                return None

            ip = self._get_cell_value(sheet, self.column_config.ip, row_num)
            snmp_community = self._get_cell_value(sheet, self.column_config.snmp_community, row_num)
            mysql_user = self._get_cell_value(sheet, self.column_config.mysql_user, row_num)
            mysql_password = self._get_cell_value(sheet, self.column_config.mysql_password, row_num)

            return Device(
                id=device_id,
                host=str(host).strip(),
                ip=str(ip).strip() if ip else str(host).strip(),
                snmp_community=str(snmp_community).strip() if snmp_community else "public",
                mysql_user=str(mysql_user).strip() if mysql_user else "",
                _mysql_password=str(mysql_password) if mysql_password else "",
            )

        except ValidationError as e:
            logger.warning("Skipping row %d: %s", row_num, e)
            return None
        except Exception as e:
            logger.error("Error processing row %d: %s", row_num, e)
            return None

    def _get_cell_value(
        self,
        sheet: Worksheet,
        column: str,
        row: int,
    ) -> CellValue:
        """Get the value from a cell."""
        return sheet[f"{column}{row}"].value


@dataclass(slots=True)
class SpreadsheetExporter:
    """Export device data to Excel spreadsheets."""

    devices: DeviceList
    export_config: ExportConfig = field(default_factory=ExportConfig)

    def export(
        self,
        output_path: FilePath | None = None,
        *,
        add_to_existing: bool = False,
    ) -> Path:
        """
        Export devices to an Excel spreadsheet.

        Args:
            output_path: Path for output file (auto-generated if None)
            add_to_existing: If True, add sheet to existing file

        Returns:
            Path to the output file
        """
        today = date.today().isoformat()
        sheet_name = f"{today}_check"

        if output_path is not None:
            filepath = Path(output_path)
            if filepath.exists() and add_to_existing:
                wb = openpyxl.load_workbook(filepath)
                sheet = wb.create_sheet(title=sheet_name)
            else:
                wb = openpyxl.Workbook()
                sheet = wb.active
                sheet.title = sheet_name
        else:
            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet.title = sheet_name
            filepath = Path(f"{today}_check.xlsx")

        self._write_header(sheet)
        self._write_devices(sheet)

        if self.export_config.auto_width:
            self._auto_adjust_columns(sheet)

        wb.save(filepath)
        wb.close()

        logger.info("Exported %d devices to %s", len(self.devices), filepath)
        return filepath

    def _write_header(self, sheet: Worksheet) -> None:
        """Write header row to worksheet."""
        if not self.export_config.include_header:
            return

        headers = ["name", "managementip", "state", "snmp", "ssh", "mysql", "errors"]
        for col, header in enumerate(headers, start=1):
            sheet.cell(row=1, column=col, value=header)

    def _write_devices(self, sheet: Worksheet) -> None:
        """Write device data to worksheet."""
        start_row = 2 if self.export_config.include_header else 1

        for row_num, device in enumerate(self.devices, start=start_row):
            sheet.cell(row=row_num, column=1, value=device.host)
            sheet.cell(row=row_num, column=2, value=device.ip)
            sheet.cell(row=row_num, column=3, value=_format_alive(device.alive))
            sheet.cell(row=row_num, column=4, value=_format_status(device.snmp))
            sheet.cell(row=row_num, column=5, value=_format_status(device.ssh))
            sheet.cell(row=row_num, column=6, value=_format_status(device.mysql))
            sheet.cell(row=row_num, column=7, value="; ".join(device.errors))

    def _auto_adjust_columns(self, sheet: Worksheet) -> None:
        """Auto-adjust column widths based on content."""
        for column in sheet.columns:
            max_length = 0
            column_letter = column[0].column_letter

            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except (TypeError, AttributeError):
                    pass

            adjusted_width = min(max_length + 2, self.export_config.max_column_width)
            sheet.column_dimensions[column_letter].width = adjusted_width


def _format_status(value: bool) -> str:
    """Format boolean status as 'open' or 'closed'."""
    return "open" if value else "closed"


def _format_alive(value: bool) -> str:
    """Format alive status as 'up' or 'down'."""
    return "up" if value else "down"


# Convenience functions for backward compatibility
def import_from_excel(spreadsheet_path: FilePath) -> DeviceList:
    """
    Import device data from an Excel spreadsheet.

    Args:
        spreadsheet_path: Path to the Excel file

    Returns:
        List of Device objects

    Raises:
        FileNotFoundError: If the spreadsheet doesn't exist
    """
    importer = SpreadsheetImporter(file_path=Path(spreadsheet_path))
    return importer.import_devices()


def export_to_excel(
    devices: DeviceList,
    spreadsheet_path: FilePath | None = None,
    send_email: bool = False,
) -> Path:
    """
    Export device scan results to an Excel spreadsheet.

    Args:
        devices: List of Device objects to export
        spreadsheet_path: Optional path to existing Excel file to update
        send_email: Whether to send the results via email

    Returns:
        Path to the output file
    """
    exporter = SpreadsheetExporter(devices=devices)
    output_path = exporter.export(
        output_path=spreadsheet_path,
        add_to_existing=spreadsheet_path is not None,
    )

    if send_email:
        try:
            import mail

            mail.send(output_path)
        except Exception as e:
            logger.error("Failed to send email: %s", e)

    return output_path


if __name__ == "__main__":
    import sys

    print("Spreadsheet import/export module")
    print()
    print("Usage:")
    print("  Import: python spreadsheet.py import <excel_file>")
    print("  Export: python spreadsheet.py export <output_file>")
    print()

    if len(sys.argv) > 2:
        command = sys.argv[1]
        filepath = sys.argv[2]

        match command:
            case "import":
                try:
                    imported_devices = import_from_excel(filepath)
                    print(f"Imported {len(imported_devices)} devices:")
                    for dev in imported_devices:
                        print(f"  - {dev}")
                except Exception as e:
                    print(f"Error: {e}")
                    sys.exit(1)
            case _:
                print(f"Unknown command: {command}")
                sys.exit(1)
