from requests import Session

from src.core.settings import settings


class EmailSender:
    session = Session()

    @classmethod
    def send(cls, to_emails: list[str], subject: str, text: str):
        res = cls.session.post(
            f"https://api.mailgun.net/v3/{settings.mailgun_domain}/messages",
            auth=("api", settings.mailgun_api_key),
            data={
                "from": f"<GlueMe@{settings.mailgun_domain}>",
                "to": to_emails,
                "subject": subject,
                "text": text
            }
        )
        res.raise_for_status()

