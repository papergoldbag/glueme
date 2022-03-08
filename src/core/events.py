from src.db.models import create_tables


async def on_startup():
    create_tables()


async def on_shutdown():
    pass
