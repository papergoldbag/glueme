from datetime import datetime

from fastapi import APIRouter, Depends, Body, Query
from sqlalchemy.orm import Session

from src.app.api.dependencies import get_current_user, get_session
from src.app.api.schemas.user import UserOut, AddTagIn, TagOut, UpdateUser, ConnectedDevice
from src.app.api.utils import dt_to_utc, make_http_exception
from src.db import models

router = APIRouter()


@router.post('', response_model=UserOut)
def get_my_profile(user: models.User = Depends(get_current_user)):
    return UserOut.from_orm(user)


@router.post('.update', response_model=UserOut)
def update_user(u: UpdateUser = Body(...), user: models.User = Depends(get_current_user), s: Session = Depends(get_session)):
    data_update = u.dict(exclude_unset=True)
    for key, value in data_update.items():
        setattr(user, key, value)
    s.commit()
    return UserOut.from_orm(user)


@router.get('.connected_device', response_model=list[ConnectedDevice])
def connected_device(user: models.User = Depends(get_current_user), s: Session = Depends(get_session)):
    res = []
    for t in user.tokens:
        res.append(ConnectedDevice(
            id=t.id,
            user_agent=t.user_agent,
            is_me=True if user.id == t.user_id else False
        ))
    return res


@router.post('.add_tag', response_model=list[TagOut])
def add_tag(addtag: AddTagIn = Body(...), s: Session = Depends(get_session), user: models.User = Depends(get_current_user)):
    tag_value = addtag.tag.strip()

    tag = s.query(models.Tag).where(models.Tag.tag == tag_value).scalar()
    if tag:
        user_tag = s.query(models.UserTags).where(models.UserTags.tag_id == tag.id)
        if user_tag:
            raise make_http_exception(['tag_value'], msg='you have this tag yet')
    else:
        tag = models.Tag(
            tag=tag_value,
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
