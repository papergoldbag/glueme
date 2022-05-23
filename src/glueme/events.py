from datetime import datetime

from loguru import logger
from sqlalchemy.orm import close_all_sessions

from src.glueme import models
from src.glueme.db import new_session
from src.glueme.models import create_tables
from src.glueme.settings import DEFAULT_TAGS
from src.utils.dtutc import dt_to_utc


def _add_default_tags():
    session = new_session()
    for tag in DEFAULT_TAGS:
        if not models.Tag.title_exists(session, title=tag):
            session.add(models.Tag(
                title=tag,
                created=dt_to_utc(datetime.now())
            ))
    session.commit()
    session.close()
    logger.info('default tags were added')


async def on_startup():
    create_tables()
    models.CodeType.add_code_types(new_session())
    _add_default_tags()


async def on_shutdown():
    close_all_sessions()
