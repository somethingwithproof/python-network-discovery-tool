"""
Tests for the mail module.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from mail import (
    EmailConfig,
    EmailConfigError,
    EmailSender,
    EmailSendError,
    send,
)


class TestEmailConfig:
    """Tests for the EmailConfig dataclass."""

    def test_default_values(self):
        """Test default configuration values."""
        with patch.dict(os.environ, {}, clear=True):
            config = EmailConfig()
            assert config.email_from == ""
            assert config.email_to == ""
            assert config.username == ""
            assert config.password == ""
            assert config.smtp_server == "smtp.gmail.com:587"
            assert config.use_tls is True
            assert config.timeout == 30

    def test_from_environment(self):
        """Test configuration from environment variables."""
        env = {
            "EMAIL_FROM": "sender@example.com",
            "EMAIL_TO": "recipient@example.com",
            "EMAIL_USERNAME": "user",
            "EMAIL_PASSWORD": "secret",
            "EMAIL_SMTP_SERVER": "smtp.test.com:465",
        }
        with patch.dict(os.environ, env):
            config = EmailConfig()
            assert config.email_from == "sender@example.com"
            assert config.email_to == "recipient@example.com"
            assert config.username == "user"
            assert config.password == "secret"
            assert config.smtp_server == "smtp.test.com:465"

    def test_validate_success(self):
        """Test successful validation."""
        config = EmailConfig(
            email_from="sender@example.com",
            email_to="recipient@example.com",
            username="user",
            password="secret",
            smtp_server="smtp.test.com:587",
        )
        # Should not raise
        config.validate()

    def test_validate_missing_email_from(self):
        """Test validation fails without email_from."""
        config = EmailConfig(
            email_to="recipient@example.com",
            username="user",
            password="secret",
        )
        with pytest.raises(EmailConfigError, match="EMAIL_FROM"):
            config.validate()

    def test_validate_missing_email_to(self):
        """Test validation fails without email_to."""
        config = EmailConfig(
            email_from="sender@example.com",
            username="user",
            password="secret",
        )
        with pytest.raises(EmailConfigError, match="EMAIL_TO"):
            config.validate()

    def test_validate_missing_username(self):
        """Test validation fails without username."""
        config = EmailConfig(
            email_from="sender@example.com",
            email_to="recipient@example.com",
            password="secret",
        )
        with pytest.raises(EmailConfigError, match="EMAIL_USERNAME"):
            config.validate()

    def test_validate_missing_password(self):
        """Test validation fails without password."""
        config = EmailConfig(
            email_from="sender@example.com",
            email_to="recipient@example.com",
            username="user",
        )
        with pytest.raises(EmailConfigError, match="EMAIL_PASSWORD"):
            config.validate()

    def test_password_not_in_repr(self):
        """Test that password is not shown in repr."""
        config = EmailConfig(password="supersecret")
        assert "supersecret" not in repr(config)


class TestEmailSender:
    """Tests for the EmailSender class."""

    @pytest.fixture
    def valid_config(self) -> EmailConfig:
        """Create a valid email configuration."""
        return EmailConfig(
            email_from="sender@example.com",
            email_to="recipient@example.com",
            username="user",
            password="secret",
            smtp_server="smtp.test.com:587",
        )

    def test_init_with_config(self, valid_config: EmailConfig):
        """Test initialization with config object."""
        sender = EmailSender(config=valid_config)
        assert sender.config.email_from == "sender@example.com"

    def test_init_with_arguments(self):
        """Test initialization with explicit arguments."""
        sender = EmailSender(
            email_from="sender@example.com",
            email_to="recipient@example.com",
            username="user",
            password="secret",
        )
        assert sender.config.email_from == "sender@example.com"

    def test_send_email_file_not_found(self, valid_config: EmailConfig):
        """Test send_email with non-existent file."""
        sender = EmailSender(config=valid_config)
        with pytest.raises(FileNotFoundError):
            sender.send_email("/nonexistent/file.txt", "Test Subject")

    @patch("smtplib.SMTP")
    def test_send_email_success(
        self,
        mock_smtp,
        valid_config: EmailConfig,
        temp_dir: Path,
    ):
        """Test successful email sending."""
        # Create test file
        test_file = temp_dir / "test.txt"
        test_file.write_text("Test content")

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        sender = EmailSender(config=valid_config)
        sender.send_email(test_file, "Test Subject")

        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("user", "secret")
        mock_server.sendmail.assert_called_once()

    @patch("smtplib.SMTP")
    def test_send_email_with_body(
        self,
        mock_smtp,
        valid_config: EmailConfig,
        temp_dir: Path,
    ):
        """Test email sending with custom body."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Test content")

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        sender = EmailSender(config=valid_config)
        sender.send_email(test_file, "Test Subject", body="Custom body text")

        # Verify sendmail was called
        call_args = mock_server.sendmail.call_args
        message = call_args[0][2]
        assert "Custom body text" in message

    @patch("smtplib.SMTP")
    def test_send_email_smtp_error(
        self,
        mock_smtp,
        valid_config: EmailConfig,
        temp_dir: Path,
    ):
        """Test email sending handles SMTP errors."""
        import smtplib

        test_file = temp_dir / "test.txt"
        test_file.write_text("Test content")

        mock_server = MagicMock()
        mock_server.sendmail.side_effect = smtplib.SMTPException("SMTP error")
        mock_smtp.return_value.__enter__.return_value = mock_server

        sender = EmailSender(config=valid_config)
        with pytest.raises(EmailSendError, match="SMTP error"):
            sender.send_email(test_file, "Test Subject")

    def test_create_attachment_text(self, valid_config: EmailConfig, temp_dir: Path):
        """Test creating text file attachment."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Test content")

        sender = EmailSender(config=valid_config)
        attachment = sender._create_attachment(test_file)
        assert attachment["Content-Disposition"] is not None

    def test_create_attachment_binary(self, valid_config: EmailConfig, temp_dir: Path):
        """Test creating binary file attachment."""
        test_file = temp_dir / "test.bin"
        test_file.write_bytes(b"\x00\x01\x02\x03")

        sender = EmailSender(config=valid_config)
        attachment = sender._create_attachment(test_file)
        assert attachment["Content-Disposition"] is not None


class TestSendConvenienceFunction:
    """Tests for the send convenience function."""

    @patch("mail.EmailSender")
    def test_send_with_defaults(self, mock_sender_class, temp_dir: Path):
        """Test send function with default subject."""
        test_file = temp_dir / "report.xlsx"
        test_file.write_text("Test")

        mock_sender = MagicMock()
        mock_sender_class.return_value = mock_sender

        env = {
            "EMAIL_FROM": "sender@example.com",
            "EMAIL_TO": "recipient@example.com",
            "EMAIL_USERNAME": "user",
            "EMAIL_PASSWORD": "secret",
        }
        with patch.dict(os.environ, env):
            send(test_file)

        mock_sender.send_email.assert_called_once()
        call_args = mock_sender.send_email.call_args
        assert "report.xlsx" in call_args[0][1]  # Subject contains filename

    @patch("mail.EmailSender")
    def test_send_with_custom_subject(self, mock_sender_class, temp_dir: Path):
        """Test send function with custom subject."""
        test_file = temp_dir / "report.xlsx"
        test_file.write_text("Test")

        mock_sender = MagicMock()
        mock_sender_class.return_value = mock_sender

        env = {
            "EMAIL_FROM": "sender@example.com",
            "EMAIL_TO": "recipient@example.com",
            "EMAIL_USERNAME": "user",
            "EMAIL_PASSWORD": "secret",
        }
        with patch.dict(os.environ, env):
            send(test_file, subject="Custom Subject")

        mock_sender.send_email.assert_called_once()
        call_args = mock_sender.send_email.call_args
        assert call_args[0][1] == "Custom Subject"
