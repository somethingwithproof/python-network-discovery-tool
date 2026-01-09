"""
Email sending module for network discovery reports.

This module provides functionality for sending scan results via email
with file attachments.

Requires Python 3.12+
"""

from __future__ import annotations

import logging
import mimetypes
import os
import smtplib
from dataclasses import dataclass, field
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import StrEnum, auto
from pathlib import Path

# Type aliases using Python 3.12+ syntax
type FilePath = str | Path
type EmailAddress = str

logger = logging.getLogger(__name__)


class EmailErrorType(StrEnum):
    """Types of email errors."""

    CONFIG = auto()
    SEND = auto()
    CONNECTION = auto()


class EmailConfigError(Exception):
    """Raised when email configuration is invalid."""

    __slots__ = ("error_type", "field")

    def __init__(
        self,
        message: str,
        *,
        field: str | None = None,
        error_type: EmailErrorType = EmailErrorType.CONFIG,
    ) -> None:
        super().__init__(message)
        self.field = field
        self.error_type = error_type


class EmailSendError(Exception):
    """Raised when email sending fails."""

    __slots__ = ("error_type", "recipient")

    def __init__(
        self,
        message: str,
        *,
        recipient: str | None = None,
        error_type: EmailErrorType = EmailErrorType.SEND,
    ) -> None:
        super().__init__(message)
        self.recipient = recipient
        self.error_type = error_type


@dataclass(slots=True, kw_only=True)
class EmailConfig:
    """
    Email configuration loaded from environment variables.

    Environment variables:
        EMAIL_FROM: Sender email address
        EMAIL_TO: Recipient email address
        EMAIL_USERNAME: SMTP authentication username
        EMAIL_PASSWORD: SMTP authentication password
        EMAIL_SMTP_SERVER: SMTP server address (host:port)
    """

    email_from: EmailAddress = field(default_factory=lambda: os.environ.get("EMAIL_FROM", ""))
    email_to: EmailAddress = field(default_factory=lambda: os.environ.get("EMAIL_TO", ""))
    username: str = field(default_factory=lambda: os.environ.get("EMAIL_USERNAME", ""))
    password: str = field(
        default_factory=lambda: os.environ.get("EMAIL_PASSWORD", ""),
        repr=False,  # Don't show password in repr
    )
    smtp_server: str = field(
        default_factory=lambda: os.environ.get("EMAIL_SMTP_SERVER", "smtp.gmail.com:587")
    )
    use_tls: bool = True
    timeout: int = 30

    def validate(self) -> None:
        """
        Validate that all required configuration is present.

        Raises:
            EmailConfigError: If any required configuration is missing
        """
        required_fields = {
            "email_from": ("EMAIL_FROM", self.email_from),
            "email_to": ("EMAIL_TO", self.email_to),
            "username": ("EMAIL_USERNAME", self.username),
            "password": ("EMAIL_PASSWORD", self.password),
            "smtp_server": ("EMAIL_SMTP_SERVER", self.smtp_server),
        }

        for field_name, (env_var, value) in required_fields.items():
            if not value:
                raise EmailConfigError(
                    f"Missing {env_var} environment variable",
                    field=field_name,
                )

    @property
    def smtp_host(self) -> str:
        """Extract SMTP host from server string."""
        return self.smtp_server.split(":")[0]

    @property
    def smtp_port(self) -> int:
        """Extract SMTP port from server string."""
        parts = self.smtp_server.split(":")
        return int(parts[1]) if len(parts) > 1 else 587


@dataclass(slots=True, frozen=True)
class AttachmentInfo:
    """Information about an email attachment."""

    path: Path
    mime_type: str
    main_type: str
    sub_type: str

    @classmethod
    def from_path(cls, file_path: Path) -> AttachmentInfo:
        """Create AttachmentInfo from a file path."""
        ctype, encoding = mimetypes.guess_type(str(file_path))

        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        main_type, sub_type = ctype.split("/", 1)

        return cls(
            path=file_path,
            mime_type=ctype,
            main_type=main_type,
            sub_type=sub_type,
        )


class EmailSender:
    """
    Sends emails with file attachments.

    Can be initialized with explicit configuration or use environment variables.
    """

    __slots__ = ("_config",)

    def __init__(
        self,
        *,
        email_from: EmailAddress | None = None,
        email_to: EmailAddress | None = None,
        username: str | None = None,
        password: str | None = None,
        smtp_server: str | None = None,
        config: EmailConfig | None = None,
    ) -> None:
        """
        Initialize EmailSender.

        Args:
            email_from: Sender email address (or use EMAIL_FROM env var)
            email_to: Recipient email address (or use EMAIL_TO env var)
            username: SMTP username (or use EMAIL_USERNAME env var)
            password: SMTP password (or use EMAIL_PASSWORD env var)
            smtp_server: SMTP server address (or use EMAIL_SMTP_SERVER env var)
            config: Pre-configured EmailConfig object (overrides other args)
        """
        match config:
            case EmailConfig():
                self._config = config
            case None:
                self._config = EmailConfig(
                    email_from=email_from or os.environ.get("EMAIL_FROM", ""),
                    email_to=email_to or os.environ.get("EMAIL_TO", ""),
                    username=username or os.environ.get("EMAIL_USERNAME", ""),
                    password=password or os.environ.get("EMAIL_PASSWORD", ""),
                    smtp_server=smtp_server
                    or os.environ.get("EMAIL_SMTP_SERVER", "smtp.gmail.com:587"),
                )

    @property
    def config(self) -> EmailConfig:
        """Get the email configuration."""
        return self._config

    def send_email(
        self,
        file_to_send: FilePath,
        subject: str,
        body: str | None = None,
    ) -> None:
        """
        Send an email with a file attachment.

        Args:
            file_to_send: Path to the file to attach
            subject: Email subject line
            body: Optional email body text

        Raises:
            EmailConfigError: If configuration is invalid
            EmailSendError: If sending fails
            FileNotFoundError: If attachment file doesn't exist
        """
        self._config.validate()

        file_path = Path(file_to_send)
        if not file_path.is_file():
            raise FileNotFoundError(f"Attachment file not found: {file_path}")

        msg = self._build_message(file_path, subject, body)

        try:
            self._send_smtp(msg)
            logger.info("Email sent successfully to %s", self._config.email_to)
        except smtplib.SMTPException as e:
            logger.error("Failed to send email: %s", e)
            raise EmailSendError(
                f"Failed to send email: {e}",
                recipient=self._config.email_to,
                error_type=EmailErrorType.SEND,
            ) from e
        except OSError as e:
            logger.error("Connection error: %s", e)
            raise EmailSendError(
                f"Connection error: {e}",
                error_type=EmailErrorType.CONNECTION,
            ) from e

    def _build_message(
        self,
        file_path: Path,
        subject: str,
        body: str | None,
    ) -> MIMEMultipart:
        """Build the email message with attachment."""
        msg = MIMEMultipart()
        msg["From"] = self._config.email_from
        msg["To"] = self._config.email_to
        msg["Subject"] = subject

        # Add body text
        body_text = body or f"Please find the attached file: {file_path.name}"
        msg.attach(MIMEText(body_text, "plain"))

        # Add attachment
        attachment = self._create_attachment(file_path)
        msg.attach(attachment)

        return msg

    def _create_attachment(self, file_path: Path) -> MIMEBase:
        """Create a MIME attachment from a file."""
        info = AttachmentInfo.from_path(file_path)

        with file_path.open("rb") as fp:
            file_data = fp.read()

        # Use pattern matching to create appropriate MIME type
        attachment = self._create_mime_part(info, file_data)

        attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename=file_path.name,
        )

        return attachment

    def _create_mime_part(
        self,
        info: AttachmentInfo,
        file_data: bytes,
    ) -> MIMEBase:
        """Create the appropriate MIME part based on content type."""
        match info.main_type:
            case "text":
                return MIMEText(
                    file_data.decode(errors="replace"),
                    _subtype=info.sub_type,
                )
            case "image":
                return MIMEImage(file_data, _subtype=info.sub_type)
            case "audio":
                return MIMEAudio(file_data, _subtype=info.sub_type)
            case _:
                attachment = MIMEBase(info.main_type, info.sub_type)
                attachment.set_payload(file_data)
                encoders.encode_base64(attachment)
                return attachment

    def _send_smtp(self, msg: MIMEMultipart) -> None:
        """Send the message via SMTP."""
        with smtplib.SMTP(
            self._config.smtp_host,
            self._config.smtp_port,
            timeout=self._config.timeout,
        ) as server:
            if self._config.use_tls:
                server.starttls()
            server.login(self._config.username, self._config.password)
            server.sendmail(
                self._config.email_from,
                self._config.email_to,
                msg.as_string(),
            )


def send(file_path: FilePath, subject: str | None = None) -> None:
    """
    Convenience function to send an email with default configuration.

    Uses environment variables for email configuration.

    Args:
        file_path: Path to the file to attach
        subject: Email subject (defaults to filename-based subject)

    Raises:
        EmailConfigError: If required environment variables are missing
        EmailSendError: If sending fails
    """
    path = Path(file_path)
    email_subject = subject or f"Network Scan Results: {path.name}"

    sender = EmailSender()
    sender.send_email(path, email_subject)


if __name__ == "__main__":
    import sys

    # Example usage - requires environment variables to be set:
    # export EMAIL_FROM="sender@example.com"
    # export EMAIL_TO="recipient@example.com"
    # export EMAIL_USERNAME="sender@example.com"
    # export EMAIL_PASSWORD="your-app-password"
    # export EMAIL_SMTP_SERVER="smtp.gmail.com:587"

    print("Email sender module")
    print()
    print("Required environment variables:")
    print("  EMAIL_FROM       - Sender email address")
    print("  EMAIL_TO         - Recipient email address")
    print("  EMAIL_USERNAME   - SMTP authentication username")
    print("  EMAIL_PASSWORD   - SMTP authentication password")
    print("  EMAIL_SMTP_SERVER - SMTP server (default: smtp.gmail.com:587)")
    print()

    if len(sys.argv) > 1:
        file_to_send = sys.argv[1]
        cli_subject = sys.argv[2] if len(sys.argv) > 2 else None

        try:
            send(file_to_send, cli_subject)
            print(f"Email sent successfully with attachment: {file_to_send}")
        except (EmailConfigError, EmailSendError, FileNotFoundError) as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print("Usage: python mail.py <file_to_send> [subject]")
