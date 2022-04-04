import requests

from glueme.app.settings import MAILGUN_API_KEY, MAILGUN_DOMAIN


class Mailgun:
    @classmethod
    def send(cls, to_emails: list[str] or str, subject: str, text: str):
        if isinstance(to_emails, str):
            to_emails = [to_emails]
        res = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"<GlueMe@{MAILGUN_DOMAIN}>",
                "to": to_emails,
                "subject": subject,
                "text": text
            }
        )
        res.raise_for_status()

