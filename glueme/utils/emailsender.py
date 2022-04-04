import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from glueme.app.settings import MAILRU_LOGIN, MAILRU_PASS


class EmailSender:
    @classmethod
    def send(cls, to_email: str, subject: str, text: str):
        fromaddr = MAILRU_LOGIN
        toaddr = to_email
        mypass = MAILRU_PASS

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject

        body = text
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        server.login(fromaddr, mypass)
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()
