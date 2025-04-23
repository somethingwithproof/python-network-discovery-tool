"""Tests for the improved CLI interface."""

import os
import tempfile
from unittest.mock import patch, AsyncMock, MagicMock

import pytest

from improvements.cli_improved import parse_args, run_discovery, cli, validate_network


class TestCliImproved:
    """Tests for the improved CLI interface."""

    def test_validate_network_valid_cidr(self):
        """Test that a valid CIDR network is validated correctly."""
        is_network, network_obj, error = validate_network("192.168.1.0/24")
        assert is_network is True
        assert str(network_obj) == "192.168.1.0/24"
        assert error == ""

    def test_validate_network_valid_ip(self):
        """Test that a valid IP address is validated correctly."""
        is_network, network_obj, error = validate_network("192.168.1.1")
        assert is_network is False
        assert str(network_obj) == "192.168.1.1"
        assert error == ""

    def test_validate_network_invalid(self):
        """Test that an invalid network or IP address is rejected."""
        is_network, network_obj, error = validate_network("invalid")
        assert is_network is False
        assert network_obj is None
        assert "Invalid network or IP address format" in error

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
        assert not args.email
        assert args.smtp_server == "smtp.gmail.com"
        assert args.smtp_port == 587
        assert args.smtp_username is None
        assert args.smtp_password is None
        assert args.email_recipient is None

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
                "--email",
                "--smtp-server",
                "smtp.example.com",
                "--smtp-port",
                "465",
                "--smtp-username",
                "user@example.com",
                "--smtp-password",
                "password",
                "--email-recipient",
                "admin@example.com",
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
        assert args.email
        assert args.smtp_server == "smtp.example.com"
        assert args.smtp_port == 465
        assert args.smtp_username == "user@example.com"
        assert args.smtp_password == "password"
        assert args.email_recipient == "admin@example.com"

    @pytest.mark.asyncio
    async def test_run_discovery_network_success(self):
        """Test that run_discovery works with a network."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = MagicMock()
            args.network = "192.168.1.0/24"
            args.output_dir = temp_dir
            args.template_dir = temp_dir
            args.format = "html"
            args.no_notification = True
            args.no_repository = True
            args.no_report = False

            # Create a template file for HTML reports
            os.makedirs(os.path.join(temp_dir, "templates"), exist_ok=True)
            with open(os.path.join(temp_dir, "templates", "layout.html"), "w") as f:
                f.write("<html>{{ devices }}</html>")

            # Mock the DeviceDiscoveryService
            with patch(
                "improvements.cli_improved.DeviceDiscoveryService"
            ) as mock_discovery_service:
                # Mock the discover_network method
                mock_instance = mock_discovery_service.return_value
                mock_instance.discover_network = AsyncMock()
                mock_instance.discover_network.return_value = []
                mock_instance.generate_report.return_value = os.path.join(
                    temp_dir, "devices.html"
                )

                # Run the discovery
                result = await run_discovery(args)

                # Check that discover_network was called with the correct arguments
                mock_instance.discover_network.assert_called_once_with("192.168.1.0/24")
                mock_instance.generate_report.assert_called_once_with("html")
                assert result == 0

    @pytest.mark.asyncio
    async def test_run_discovery_device_success(self):
        """Test that run_discovery works with a single device."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = MagicMock()
            args.network = "192.168.1.1"
            args.output_dir = temp_dir
            args.template_dir = temp_dir
            args.format = "html"
            args.no_notification = True
            args.no_repository = True
            args.no_report = False

            # Create a template file for HTML reports
            os.makedirs(os.path.join(temp_dir, "templates"), exist_ok=True)
            with open(os.path.join(temp_dir, "templates", "layout.html"), "w") as f:
                f.write("<html>{{ devices }}</html>")

            # Mock the DeviceDiscoveryService
            with patch(
                "improvements.cli_improved.DeviceDiscoveryService"
            ) as mock_discovery_service:
                # Mock the discover_device method
                mock_instance = mock_discovery_service.return_value
                mock_instance.discover_device = AsyncMock()
                mock_device = MagicMock()
                mock_device.status.return_value = "Device status"
                mock_instance.discover_device.return_value = mock_device
                mock_instance.generate_report.return_value = os.path.join(
                    temp_dir, "devices.html"
                )

                # Run the discovery
                result = await run_discovery(args)

                # Check that discover_device was called with the correct arguments
                mock_instance.discover_device.assert_called_once_with("192.168.1.1")
                mock_instance.generate_report.assert_called_once_with("html")
                assert result == 0

    @pytest.mark.asyncio
    async def test_run_discovery_invalid_network(self):
        """Test that run_discovery handles invalid networks."""
        args = MagicMock()
        args.network = "invalid"

        # Run the discovery
        result = await run_discovery(args)

        # Check that the function returned an error code
        assert result == 1

    @pytest.mark.asyncio
    async def test_run_discovery_email_missing_params(self):
        """Test that run_discovery validates email parameters."""
        args = MagicMock()
        args.network = "192.168.1.0/24"
        args.no_notification = False
        args.email = True
        args.smtp_username = None
        args.smtp_password = None
        args.email_recipient = None

        # Run the discovery
        result = await run_discovery(args)

        # Check that the function returned an error code
        assert result == 1

    @pytest.mark.asyncio
    async def test_run_discovery_html_missing_template(self):
        """Test that run_discovery validates template directory for HTML reports."""
        with tempfile.TemporaryDirectory() as temp_dir:
            args = MagicMock()
            args.network = "192.168.1.0/24"
            args.output_dir = temp_dir
            args.template_dir = "/nonexistent"
            args.format = "html"
            args.no_notification = True
            args.no_repository = True
            args.no_report = False

            # Run the discovery
            result = await run_discovery(args)

            # Check that the function returned an error code
            assert result == 1

    def test_cli_success(self):
        """Test that the CLI function works."""
        with patch("improvements.cli_improved.parse_args") as mock_parse_args:
            with patch("improvements.cli_improved.asyncio.run") as mock_run:
                # Setup mocks
                mock_parse_args.return_value = MagicMock()
                mock_run.return_value = 0

                # Run the CLI
                result = cli(["192.168.1.0/24"])

                # Check that asyncio.run was called
                mock_run.assert_called_once()
                assert result == 0

    def test_cli_keyboard_interrupt(self):
        """Test that the CLI function handles keyboard interrupts."""
        with patch("improvements.cli_improved.parse_args") as mock_parse_args:
            with patch("improvements.cli_improved.asyncio.run") as mock_run:
                # Setup mocks
                mock_parse_args.return_value = MagicMock()
                mock_run.side_effect = KeyboardInterrupt()

                # Run the CLI
                result = cli(["192.168.1.0/24"])

                # Check that the function returned the correct exit code
                assert result == 130

    def test_cli_unexpected_error(self):
        """Test that the CLI function handles unexpected errors."""
        with patch("improvements.cli_improved.parse_args") as mock_parse_args:
            with patch("improvements.cli_improved.asyncio.run") as mock_run:
                # Setup mocks
                mock_parse_args.return_value = MagicMock()
                mock_run.side_effect = Exception("Unexpected error")

                # Run the CLI
                result = cli(["192.168.1.0/24"])

                # Check that the function returned an error code
                assert result == 1
