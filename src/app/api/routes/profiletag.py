from fastapi import APIRouter, Depends, Body, Query
from sqlalchemy.orm import Session

from src.app.api.deps import get_current_user, get_session
from src.app.api.schemas.tag import AddTagWithTitleIn, AddTagWithIdIn
from src.app.api.schemas.token import TokenDevicesOut
from src.app.api.schemas.user import UserOut, TagOut, UserUpdateIn
from src.app.api.utils import make_http_exception
from src.db import models
from src.services.tags import TagService
from src.services.user import UserService

router = APIRouter()


@router.post('.add_with_id', response_model=list[TagOut])
def add_tag_with_id(addtag: AddTagWithIdIn = Body(...), s: Session = Depends(get_session), user: models.User = Depends(get_current_user)):
    tag = TagService.by_id(s, _id=addtag.tag_id)
    if not tag:
        raise make_http_exception(['tag_id'], 'tag_id not exists')
    if UserService.has_tag_id(s, user_id=user.id, tag_id=tag.id):
        raise make_http_exception(['tag_id'], 'u have tag_id yet')
    user.tags.append(tag)
    s.commit()
    return [TagOut.from_orm(t) for t in user.tags]


@router.post('.add_with_title', response_model=list[TagOut])
def add_tag_with_title(addtag: AddTagWithTitleIn = Body(...), s: Session = Depends(get_session), user: models.User = Depends(get_current_user)):
    tag = TagService.by_title(s, title=addtag.title)
    if tag:
        if UserService.has_tag_id(s, user_id=user.id, tag_id=tag.id):
            raise make_http_exception(['tag_value'], msg='you have this tag yet')
    else:
        tag = TagService.add_tag(s, title=addtag.title)
    user.tags.append(tag)
    s.commit()
    return [TagOut.from_orm(t) for t in user.tags]


@router.delete('.remove', response_model=list[TagOut])
def remove_tag(tag_id: int = Query(...), s: Session = Depends(get_session), user: models.User = Depends(get_current_user)):
    user_tag = UserService.tag_by_id(s, user_id=user.id, tag_id=tag_id)
    if not user_tag:
        raise make_http_exception(['tag_id'], msg=f'tag_id is not exists or u dont have that one')
    s.delete(user_tag)
    s.commit()
    return [TagOut.from_orm(t) for t in user.tags]
