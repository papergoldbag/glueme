from fastapi import FastAPI

from src.app.api.routes import api_router
from src.core.events import on_startup, on_shutdown
from src.core.middleware import setup_middleware


def get_application() -> FastAPI:
    application = FastAPI(title='GlueMe API')

    setup_middleware(application)

    application.add_event_handler("startup", on_startup)
    application.add_event_handler("shutdown", on_shutdown)

    application.include_router(api_router, prefix='/api')

    return application
