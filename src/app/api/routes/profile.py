from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.api.dependencies import get_session, get_current_user
from src.app.api.schemas.user import UserOut
from src.db import models

router = APIRouter()


@router.post('', response_model=UserOut)
def profile(user: models.User = Depends(get_current_user), s: Session = Depends(get_session)):
    return UserOut.from_orm(user)

