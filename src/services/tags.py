from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.db import models
from src.utils.methods import dt_to_utc


class TagService:
    @classmethod
    def by_id(cls, s: Session, *, _id: int) -> models.Tag:
        return s.query(models.Tag).where(models.Tag.id == _id).scalar()

    @classmethod
    def by_title(cls, s: Session, *, title: str) -> models.Tag:
        title = title.strip().lower()
        return s.query(models.Tag).where(func.lower(models.Tag.title) == title).scalar()

    @classmethod
    def add_tag(cls, s: Session, *, title: str) -> models.Tag:
        title = title.strip()
        tag = models.Tag(
            title=title,
            created=dt_to_utc(datetime.now())
        )
        s.add(tag)
        s.commit()
        return tag

    @classmethod
    def tag_id_exists(cls, s: Session, *, _id: int) -> bool:
        return s.query(s.query(models.Tag).where(models.Tag.id == _id).exists()).scalar()

    @classmethod
    def search_tag(cls, s: Session, *, q: str) -> list[models.Tag]:
        q = q.strip().lower()
        res = s.query(models.Tag).filter(func.lower(models.Tag.title).like(f'{q}%')).all()
        return res
