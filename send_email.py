import smtplib
import ssl
import os

def send_email(receiver, message):
    host = "smtp.gmail.com"
    port = 465

    username = "khushitiwari0206@gmail.com"
    password = os.getenv("gmail_app_password")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        print("Login successful")
        server.sendmail(username, receiver, message)
        print("sendmail completed")

