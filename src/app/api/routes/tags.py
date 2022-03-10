from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.api.deps import get_current_user, get_session
from src.app.api.schemas.user import TagOut
from src.db import models

router = APIRouter()


@router.get('', response_model=list[TagOut])
def all_tags(user: models.User = Depends(get_current_user), s: Session = Depends(get_session)):
    return [TagOut.from_orm(t) for t in s.query(models.Tag).all()]

