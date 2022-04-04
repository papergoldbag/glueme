from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from glueme.api.depends import get_current_user, get_session
from glueme.api.schemas.tag import TagWithIsMyOut, TagOut
from glueme.models import models
from glueme.services.tag import TagService

router = APIRouter()


@router.get('', response_model=list[TagOut])
def all_tags(s: Session = Depends(get_session)):
    return [TagOut.from_orm(t) for t in s.query(models.Tag).all()]


@router.get('.search', response_model=list[TagWithIsMyOut])
def search_tags(q: str = Query(...), user: models.User = Depends(get_current_user), s: Session = Depends(get_session)):
    res = []
    user_tag_ids = [t.id for t in user.tags]
    for tag in TagService.search_tags(s, q=q):
        res.append(TagWithIsMyOut(
            id=tag.id,
            title=tag.title,
            created=tag.created,
            is_my=True if tag.id in user_tag_ids else False
        ))
    return res
