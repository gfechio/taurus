import platform
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os

class Email:

    @staticmethod
    def send(mailfrom='taurus@localhost', to=None, title=None, body=None):
        email = MIMEMultipart()
        email["From"] = mailfrom
        email["To"] = to
        email["Subject"] = title

        part = MIMEText(body, 'html')
        email.attach(part)

        try:
            smtp = smtplib.SMTP('localhost')
            smtp.sendmail(mailfrom, to, email.as_string())
            smtp.quit()
        except Exception as error:
            return f"Error: {error}."

        return True
