"""
Tests for the discovery module (main orchestrator).
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from discovery import parse_args, scan_device, scan_devices, main
from devices import Device, ScanConfig


class TestParseArgs:
    """Tests for the parse_args function."""

    def test_parse_args_minimal(self):
        """Test parsing minimal arguments."""
        with patch('sys.argv', ['discovery', 'input.xlsx']):
            args = parse_args()
            assert args.inputfile == Path('input.xlsx')
            assert args.output is None
            assert args.workers == 10
            assert args.database == Path('devices.db')
            assert args.verbose is False

    def test_parse_args_full(self):
        """Test parsing all arguments."""
        with patch('sys.argv', [
            'discovery',
            'input.xlsx',
            '-o', 'output.xlsx',
            '-w', '20',
            '-d', 'custom.db',
            '-v',
            '--no-ssh-strict',
        ]):
            args = parse_args()
            assert args.inputfile == Path('input.xlsx')
            assert args.output == Path('output.xlsx')
            assert args.workers == 20
            assert args.database == Path('custom.db')
            assert args.verbose is True
            assert args.no_ssh_strict is True

    def test_parse_args_missing_input(self):
        """Test that missing input file raises error."""
        with patch('sys.argv', ['discovery']):
            with pytest.raises(SystemExit):
                parse_args()


class TestScanDevice:
    """Tests for the scan_device function."""

    def test_scan_device_success(
        self,
        sample_device: Device,
        scan_config: ScanConfig,
        mock_subprocess_ping_success,
        mock_paramiko_success,
        mock_snmp_success,
    ):
        """Test successful device scan."""
        result = scan_device(sample_device, scan_config)
        assert result.scanned is True
        assert result is sample_device

    def test_scan_device_failure(
        self,
        sample_device: Device,
        scan_config: ScanConfig,
        mock_subprocess_ping_failure,
    ):
        """Test device scan when ping fails."""
        result = scan_device(sample_device, scan_config)
        assert result.scanned is True
        assert result.alive is False

    def test_scan_device_exception(
        self,
        sample_device: Device,
        scan_config: ScanConfig,
    ):
        """Test device scan handles exceptions."""
        with patch.object(sample_device, 'scan_all', side_effect=Exception("Test error")):
            result = scan_device(sample_device, scan_config)
            assert "Test error" in str(result.errors)


class TestScanDevices:
    """Tests for the scan_devices function."""

    def test_scan_devices_empty_list(self, scan_config: ScanConfig):
        """Test scanning empty device list."""
        result = scan_devices([], scan_config)
        assert result == []

    def test_scan_devices_single(
        self,
        sample_device: Device,
        scan_config: ScanConfig,
        mock_subprocess_ping_success,
        mock_paramiko_success,
        mock_snmp_success,
    ):
        """Test scanning a single device."""
        result = scan_devices([sample_device], scan_config, max_workers=1)
        assert len(result) == 1
        assert result[0].scanned is True

    def test_scan_devices_multiple(
        self,
        sample_devices: list[Device],
        scan_config: ScanConfig,
        mock_subprocess_ping_success,
        mock_paramiko_success,
        mock_snmp_success,
    ):
        """Test scanning multiple devices concurrently."""
        result = scan_devices(sample_devices, scan_config, max_workers=3)
        assert len(result) == len(sample_devices)
        for device in result:
            assert device.scanned is True

    def test_scan_devices_respects_max_workers(
        self,
        sample_devices: list[Device],
        scan_config: ScanConfig,
        mock_subprocess_ping_failure,
    ):
        """Test that max_workers is respected."""
        # With 3 devices and max_workers=2, should still complete
        result = scan_devices(sample_devices, scan_config, max_workers=2)
        assert len(result) == len(sample_devices)


class TestMain:
    """Tests for the main function."""

    def test_main_file_not_found(self, temp_dir: Path):
        """Test main with non-existent input file."""
        with patch('sys.argv', ['discovery', str(temp_dir / 'nonexistent.xlsx')]):
            result = main()
            assert result == 3  # ExitCode.INPUT_ERROR

    @patch('discovery.spreadsheet')
    @patch('discovery.database')
    def test_main_empty_file(
        self,
        mock_database,
        mock_spreadsheet,
        temp_dir: Path,
    ):
        """Test main with empty input file."""
        # Create empty input file
        input_file = temp_dir / 'empty.xlsx'
        input_file.touch()

        mock_spreadsheet.import_from_excel.return_value = []
        mock_db_instance = MagicMock()
        mock_database.Database.return_value = mock_db_instance

        with patch('sys.argv', ['discovery', str(input_file)]):
            result = main()
            assert result == 0

    @patch('discovery.spreadsheet')
    @patch('discovery.database')
    def test_main_success(
        self,
        mock_database,
        mock_spreadsheet,
        sample_devices: list[Device],
        temp_dir: Path,
        mock_subprocess_ping_success,
        mock_paramiko_success,
        mock_snmp_success,
    ):
        """Test successful main execution."""
        # Create input file
        input_file = temp_dir / 'input.xlsx'
        input_file.touch()

        mock_spreadsheet.import_from_excel.return_value = sample_devices
        mock_spreadsheet.export_to_excel.return_value = temp_dir / 'output.xlsx'
        mock_db_instance = MagicMock()
        mock_database.Database.return_value = mock_db_instance

        with patch('sys.argv', ['discovery', str(input_file), '-w', '2']):
            result = main()
            assert result == 0

        # Verify database operations were called
        mock_db_instance.create_table.assert_called_once()
        mock_db_instance.insert_devices.assert_called_once()
        assert mock_db_instance.update_device.call_count == len(sample_devices)

    @patch('discovery.spreadsheet')
    @patch('discovery.database')
    def test_main_import_error(
        self,
        mock_database,
        mock_spreadsheet,
        temp_dir: Path,
    ):
        """Test main handles import errors."""
        input_file = temp_dir / 'input.xlsx'
        input_file.touch()

        mock_spreadsheet.import_from_excel.side_effect = Exception("Import error")

        with patch('sys.argv', ['discovery', str(input_file)]):
            result = main()
            assert result == 3  # ExitCode.INPUT_ERROR

    @patch('discovery.spreadsheet')
    @patch('discovery.database')
    def test_main_verbose_mode(
        self,
        mock_database,
        mock_spreadsheet,
        temp_dir: Path,
    ):
        """Test main with verbose logging."""
        import logging

        input_file = temp_dir / 'input.xlsx'
        input_file.touch()

        mock_spreadsheet.import_from_excel.return_value = []
        mock_db_instance = MagicMock()
        mock_database.Database.return_value = mock_db_instance

        with patch('sys.argv', ['discovery', str(input_file), '-v']):
            with patch.object(logging.getLogger(), 'setLevel') as mock_set_level:
                main()
                mock_set_level.assert_called_with(logging.DEBUG)
