'''Send emails with stocks predictions'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config

class Email:
    '''
    Email Class
    '''
    @staticmethod
    def send(title=None, body=None):
        '''
        Sends email
        :param title: String wiht title of the email
        :param body: Message string
        :return:
        '''
        email = MIMEMultipart()
        email["From"] = config.MAIL_FROM
        email["To"] = config.MAIL_RECEIVERS
        email["Subject"] = title

        part = MIMEText(body, 'html')
        email.attach(part)

        try:
            smtp = smtplib.SMTP(config.MAIL_SERVER)
            smtp.sendmail(email["To"], email["To"], email.as_string())
        except smtplib .SMTPHeloError as error:
            return f"Error: {error}."
        finally:
            smtp.quit()

        return True
