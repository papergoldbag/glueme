from fastapi import APIRouter

from .routes import registration, auth, profile, tag, profiletag

api_router = APIRouter()


api_router.include_router(registration.router, prefix='/registration', tags=['Registration'])
api_router.include_router(auth.router, prefix='/auth', tags=['Auth'])
api_router.include_router(profile.router, prefix='/profile', tags=['Profile'])
api_router.include_router(profiletag.router, prefix='/profile/tag', tags=['Profile Tag'])
api_router.include_router(tag.router, prefix='/tags', tags=['Tags'])
