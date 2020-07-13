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

        if platform.system() == 'Linux':
            sendmail_socket = subprocess.Popen(["/sbin/sendmail", "-t"], stdin=subprocess.PIPE)
            sendmail_socket.communicate(bytes(email.as_string(), 'utf8'))

        if platform.system() == 'Darwin':
            smtp = smtplib.SMTP('mail')
            smtp.sendmail(mailfrom, to, email.as_string())
            smtp.quit()

        return True
