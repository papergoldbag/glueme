from sqlalchemy.orm import close_all_sessions

from src.db.models import create_tables


async def on_startup():
    create_tables()


async def on_shutdown():
    close_all_sessions()
