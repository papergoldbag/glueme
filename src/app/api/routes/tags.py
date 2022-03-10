from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.app.api.deps import get_current_user, get_session
from src.app.api.schemas.tag import TagWithIsMyOut
from src.db import models
from src.services.tags import TagService

router = APIRouter()


@router.get('', response_model=list[TagWithIsMyOut])
def all_tags(user: models.User = Depends(get_current_user), s: Session = Depends(get_session)):
    user_tag_ids: set[int] = set(t.id for t in user.tags)
    res = []
    for t in s.query(models.Tag).all():
        res.append(TagWithIsMyOut(
            id=t.id,
            title=t.title,
            created=t.created,
            is_my=t.id in user_tag_ids
        ))
    return res


@router.get('.search', response_model=list[TagWithIsMyOut])
def search_tags(q: str = Query(...), user: models.User = Depends(get_current_user), s: Session = Depends(get_session)):
    user_tag_ids: set[int] = set(t.id for t in user.tags)
    tags = TagService.search_tags(s, q=q)
    res = []
    for t in tags:
        res.append(TagWithIsMyOut(
            id=t.id,
            title=t.title,
            created=t.created,
            is_my=t.id in user_tag_ids
        ))
    return res
