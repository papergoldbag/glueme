import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.glueme.settings import MAILRU_LOGIN, MAILRU_PASS, MAILRU_SERVER, MAILRU_PORT


def send_mail(to_email: str, subject: str, text: str):
    toaddr = to_email

    msg = MIMEMultipart()
    msg['From'] = MAILRU_LOGIN
    msg['To'] = toaddr
    msg['Subject'] = subject

    body = text
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL(MAILRU_SERVER, MAILRU_PORT)
    server.login(MAILRU_LOGIN, MAILRU_PASS)
    server.sendmail(MAILRU_LOGIN, toaddr, msg.as_string())
    server.quit()
