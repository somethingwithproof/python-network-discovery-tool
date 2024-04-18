import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Setup logging
logger = logging.getLogger(__name__)

class MailSender:
    """Handles sending emails."""

    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, to_address: str, subject: str, body: str) -> None:
        """Sends an email."""
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.username, to_address, msg.as_string())
            logger.info(f"Email sent to {to_address}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
