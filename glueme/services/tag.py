from sqlalchemy import func
from sqlalchemy.orm import Session

from glueme.models import models


class TagService:
    @classmethod
    def search_tags(cls, s: Session, *, q: str) -> list[models.Tag]:
        q = q.strip().lower()
        res = s.query(models.Tag).filter(func.lower(models.Tag.title).like(f'{q}%')).all()
        return res
