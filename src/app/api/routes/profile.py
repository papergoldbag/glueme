from fastapi import APIRouter, Depends

from src.app.api.dependencies import get_current_user
from src.app.api.schemas.user import UserOut
from src.db import models

router = APIRouter()


@router.post('', response_model=UserOut)
def profile(user: models.User = Depends(get_current_user)):
    return UserOut.from_orm(user)

