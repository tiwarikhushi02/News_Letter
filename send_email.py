import smtplib
import ssl
import os
from email.message import EmailMessage


def send_email(receiver, message):
    host = "smtp.gmail.com"
    port = 465

    username = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("gmail_app_password")

    msg = EmailMessage()
    msg["Subject"] = "📰 AI-Powered Daily News Digest"
    msg["From"] = username
    msg["To"] = receiver

    # Plain text fallback
    msg.set_content(message)

    # HTML version
    html = f"""
    <html>
        <body>
            <h1>📰 AI-Powered Daily News Digest</h1>

            <pre>{message}</pre>

            <hr>

            <p>
                <a href="http://127.0.0.1:8000/unsubscribe">
                    Unsubscribe
                </a>
            </p>
        </body>
    </html>
    """

    msg.add_alternative(html, subtype="html")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        print("Login successful")

        server.send_message(msg)

        print("sendmail completed")