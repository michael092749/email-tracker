import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import cred
import ssl
import os
import urllib.parse

from twilio.rest import Client
from pathlib import Path

def send_email_with_tracking(recipient_email, subject, tracking_url):
    sender_email = cred.my_email
    sender_password = cred.my_password

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    encoded_email = urllib.parse.quote(recipient_email)

    text = ""
    html = f"""\
    <html>
      <body>
        <p>Hi,<br>
           The email body here.<br>
           <img src="{tracking_url}?email={encoded_email}&campaign={subject}" alt="Tracking Pixel">
        </p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(cred.my_email, cred.my_password) 
        server.sendmail(cred.my_email, recipient_email, message.as_string())

def main():
    tracking_url = "http://IP/tracking-pixel"
    recipient = "michaelantunes77@gmail.com"
    subject = "Money Balls"
    send_email_with_tracking(recipient, subject, tracking_url)

if __name__== "__main__":
    main()
