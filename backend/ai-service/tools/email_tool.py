# tools/email_tool.py
import os
import smtplib
from email.mime.text import MIMEText
from crewai.tools import tool


@tool("SendEmailTool")
def send_email_tool(to: str, subject: str, body: str) -> str:
    """
    Send an email to the specified recipient via SMTP.

    Args:
        to: The recipient email address.
        subject: The email subject line.
        body: The full email body text.
    """
    sender = os.environ["GMAIL_SENDER"]
    password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["To"] = to
    msg["From"] = sender

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        return f"Email successfully sent to {to}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"
