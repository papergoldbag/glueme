from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .events import on_startup, on_shutdown
from ..api.router import api_router


def setup_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def get_application() -> FastAPI:
    application = FastAPI(title='GlueMe API')

    setup_middleware(application)

    application.add_event_handler("startup", on_startup)
    application.add_event_handler("shutdown", on_shutdown)

    application.include_router(api_router, prefix='/api')

    return application
