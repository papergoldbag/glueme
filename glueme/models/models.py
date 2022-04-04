from __future__ import annotations

from typing import Optional

from sqlalchemy import Column, Integer, Identity, VARCHAR, DateTime, String, ForeignKey, Boolean, or_, func
from sqlalchemy.orm import relationship, Session

from glueme.app.db import Base


class TagToUser(Base):
    __tablename__ = 'tagtouser'

    id = Column(Integer, Identity('by default'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tag.id', ondelete='CASCADE'), nullable=False)

    @classmethod
    def get_user_tag(cls, s: Session, *, tag_id: int, user_id: int) -> TagToUser:
        return s.query(cls).where(
            cls.tag_id == tag_id,
            cls.user_id == user_id
        ).scalar()


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, Identity('by default'), primary_key=True)
    title = Column(VARCHAR(63), nullable=False, unique=True)
    created = Column(DateTime(timezone=False), nullable=False)

    users = relationship(
        'User',
        secondary=TagToUser.__table__,
        back_populates="tags"
    )

    @classmethod
    def id_exists(cls, s: Session, *, _id: int) -> bool:
        return s.query(s.query(cls).where(cls.id == _id).exists()).scalar()

    @classmethod
    def title_exists(cls, s: Session, *, title: str) -> bool:
        return s.query(s.query(cls).where(cls.title == title).exists()).scalar()

    @classmethod
    def by_id(cls, s: Session, *, _id: int) -> Tag:
        return s.query(cls).where(cls.id == _id).scalar()

    @classmethod
    def by_title(cls, s: Session, *, title: str) -> Tag:
        title = title.strip().lower()
        return s.query(cls).where(func.lower(cls.title) == title).scalar()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nick = Column(VARCHAR(63), nullable=False, unique=True)
    name = Column(VARCHAR(31), nullable=False, default='')
    email = Column(VARCHAR(127), nullable=False, unique=True)
    password_hash = Column(VARCHAR(127), nullable=False)
    created = Column(DateTime(timezone=False), nullable=False)
    bio = Column(String(511), nullable=False, default='')

    tokens: list[UserToken] = relationship('UserToken', back_populates='user')
    tags: list[Tag] = relationship(
        'Tag',
        secondary=TagToUser.__table__,
        back_populates="users"
    )

    @classmethod
    def by_nick_or_email(cls, s: Session, *, nick_or_email: str) -> Optional[User]:
        return s.query(cls).where(or_(cls.nick == nick_or_email, cls.email == nick_or_email)).scalar()

    @classmethod
    def by_nick(cls, s: Session, *, nick: str) -> Optional[User]:
        return s.query(cls).where(cls.nick == nick).scalar()

    @classmethod
    def by_email(cls, s: Session, *, email: str) -> Optional[User]:
        return s.query(cls).where(cls.email == email).scalar()

    @classmethod
    def nick_exists(cls, s: Session, *, nick: str) -> bool:
        nick = nick.strip()
        return s.query(s.query(cls).where(cls.nick == nick).exists()).scalar()

    @classmethod
    def email_exists(cls, s: Session, *, email: str) -> bool:
        email = email.strip()
        return s.query(s.query(cls).where(cls.email == email).exists()).scalar()


class UserToken(Base):
    __tablename__ = 'usertoken'
    id = Column(Integer, Identity('by default'), primary_key=True)
    token = Column(VARCHAR(255), nullable=False, unique=True)
    user_agent = Column(VARCHAR(255), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False)

    user = relationship('User', back_populates='tokens')

    @classmethod
    def by_id(cls, s: Session, *, _id: int) -> Optional[Tag]:
        return s.query(cls).where(cls.id == _id).scalar()

    @classmethod
    def by_token(cls, s: Session, *, token: str) -> Optional[Tag]:
        return s.query(cls).where(cls.token == token).scalar()


class CodeType(Base):
    __tablename__ = 'codetype'
    name = Column(VARCHAR(31), primary_key=True, unique=True)

    @classmethod
    def type_exists(cls, s: Session, *, name: str) -> bool:
        return s.query(s.query(cls).where(cls.name == name).exists()).scalar()


class SentCode(Base):
    __tablename__ = 'sentcode'
    id = Column(Integer, Identity('by default'), primary_key=True)
    code = Column(VARCHAR(63), nullable=False)
    email = Column(VARCHAR(127), nullable=False)
    created = Column(DateTime(timezone=False), nullable=False)
    expired = Column(DateTime(timezone=False), nullable=False)
    is_used = Column(Boolean, nullable=False)
    code_type_name = Column(VARCHAR(31), ForeignKey(CodeType.name, ondelete='CASCADE'), nullable=False)

