from fastapi import APIRouter

from src.app.api.routes import registration, auth, code, profile, tags, profiletag

api_router = APIRouter()


api_router.include_router(registration.router, prefix='/registration', tags=['Registration'])
api_router.include_router(code.router, prefix='/codes', tags=['Codes'])
api_router.include_router(auth.router, prefix='/auth', tags=['Auth'])
api_router.include_router(profile.router, prefix='/profile', tags=['Profile'])
api_router.include_router(profiletag.router, prefix='/profile/tag', tags=['Profile Tag'])
api_router.include_router(tags.router, prefix='/tags', tags=['Tags'])
