import os
import config
import platform
import smtplib
import subprocess

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Email:

    @staticmethod
    def send(title=None, body=None):
        email = MIMEMultipart()
        email["From"] = config.MAIL_FROM
        email["To"] = config.MAIL_RECEIVERS
        email["Subject"] = title

        part = MIMEText(body, 'html')
        email.attach(part)

        try:
            smtp = smtplib.SMTP(config.MAIL_SERVER)
            smtp.sendmail(email["To"], email["To"], email.as_string())
            smtp.quit()
        except Exception as error:
            return f"Error: {error}."

        return True
