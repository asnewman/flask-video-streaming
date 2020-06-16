import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
GMAIL_USERNAME = ''
GMAIL_PASSWORD = ''

class Emailer:
    def sendmail(self, recipient, subject, content):
        img_data = open('./1.jpg', 'rb').read()
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

sender = Emailer()

sendTo = ""
emailSubject = "Test email"
emailContent = "This is a test of my Emailer Class"

sender.sendmail(sendTo, emailSubject, emailContent)
