from __future__ import annotations

from sqlalchemy import Column, Integer, Identity, VARCHAR, DateTime, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.db.base import Base, engine


class UserTags(Base):
    __tablename__ = 'user_tags'

    id = Column(Integer, Identity('by default'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id', ondelete='CASCADE'), nullable=False)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, Identity('by default'), primary_key=True)
    tag = Column(VARCHAR(63), nullable=False, unique=True)
    created = Column(DateTime(timezone=False), nullable=False)

    users = relationship(
        'User',
        secondary=UserTags.__table__,
        back_populates="tags"
    )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nick = Column(VARCHAR(63), nullable=False, unique=True)
    name = Column(VARCHAR(31))
    email = Column(VARCHAR(127), nullable=False, unique=True)
    password_hash = Column(VARCHAR(127), nullable=False)
    created = Column(DateTime(timezone=False), nullable=False)
    bio = Column(String(511))

    tokens = relationship('UserToken', back_populates='user')
    tags = relationship(
        'Tag',
        secondary=UserTags.__table__,
        back_populates="users"
    )


class UserToken(Base):
    __tablename__ = 'user_tokens'
    id = Column(Integer, Identity('by default'), primary_key=True)
    token = Column(VARCHAR(255), nullable=False, unique=True)
    user_agent = Column(VARCHAR(255), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False)

    user = relationship('User', back_populates='tokens')


class Codes(Base):
    __tablename__ = 'codes'
    id = Column(Integer, Identity('by default'), primary_key=True)
    code = Column(VARCHAR(63), nullable=False)
    email = Column(VARCHAR(127), nullable=False)
    created = Column(DateTime(timezone=False), nullable=False)
    expired = Column(DateTime(timezone=False), nullable=False)
    is_active = Column(Boolean, nullable=False)


def create_tables():
    Base.metadata.create_all(bind=engine, checkfirst=True)


def recreate_tables():
    Base.metadata.drop_all(bind=engine, checkfirst=True)
    Base.metadata.create_all(bind=engine, checkfirst=True)


if __name__ == '__main__':
    recreate_tables()
