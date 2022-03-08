from fastapi import APIRouter

from src.app.api.routes import registration, code, auth, profile

api_router = APIRouter()

api_router.include_router(registration.router, prefix='/registration', tags=['Registration'])
api_router.include_router(code.router, prefix='/code', tags=['Code'])
api_router.include_router(auth.router, prefix='/auth', tags=['Auth'])
api_router.include_router(profile.router, prefix='/profile', tags=['Profile'])
