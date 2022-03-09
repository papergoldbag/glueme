from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.db import models
from src.utils.methods import dt_to_utc


class TagService:

    @classmethod
    def by_title(cls, s: Session, *, title: str) -> models.Tag:
        title = title.strip().lower()
        return s.query(models.Tag).where(func.lower(models.Tag.title) == title).scalar()

    @classmethod
    def add_tag(cls, s: Session, *, title: str) -> models.Tag:
        title = title.strip().lower()
        tag = models.Tag(
            title=title,
            created=dt_to_utc(datetime.now())
        )
        s.add(tag)
        s.commit()
        return tag

