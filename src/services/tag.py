from sqlalchemy import func
from sqlalchemy.orm import Session

from src.glueme import models


class TagService:
    @classmethod
    def search_tags(cls, s: Session, *, q: str) -> list[models.Tag]:
        q = q.strip().lower()
        res = s.query(models.Tag).where(func.lower(models.Tag.title).like(f'{q}%')).all()
        return res
