"""Notification service implementations.

This module provides implementations of the NotificationService interface.
"""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from network_discovery.application.interfaces import NotificationService

# Setup logging
logger = logging.getLogger(__name__)


class EmailNotificationService(NotificationService):
    """Implementation of NotificationService using email."""

    def __init__(
        self, smtp_server: str, smtp_port: int, username: str, password: str
    ) -> None:
        """Initialize a new EmailNotificationService.

        Args:
            smtp_server: The SMTP server address.
            smtp_port: The SMTP server port.
            username: The SMTP username.
            password: The SMTP password.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_notification(self, recipient: str, subject: str, message: str) -> None:
        """Send a notification via email.

        Args:
            recipient: The email address of the recipient.
            subject: The subject of the email.
            message: The message content of the email.
        """
        msg = MIMEMultipart()
        msg["From"] = self.username
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.username, recipient, msg.as_string())
            logger.info("Email sent to %s", recipient)
        except Exception as e:
            logger.error("Failed to send email: %s", e)
            raise


class ConsoleNotificationService(NotificationService):
    """Implementation of NotificationService using console output."""

    def send_notification(self, recipient: str, subject: str, message: str) -> None:
        """Send a notification to the console.

        Args:
            recipient: The intended recipient (ignored).
            subject: The subject of the notification.
            message: The message content of the notification.
        """
        print(f"NOTIFICATION TO: {recipient}")
        print(f"SUBJECT: {subject}")
        print(f"MESSAGE: {message}")
        logger.info("Console notification sent to %s", recipient)
