"""Notification service implementations.

This module provides implementations of the NotificationService interface.

Supported notification channels:
- Email (SMTP)
- Console (stdout)
- Webhook (HTTP POST to Slack, Teams, Discord, generic endpoints)
"""

import json
import logging
import smtplib
import urllib.error
import urllib.request
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum
from typing import Any

from network_discovery.application.interfaces import NotificationService


# Setup logging
logger = logging.getLogger(__name__)


class WebhookType(Enum):
    """Supported webhook types."""

    SLACK = "slack"
    TEAMS = "teams"
    DISCORD = "discord"
    GENERIC = "generic"


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

        Raises:
            IOError: If there is an error writing to the console.
        """
        try:
            print(f"NOTIFICATION TO: {recipient}")
            print(f"SUBJECT: {subject}")
            print(f"MESSAGE: {message}")
            logger.info("Console notification sent to %s", recipient)
        except Exception as e:
            logger.error("Failed to send console notification: %s", e)
            raise


@dataclass
class WebhookConfig:
    """Configuration for webhook notifications."""

    url: str
    webhook_type: WebhookType = WebhookType.GENERIC
    username: str = "Network Discovery"
    icon_url: str = ""
    timeout: int = 10


class WebhookNotificationService(NotificationService):
    """Implementation of NotificationService using webhooks.

    Supports Slack, Microsoft Teams, Discord, and generic webhook endpoints.
    """

    def __init__(self, config: WebhookConfig) -> None:
        """Initialize the WebhookNotificationService.

        Args:
            config: Webhook configuration including URL and type.
        """
        self.config = config

    def _format_slack_payload(self, subject: str, message: str) -> dict[str, Any]:
        """Format message for Slack webhook.

        Args:
            subject: The notification subject.
            message: The notification message.

        Returns:
            Slack-formatted payload dictionary.
        """
        return {
            "username": self.config.username,
            "icon_url": self.config.icon_url or None,
            "attachments": [
                {
                    "color": "#36a64f",
                    "title": subject,
                    "text": message,
                    "footer": "Network Discovery Tool",
                    "ts": int(__import__("time").time()),
                }
            ],
        }

    def _format_teams_payload(self, subject: str, message: str) -> dict[str, Any]:
        """Format message for Microsoft Teams webhook.

        Args:
            subject: The notification subject.
            message: The notification message.

        Returns:
            Teams-formatted payload dictionary.
        """
        return {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": subject,
            "sections": [
                {
                    "activityTitle": subject,
                    "activitySubtitle": self.config.username,
                    "facts": [],
                    "markdown": True,
                    "text": message,
                }
            ],
        }

    def _format_discord_payload(self, subject: str, message: str) -> dict[str, Any]:
        """Format message for Discord webhook.

        Args:
            subject: The notification subject.
            message: The notification message.

        Returns:
            Discord-formatted payload dictionary.
        """
        return {
            "username": self.config.username,
            "avatar_url": self.config.icon_url or None,
            "embeds": [
                {
                    "title": subject,
                    "description": message,
                    "color": 3447003,  # Blue color
                    "footer": {"text": "Network Discovery Tool"},
                }
            ],
        }

    def _format_generic_payload(
        self, recipient: str, subject: str, message: str
    ) -> dict[str, Any]:
        """Format message for generic webhook.

        Args:
            recipient: The notification recipient.
            subject: The notification subject.
            message: The notification message.

        Returns:
            Generic payload dictionary.
        """
        return {
            "recipient": recipient,
            "subject": subject,
            "message": message,
            "source": "network-discovery",
            "timestamp": __import__("time").time(),
        }

    def send_notification(self, recipient: str, subject: str, message: str) -> None:
        """Send a notification via webhook.

        Args:
            recipient: The intended recipient (used in generic webhook).
            subject: The subject of the notification.
            message: The message content of the notification.

        Raises:
            urllib.error.URLError: If there is an error sending the webhook.
        """
        # Format payload based on webhook type
        if self.config.webhook_type == WebhookType.SLACK:
            payload = self._format_slack_payload(subject, message)
        elif self.config.webhook_type == WebhookType.TEAMS:
            payload = self._format_teams_payload(subject, message)
        elif self.config.webhook_type == WebhookType.DISCORD:
            payload = self._format_discord_payload(subject, message)
        else:
            payload = self._format_generic_payload(recipient, subject, message)

        try:
            data = json.dumps(payload).encode("utf-8")
            request = urllib.request.Request(
                self.config.url,
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "NetworkDiscovery/1.0",
                },
                method="POST",
            )

            with urllib.request.urlopen(
                request, timeout=self.config.timeout
            ) as response:
                if response.status not in (200, 201, 204):
                    logger.warning("Webhook returned status %d", response.status)

            logger.info(
                "Webhook notification sent to %s (%s)",
                self.config.url,
                self.config.webhook_type.value,
            )

        except urllib.error.HTTPError as e:
            logger.error("Webhook HTTP error: %d %s", e.code, e.reason)
            raise

        except urllib.error.URLError as e:
            logger.error("Webhook URL error: %s", e.reason)
            raise

        except Exception as e:
            logger.error("Failed to send webhook notification: %s", e)
            raise


class CompositeNotificationService(NotificationService):
    """Notification service that sends to multiple channels.

    Allows sending notifications to multiple services simultaneously.
    """

    def __init__(self, services: list[NotificationService]) -> None:
        """Initialize with a list of notification services.

        Args:
            services: List of notification services to use.
        """
        self.services = services

    def add_service(self, service: NotificationService) -> None:
        """Add a notification service.

        Args:
            service: The notification service to add.
        """
        self.services.append(service)

    def send_notification(self, recipient: str, subject: str, message: str) -> None:
        """Send a notification to all configured services.

        Args:
            recipient: The intended recipient.
            subject: The subject of the notification.
            message: The message content of the notification.

        Note:
            Failures in individual services are logged but don't prevent
            other services from receiving the notification.
        """
        errors = []
        for service in self.services:
            try:
                service.send_notification(recipient, subject, message)
            except Exception as e:
                logger.error(
                    "Failed to send via %s: %s",
                    type(service).__name__,
                    e,
                )
                errors.append((type(service).__name__, e))

        if errors and len(errors) == len(self.services):
            # All services failed
            raise RuntimeError(f"All notification services failed: {errors}")
