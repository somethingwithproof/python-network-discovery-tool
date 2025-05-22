"""Tests for the CLI interface."""

import os
import tempfile
from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from network_discovery.interfaces.cli import cli
from network_discovery.interfaces.cli import parse_args
from network_discovery.interfaces.cli import run_discovery


@pytest.fixture
def temp_directory():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


class TestCli:
    """Tests for the CLI interface."""

    def test_cli_with_asyncio(self, temp_directory):
        """Test that the CLI function works with asyncio.run."""
        args = parse_args(["192.168.1.0/24"])
        assert args.network == "192.168.1.0/24"
        assert args.output_dir == "./output"
        assert args.format == "html"
        assert args.template_dir == "./templates"
        assert not args.verbose
        assert not args.no_report
        assert not args.no_notification
        assert not args.no_repository
        assert args.repository_file == "./devices.json"

    def test_cli_parse_args_custom(self):
        """Test parse_args with custom arguments."""
        args = parse_args(
            [
                "192.168.1.1",
                "-o",
                "/tmp/output",
                "-f",
                "csv",
                "-t",
                "/tmp/templates",
                "-v",
                "--no-report",
                "--no-notification",
                "--no-repository",
                "-r",
                "/tmp/devices.json",
            ]
        )
        assert args.network == "192.168.1.1"
        assert args.output_dir == "/tmp/output"
        assert args.format == "csv"
        assert args.template_dir == "/tmp/templates"
        assert args.verbose
        assert args.no_report
        assert args.no_notification
        assert args.no_repository
        assert args.repository_file == "/tmp/devices.json"

    @pytest.mark.asyncio
    async def test_run_discovery_single_device(self, temp_directory):
        """Test that run_discovery works with a single device IP."""
        args = parse_args(
            [
                "192.168.1.0/24",
                "-o",
                temp_directory,
                "-t",
                temp_directory,
                "--no-notification",
                "--no-repository",
                "--no-report",
            ]
        )

        with patch(
            "network_discovery.core.discovery.DeviceDiscoveryService"
        ) as mock_discovery_service:
            mock_instance = mock_discovery_service.return_value
            mock_instance.discover_network = AsyncMock()
            mock_instance.discover_network.return_value = []
            mock_instance.generate_report.return_value = os.path.join(
                temp_directory, "devices.html"
            )

            await run_discovery(args)

            mock_instance.discover_network.assert_called_once_with(
                "192.168.1.0/24"
            )
            mock_instance.generate_report.assert_called_once_with("html")

    @pytest.mark.asyncio
    async def test_run_discovery_device(self, temp_directory):
        """Test that run_discovery works with a single device."""
        args = parse_args(
            [
                "192.168.1.1",
                "-o",
                temp_directory,
                "-t",
                temp_directory,
                "--no-notification",
                "--no-repository",
                "--no-report",
            ]
        )

        with patch(
            "network_discovery.core.discovery.DeviceDiscoveryService"
        ) as mock_discovery_service:
            mock_instance = mock_discovery_service.return_value
            mock_instance.discover_device = AsyncMock()
            mock_instance.discover_device.return_value = None
            mock_instance.generate_report.return_value = os.path.join(
                temp_directory, "devices.html"
            )

            await run_discovery(args)

            mock_instance.discover_device.assert_called_once_with("192.168.1.1")
            mock_instance.generate_report.assert_called_once_with("html")

    def test_cli_entry_point(self, temp_directory):
        """Test the CLI entry point function."""
        with patch(
            "network_discovery.interfaces.cli.parse_args"
        ) as mock_parse_args:
            with patch("asyncio.run") as mock_run:
                mock_args = parse_args(
                    [
                        "192.168.1.0/24",
                        "-o",
                        temp_directory,
                        "-t",
                        temp_directory,
                        "--no-notification",
                        "--no-repository",
                        "--no-report",
                    ]
                )
                mock_parse_args.return_value = mock_args

                cli(["192.168.1.0/24"])
                mock_run.assert_called_once()
