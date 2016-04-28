import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


EMAILFROM = 'user@gmail.com'
EMAILTO = 'user@icloud.com'
USERNAME = 'user@gmail.com'
PASSWORD = 'password'
SMTP_SERVER = 'smtp.gmail.com:587'


def send(fileToSend):
    msg = MIMEMultipart()
    msg["From"] = EMAILFROM
    msg["To"] = EMAILTO
    msg["Subject"] = "Check for zenoss devices"
    msg.preamble = "Check for zenoss devices"

    text_part = MIMEText('Check for zenoss devices in attachment, please see it', 'plain')
    msg.attach(text_part)

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment",
                          filename=fileToSend)
    msg.attach(attachment)

    server = smtplib.SMTP(SMTP_SERVER)
    server.starttls()
    server.login(USERNAME, PASSWORD)
    server.sendmail(EMAILFROM, EMAILTO, msg.as_string())
    server.quit()
