import os
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class EmailSender:
    def __init__(self, email_from, email_to, username, password, smtp_server):
        self.email_from = email_from
        self.email_to = email_to
        self.username = username
        self.password = password
        self.smtp_server = smtp_server

    def send_email(self, file_to_send, subject):
        if not os.path.isfile(file_to_send):
            raise ValueError('Invalid file path')

        if not self.email_from:
            raise ValueError('Missing sender email')

        if not self.email_to:
            raise ValueError('Missing recipient email')

        if not self.username:
            raise ValueError('Missing email username')

        if not self.password:
            raise ValueError('Missing email password')

        if not self.smtp_server:
            raise ValueError('Missing SMTP server information')

        msg = MIMEMultipart()
        msg["From"] = self.email_from
        msg["To"] = self.email_to
        msg["Subject"] = subject
        msg.preamble = subject

        text_part = MIMEText('Check for zenoss devices in attachment, please see it', 'plain')
        msg.attach(text_part)

        ctype, encoding = mimetypes.guess_type(file_to_send)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        with open(file_to_send, 'rb') as fp:
            if maintype == "text":
                attachment = MIMEText(fp.read(), _subtype=subtype)
            elif maintype == "image":
                attachment = MIMEImage(fp.read(), _subtype=subtype)
            elif maintype == "audio":
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
            else:
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                encoders.encode_base64(attachment)

        attachment.add_header("Content-Disposition", "attachment", filename=file_to_send)
        msg.attach(attachment)

        with smtplib.SMTP(self.smtp_server) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.email_from, self.email_to, msg.as_string())


if __name__ == '__main__':
    email_sender = EmailSender(email_from='user@gmail.com',
                               email_to='user@icloud.com',
                               username='user@gmail.com',
                               password='password',
                               smtp_server='smtp.gmail.com:587')

    email_sender.send_email(file_to_send='path/to/file',
                            subject='Check for zenoss devices')
