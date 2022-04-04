import sys

from loguru import logger

from glueme.app.settings import LOG_PATH


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
