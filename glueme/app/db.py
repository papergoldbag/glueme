from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from .settings import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def new_session() -> Session:
    return SessionLocal()


def create_tables():
    from ..models import models
    models  # not to be removed when optimizing imports
    Base.metadata.create_all(bind=engine, checkfirst=True)
    logger.info('tables were created')


def recreate_tables():
    from ..models import models
    models  # not to be removed when optimizing imports
    Base.metadata.drop_all(bind=engine, checkfirst=True)
    Base.metadata.create_all(bind=engine, checkfirst=True)
    logger.info('tables were recreated')
