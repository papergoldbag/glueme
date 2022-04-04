from datetime import datetime

from fastapi import APIRouter, Depends, Body, Query, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from glueme.api.depends import get_current_user, get_session
from glueme.api.schemas.tag import AddTagWithTitleIn, AddTagWithIdIn
from glueme.api.schemas.user import TagOut
from glueme.models import models
from glueme.services.user import UserService
from glueme.utils.dtutc import dt_to_utc

router = APIRouter()


@router.post('/add_with_id', response_model=list[TagOut])
def add_tag_with_id(addtag: AddTagWithIdIn = Body(...), s: Session = Depends(get_session), user: models.User = Depends(get_current_user)):
    tag = models.Tag.by_id(s, _id=addtag.tag_id)
    if not tag:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'tag_id not exists')
    if UserService.user_has_tag_id(s, user_id=user.id, tag_id=tag.id):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'u have tag_id yet')
    user.tags.append(tag)
    s.commit()
    return [TagOut.from_orm(t) for t in user.tags]


@router.post('/add_with_title', response_model=list[TagOut])
def add_tag_with_title(addtag: AddTagWithTitleIn = Body(...), s: Session = Depends(get_session), user: models.User = Depends(get_current_user)):
    tag = models.Tag.by_title(s, title=addtag.title)
    if tag:
        if UserService.user_has_tag_id(s, user_id=user.id, tag_id=tag.id):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'you have this tag yet')
    else:
        tag = models.Tag(
            title=addtag.title,
            created=dt_to_utc(datetime.now())
        )
        s.add(tag)
        s.commit()
    user.tags.append(tag)
    s.commit()
    return [TagOut.from_orm(t) for t in user.tags]


@router.delete('/remove', response_model=list[TagOut])
def remove_tag(tag_id: int = Query(...), s: Session = Depends(get_session), user: models.User = Depends(get_current_user)):
    user_tag = models.TagToUser.get_user_tag(s, user_id=user.id, tag_id=tag_id)
    if not user_tag:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f'tag_id is not exists or u dont have that one')
    s.delete(user_tag)
    s.commit()
    return [TagOut.from_orm(t) for t in user.tags]
