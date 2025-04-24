"""Tests for the CLI interface."""

import os
import tempfile
from unittest.mock import patch, AsyncMock

import pytest

from network_discovery.interfaces.cli import parse_args, run_discovery, cli


@pytest.fixture
def temp_dir():
    """Yield a temporary directory."""
    with tempfile.TemporaryDirectory() as tmp:
        yield tmp


class TestCli:
    """Tests for the CLI interface."""

    def test_parse_args_defaults(self):
        """Test that default arguments are parsed correctly."""
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

    def test_parse_args_custom(self):
        """Test that custom arguments are parsed correctly."""
        args = parse_args([
            "192.168.1.1",
            "-o", "/tmp/output",
            "-f", "csv",
            "-t", "/tmp/templates",
            "-v",
            "--no-report",
            "--no-notification",
            "--no-repository",
            "--repository-file", "/tmp/devices.json",
        ])
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
    async def test_run_discovery_network(self, temp_dir):
        """Test that run_discovery works with a network range."""
        args = parse_args([
            "192.168.1.0/24",
            "-o", temp_dir,
            "-t", temp_dir,
            "--no-notification",
            "--no-repository"
        ])

        with patch("network_discovery.core.discovery.DeviceDiscoveryService") as mock_discovery_service:
            mock_instance = mock_discovery_service.return_value
            mock_instance.discover_network = AsyncMock()
            mock_instance.discover_network.return_value = []
            mock_instance.generate_report.return_value = os.path.join(temp_dir, "devices.html")

            await run_discovery(args)

            mock_instance.discover_network.assert_called_once_with("192.168.1.0/24")
            mock_instance.generate_report.assert_called_once_with("html")

    @pytest.mark.asyncio
    async def test_run_discovery_device(self, temp_dir):
        """Test that run_discovery works with a single IP address."""
        args = parse_args([
            "192.168.1.1",
            "-o", temp_dir,
            "-t", temp_dir,
            "--no-notification",
            "--no-repository"
        ])

        with patch("network_discovery.core.discovery.DeviceDiscoveryService") as mock_discovery_service:
            mock_instance = mock_discovery_service.return_value
            mock_instance.discover_device = AsyncMock()
            mock_instance.discover_device.return_value = None
            mock_instance.generate_report.return_value = os.path.join(temp_dir, "devices.html")

            await run_discovery(args)

            mock_instance.discover_device.assert_called_once_with("192.168.1.1")
            mock_instance.generate_report.assert_called_once_with("html")

    def test_cli(self, temp_dir):
        """Test the CLI entry point."""
        with patch("network_discovery.interfaces.cli.parse_args") as mock_parse_args:
            with patch("asyncio.run") as mock_run:
                mock_parse_args.return_value = parse_args([
                    "192.168.1.0/24",
                    "-o", temp_dir,
                    "-t", temp_dir,
                    "--no-notification",
                    "--no-repository",
                    "--no-report",
                ])
                cli(["192.168.1.0/24"])
                mock_run.assert_called_once()