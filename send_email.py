import smtplib
import ssl
import os
from email.message import EmailMessage


def send_email(receiver, message, html):
    host = "smtp.gmail.com"
    port = 465

    username = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("gmail_app_password")

    msg = EmailMessage()
    msg["Subject"] = "📰 AI-Powered Daily News Digest"
    msg["From"] = username
    msg["To"] = receiver

    # Plain text version
    msg.set_content(message)

    # HTML version
    msg.add_alternative(html, subtype="html")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        print("Login successful")

        server.send_message(msg)

        print("sendmail completed")

def send_otp_email(receiver, otp):
    host = "smtp.gmail.com"
    port = 465

    username = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("gmail_app_password")

    msg = EmailMessage()
    msg["Subject"] = "🔐 Verify Your Email"
    msg["From"] = username
    msg["To"] = receiver

    text = f"""
Hello,

Your verification code is:

{otp}

This OTP is valid for 5 minutes.

If you didn't request this, please ignore this email.
"""

    html = f"""
    <html>
        <body style="font-family:Arial,sans-serif;background:#f4f4f4;padding:30px;">
            <div style="max-width:500px;background:white;padding:30px;border-radius:10px;margin:auto;">
                <h2 style="color:#2563EB;">Email Verification</h2>

                <p>Your One-Time Password (OTP) is:</p>

                <h1 style="letter-spacing:5px;color:#10B981;">
                    {otp}
                </h1>

                <p>This OTP is valid for <b>5 minutes</b>.</p>

                <p>If you didn't request this verification, you can safely ignore this email.</p>
            </div>
        </body>
    </html>
    """

    msg.set_content(text)
    msg.add_alternative(html, subtype="html")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.send_message(msg)        