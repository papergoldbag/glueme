from datetime import datetime

from fastapi import APIRouter, Depends, Body, Query
from sqlalchemy.orm import Session

from src.app.api.dependencies import get_current_user, get_session
from src.app.api.schemas.tag import AddTagIn
from src.app.api.schemas.token import TokenDevicesOut
from src.app.api.schemas.user import UserOut, TagOut, UserUpdateIn
from src.app.api.utils import dt_to_utc, make_http_exception
from src.db import models

router = APIRouter()


@router.get('', response_model=UserOut)
def get_my_profile(user: models.User = Depends(get_current_user)):
    return UserOut.from_orm(user)


@router.post('.update', response_model=UserOut)
def update_user(u: UserUpdateIn = Body(...), user: models.User = Depends(get_current_user), s: Session = Depends(get_session)):
    data_update = u.dict(exclude_unset=True)
    if 'nick' in data_update and not data_update['nick']:
        raise make_http_exception(['nick'], msg='nick is None')

    for key, value in data_update.items():
        setattr(user, key, value)
    s.commit()
    return UserOut.from_orm(user)


@router.get('.connected_device', response_model=list[TokenDevicesOut])
def connected_device(user: models.User = Depends(get_current_user)):
    res = []
    for t in user.tokens:
        res.append(TokenDevicesOut(
            id=t.id,
            user_agent=t.user_agent,
            is_me=True if user.id == t.user_id else False
        ))
    return res


@router.post('.add_tag', response_model=list[TagOut])
def add_tag(addtag: AddTagIn = Body(...), s: Session = Depends(get_session), user: models.User = Depends(get_current_user)):
    tag_title = addtag.title.strip()

    tag = s.query(models.Tag).where(models.Tag.title == tag_title).scalar()
    if tag:
        user_tag = s.query(models.UserTags).where(models.UserTags.tag_id == tag.id)
        if user_tag:
            raise make_http_exception(['tag_value'], msg='you have this tag yet')
    else:
        tag = models.Tag(
            title=tag_title,
            created=dt_to_utc(datetime.now())
        )
        s.add(tag)
        s.commit()

    user.tags.append(tag)
    s.commit()
    return [TagOut.from_orm(t) for t in user.tags]


@router.get('.remove_tag')
def remove_tag(tag_id: int = Query(...), s: Session = Depends(get_session), user: models.User = Depends(get_current_user)):
    user_tag = s.query(models.UserTags).where(models.UserTags.tag_id == tag_id, models.UserTags.user_id == user.id).scalar()
    if not user_tag:
        raise make_http_exception(['tag_id'], msg=f'tag_id is not exists or u dont have that one')
    s.delete(user_tag)
    s.commit()
    return [TagOut.from_orm(t) for t in user.tags]
