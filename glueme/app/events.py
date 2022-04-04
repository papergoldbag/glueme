from datetime import datetime

from sqlalchemy.orm import close_all_sessions

from glueme.app.db import create_tables, new_session
from glueme.app.settings import CodeTypes, DEFAULT_TAGS
from glueme.models import models
from glueme.utils.dtutc import dt_to_utc


def add_code_types():
    session = new_session()
    if not models.CodeType.type_exists(session, name=CodeTypes.REG):
        session.add(models.CodeType(name=CodeTypes.REG))
    session.commit()
    session.close()


def add_default_tags():
    session = new_session()
    for tag in DEFAULT_TAGS:
        if not models.Tag.title_exists(session, title=tag):
            session.add(models.Tag(
                title=tag,
                created=dt_to_utc(datetime.now())
            ))
    session.commit()
    session.close()


async def on_startup():
    create_tables()
    add_code_types()
    add_default_tags()


async def on_shutdown():
    close_all_sessions()
