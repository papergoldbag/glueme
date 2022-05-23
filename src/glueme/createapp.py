import sys

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from .events import on_startup, on_shutdown
from .settings import LOG_PATH, TITLE, API_PREFIX
from ..api.router import api_router


def init_loguru():
    logger.remove(0)
    logger.add(
        sys.stdout,
        format='<green>{time:YYYY-MM-DD HH:mm}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>'
    )
    logger.add(
        LOG_PATH,
        level='ERROR',
        format='<green>{time:YYYY-MM-DD HH:mm}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>',
        rotation='10 MB',
        compression='zip'
    )
    logger.info('loguru was inited')


def get_application() -> FastAPI:
    init_loguru()

    application = FastAPI(title=TITLE)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    application.add_event_handler("startup", on_startup)
    application.add_event_handler("shutdown", on_shutdown)

    application.include_router(api_router, prefix=API_PREFIX)

    return application
