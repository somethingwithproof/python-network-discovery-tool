"""Tests for notification service implementations."""

import logging
import smtplib
from unittest.mock import patch, MagicMock, call

import pytest

from network_discovery.infrastructure.notification import (
    EmailNotificationService,
    ConsoleNotificationService,
)


@pytest.fixture
def email_notification_service():
    """Create an EmailNotificationService instance for testing."""
    return EmailNotificationService(
        smtp_server="smtp.example.com",
        smtp_port=587,
        username="test@example.com",
        password="password123"
    )


@pytest.fixture
def console_notification_service():
    """Create a ConsoleNotificationService instance for testing."""
    return ConsoleNotificationService()


class TestEmailNotificationService:
    """Tests for the EmailNotificationService class."""

    def test_init(self):
        """Test initializing EmailNotificationService with valid parameters."""
        service = EmailNotificationService(
            smtp_server="smtp.example.com",
            smtp_port=587,
            username="test@example.com",
            password="password123"
        )
        
        assert service.smtp_server == "smtp.example.com"
        assert service.smtp_port == 587
        assert service.username == "test@example.com"
        assert service.password == "password123"

    @patch('smtplib.SMTP')
    def test_send_notification_success(self, mock_smtp, email_notification_service):
        """Test successfully sending an email notification."""
        # Setup mock SMTP instance
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
        
        # Call send_notification
        email_notification_service.send_notification(
            recipient="recipient@example.com",
            subject="Test Subject",
            message="Test message content"
        )
        
        # Verify SMTP methods were called correctly
        mock_smtp.assert_called_once_with(
            email_notification_service.smtp_server,
            email_notification_service.smtp_port
        )
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with(
            email_notification_service.username,
            email_notification_service.password
        )
        mock_smtp_instance.sendmail.assert_called_once()
        
        # Verify sendmail arguments
        call_args = mock_smtp_instance.sendmail.call_args[0]
        assert call_args[0] == email_notification_service.username  # From
        assert call_args[1] == "recipient@example.com"  # To

    @patch('smtplib.SMTP')
    def test_send_notification_with_formatted_message(self, mock_smtp, email_notification_service):
        """Test sending an email with special formatting."""
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
        
        # Call send_notification with HTML-like content in message
        email_notification_service.send_notification(
            recipient="recipient@example.com",
            subject="Test Subject",
            message="Line 1\nLine 2\n<b>Bold Text</b>"
        )
        
        # Verify MIME message was created correctly (should still be treated as plain text)
        call_args = mock_smtp_instance.sendmail.call_args[0]
        mime_msg = call_args[2]  # The MIME message as string
        assert "Content-Type: text/plain" in mime_msg
        assert "Line 1" in mime_msg
        assert "Line 2" in mime_msg
        assert "<b>Bold Text</b>" in mime_msg

    @patch('smtplib.SMTP')
    def test_send_notification_smtp_error(self, mock_smtp, email_notification_service):
        """Test handling SMTP errors when sending an email notification."""
        # Setup mock to raise an SMTP error
        mock_smtp.return_value.__enter__.side_effect = smtplib.SMTPException("Connection error")
        
        # Call send_notification and expect it to raise the exception
        with pytest.raises(smtplib.SMTPException):
            email_notification_service.send_notification(
                recipient="recipient@example.com",
                subject="Test Subject",
                message="Test message content"
            )

    @patch('smtplib.SMTP')
    def test_send_notification_auth_error(self, mock_smtp, email_notification_service):
        """Test handling authentication errors when sending an email notification."""
        # Setup mock instance
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
        
        # Make login raise an authentication error
        mock_smtp_instance.login.side_effect = smtplib.SMTPAuthenticationError(535, "Authentication failed")
        
        # Call send_notification and expect it to raise the exception
        with pytest.raises(smtplib.SMTPAuthenticationError):
            email_notification_service.send_notification(
                recipient="recipient@example.com",
                subject="Test Subject",
                message="Test message content"
            )


class TestConsoleNotificationService:
    """Tests for the ConsoleNotificationService class."""

    def test_send_notification(self, console_notification_service, capfd):
        """Test sending a notification to the console."""
        # Call send_notification
        console_notification_service.send_notification(
            recipient="admin",
            subject="Test Console Subject",
            message="Test console message"
        )
        
        # Capture the stdout output
        out, err = capfd.readouterr()
        
        # Verify the output contains the expected content
        assert "NOTIFICATION TO: admin" in out
        assert "SUBJECT: Test Console Subject" in out
        assert "MESSAGE: Test console message" in out

    def test_send_notification_with_special_characters(self, console_notification_service, capfd):
        """Test sending a console notification with special characters."""
        # Call send_notification with special characters
        console_notification_service.send_notification(
            recipient="admin",
            subject="Test with 🔥 emoji",
            message="Line 1\nLine 2\nSpecial chars: äöü"
        )
        
        # Capture the stdout output
        out, err = capfd.readouterr()
        
        # Verify the output contains the expected content including special characters
        assert "Test with 🔥 emoji" in out
        assert "Special chars: äöü" in out

    @patch('builtins.print')
    def test_send_notification_print_error(self, mock_print, console_notification_service):
        """Test handling errors when printing to console."""
        # Setup mock to raise an error
        mock_print.side_effect = IOError("Print error")
        
        # Call send_notification with logging capture
        with patch('network_discovery.infrastructure.notification.logger') as mock_logger:
            with pytest.raises(IOError):
                console_notification_service.send_notification(
                    recipient="admin",
                    subject="Test Subject",
                    message="Test message"
                )
            
            # Verify error was logged
            mock_logger.error.assert_called_once()
            assert "Failed to send" in mock_logger.error.call_args[0][0]


class TestNotificationIntegration:
    """Integration tests for notification services."""

    @patch('smtplib.SMTP')
    def test_email_notification_real_message(self, mock_smtp):
        """Test email notification with a realistic message."""
        # Setup service
        service = EmailNotificationService(
            smtp_server="smtp.company.com",
            smtp_port=587,
            username="alerts@company.com",
            password="secure-password"
        )
        
        # Setup mock SMTP instance
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
        
        # Create a network discovery report message
        message = """
Network Discovery Complete

Scan Summary:
- Total devices scanned: 150
- Alive devices: 142
- Devices with SNMP: 98
- Devices with SSH: 115
- Devices with database services: 24

Critical devices requiring attention:
- 192.168.1.10 (Primary Router): SNMP service not responding
- 192.168.1.50 (Database Server): High CPU load detected

For complete details, see the attached report.
"""
        
        # Send notification
        service.send_notification(
            recipient="network-team@company.com",
            subject="Network Discovery Report - 10 Critical Issues Found",
            message=message
        )
        
        # Verify SMTP was called with appropriate parameters
        mock_smtp.assert_called_once_with("smtp.company.com", 587)
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once()
        mock_smtp_instance.sendmail.assert_called_once()
        
        # Check message content in the call
        call_args = mock_smtp_instance.sendmail.call_args[0]
        assert call_args[0] == "alerts@company.com"  # From
        assert call_args[1] == "network-team@company.com"  # To
        assert "Network Discovery Report" in call_args[2]  # Subject in message string
        assert "Total devices scanned: 150" in call_args[2]  # Content in message string

