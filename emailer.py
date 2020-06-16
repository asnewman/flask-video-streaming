import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os
import picamera
import datetime

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

GMAIL_USERNAME = os.getenv("SENDER_EMAIL")
GMAIL_PASSWORD = os.getenv("SENDER_EMAIL_PASSWORD")

class Emailer:
    def sendmail(self, recipient, subject, image_location):
        img_data = open(image_location, 'rb').read()

        image = MIMEImage(img_data, name='test.jpg')

        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = GMAIL_USERNAME
        msg["To"] = recipient
        msg.attach(image)

        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()

        #Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
        #Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, msg.as_string())
        session.quit

