from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.app.api.deps import get_current_user, get_session
from src.app.api.schemas.user import TagOut
from src.db import models
from src.services.tags import TagService

router = APIRouter()


@router.get('', response_model=list[TagOut])
def all_tags(q: str = Query(...), user: models.User = Depends(get_current_user), s: Session = Depends(get_session)):
    return [TagOut.from_orm(t) for t in s.query(models.Tag).all()]


@router.get('.search', response_model=list[TagOut])
def search_tags(q: str = Query(...), user: models.User = Depends(get_current_user), s: Session = Depends(get_session)):
    tags = TagService.search_tag(s, q=q)
    return [TagOut.from_orm(t) for t in tags]
