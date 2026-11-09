import smtplib
import os

from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

from config import SMTP_SERVER, SMTP_PORT
load_dotenv()


SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def send_alert(user, process):

    subject = "🚨 Unauthorized Browser Activity"

    body = f"""
Unauthorized browser activity detected.

User     : {user}
Browser  : {process}
Time      : {datetime.now()}

Action Taken:
Browser was terminated automatically.
"""

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:

        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        )

        server.starttls()

        server.login(
            SENDER_EMAIL,
            APP_PASSWORD
        )

        server.send_message(msg)

        server.quit()

        print("📧 Alert Email Sent")

    except Exception as e:

        print("Email Error:", e)