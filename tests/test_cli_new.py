"""Tests for the CLI interface."""

import tempfile
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from network_discovery.interfaces.cli import cli, parse_args, run_discovery


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
                "--repository-file",
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
    async def test_run_discovery_network(self, temp_dir):
        """Test that run_discovery works with a network range."""
        args = parse_args(
            [
                "192.168.1.0/24",
                "-o",
                temp_dir,
                "-t",
                temp_dir,
                "--no-notification",
                "--no-repository",
                "--no-report",
            ]
        )

        with patch(
            "network_discovery.interfaces.cli.DeviceDiscoveryService"
        ) as mock_discovery_service:
            mock_instance = mock_discovery_service.return_value
            mock_instance.discover_network = AsyncMock()
            mock_instance.discover_network.return_value = []

            result = await run_discovery(args)

            mock_instance.discover_network.assert_called_once_with("192.168.1.0/24")
            assert result == 0

    @pytest.mark.asyncio
    async def test_run_discovery_device(self, temp_dir):
        """Test that run_discovery works with a single IP address."""
        args = parse_args(
            [
                "192.168.1.1",
                "-o",
                temp_dir,
                "-t",
                temp_dir,
                "--no-notification",
                "--no-repository",
                "--no-report",
            ]
        )

        with patch(
            "network_discovery.interfaces.cli.DeviceDiscoveryService"
        ) as mock_discovery_service:
            mock_instance = mock_discovery_service.return_value
            mock_instance.discover_device = AsyncMock()
            # Return a mock device with a status method
            mock_device = MagicMock()
            mock_device.status.return_value = "alive: True"
            mock_instance.discover_device.return_value = mock_device

            result = await run_discovery(args)

            mock_instance.discover_device.assert_called_once_with("192.168.1.1")
            assert result == 0

    def test_cli(self, temp_dir):
        """Test the CLI entry point."""
        with patch("network_discovery.interfaces.cli.app") as mock_app:
            # Test that cli() passes args to app()
            cli(["192.168.1.0/24"])
            mock_app.assert_called_once_with(args=["192.168.1.0/24"])

            # Test that cli() with no args passes None to app()
            mock_app.reset_mock()
            cli()
            mock_app.assert_called_once_with(args=None)
