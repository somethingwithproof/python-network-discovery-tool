"""Tests for the CLI interface."""

import tempfile
from unittest.mock import AsyncMock, patch

import pytest

from network_discovery.interfaces.cli import cli, parse_args, run_discovery


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
    async def test_run_discovery_single_device(self, temp_directory):
        """Test that run_discovery works with a network CIDR."""
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
            "network_discovery.interfaces.cli.DeviceDiscoveryService"
        ) as mock_discovery_service:
            mock_instance = mock_discovery_service.return_value
            mock_instance.discover_network = AsyncMock()
            mock_instance.discover_network.return_value = []

            result = await run_discovery(args)

            mock_instance.discover_network.assert_called_once_with("192.168.1.0/24")
            # With --no-report, generate_report should not be called
            assert result == 0

    @pytest.mark.asyncio
    async def test_run_discovery_device(self, temp_directory):
        """Test that run_discovery works with a single device IP."""
        from unittest.mock import MagicMock

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
            # With --no-report, generate_report should not be called
            assert result == 0

    def test_cli_entry_point(self, temp_directory):
        """Test the CLI entry point function."""
        with patch("network_discovery.interfaces.cli.app") as mock_app:
            # Test that cli() passes args to app()
            cli(["192.168.1.0/24"])
            mock_app.assert_called_once_with(args=["192.168.1.0/24"])

            # Test that cli() with no args passes None to app()
            mock_app.reset_mock()
            cli()
            mock_app.assert_called_once_with(args=None)
