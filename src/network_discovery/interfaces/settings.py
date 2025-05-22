"""Settings management for the network discovery tool.

This module defines the Settings class which is used to manage configuration
settings for the network discovery tool, using Pydantic for validation.
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration settings for the network discovery tool.

    This class uses Pydantic to define and validate configuration settings,
    with support for environment variables and .env files.

    Attributes:
        network: Network CIDR or single IP address to scan.
        output_dir: Directory where reports will be saved.
        format: Format for generated reports (html, csv, xlsx, json).
        template_dir: Directory containing HTML templates.
        verbose: Whether to enable verbose logging.
        no_report: Whether to disable report generation.
        no_notification: Whether to disable notifications.
        no_repository: Whether to disable device storage.
        repository_file: File where device data will be stored.
        email: Whether to enable email notifications.
        smtp_server: SMTP server for email notifications.
        smtp_port: SMTP port for email notifications.
        smtp_username: SMTP username for email notifications.
        smtp_password: SMTP password for email notifications.
        email_recipient: Email address to send notifications to.
    """

    network: str
    output_dir: Path = Field(
        default=Path("./output"), description="Directory for reports"
    )
    format: str = Field(
        default="html",
        description="Report format",
        pattern="^(html|csv|xlsx|json)$",
    )
    template_dir: Path = Field(
        default=Path("./templates"), description="Template directory"
    )
    verbose: bool = False
    no_report: bool = False
    no_notification: bool = False
    no_repository: bool = False
    repository_file: Path = Field(default=Path("./devices.json"))
    email: bool = False
    smtp_server: str = Field(default="smtp.gmail.com")
    smtp_port: int = Field(default=587)
    smtp_username: str = ""
    smtp_password: str = ""
    email_recipient: str = ""

    model_config = {"env_file": ".env", "case_sensitive": False}
