from fastapi import APIRouter, Depends, Body, Query
from sqlalchemy.orm import Session

from src.app.api.deps import get_current_user, get_session
from src.app.api.schemas.tag import AddTagIn
from src.app.api.schemas.token import TokenDevicesOut
from src.app.api.schemas.user import UserOut, TagOut, UserUpdateIn
from src.app.api.utils import make_http_exception
from src.db import models
from src.services.tags import TagService
from src.services.user import UserService

router = APIRouter()


@router.get('', response_model=UserOut)
def get_my_profile(user: models.User = Depends(get_current_user)):
    return UserOut.from_orm(user)


@router.put('.update', response_model=UserOut)
def update_user(u: UserUpdateIn = Body(...), user: models.User = Depends(get_current_user), s: Session = Depends(get_session)):
    data_update = u.dict(exclude_unset=True)
    UserService.update_user(s, user=user, **data_update)
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
    tag = TagService.by_title(s, title=addtag.title)
    if tag:
        if UserService.user_has_tag_id(s, user_id=user.id, tag_id=tag.id):
            raise make_http_exception(['tag_value'], msg='you have this tag yet')
    else:
        tag = TagService.add_tag(s, title=addtag.title)
    user.tags.append(tag)
    s.commit()
    return [TagOut.from_orm(t) for t in user.tags]


@router.delete('.remove_tag')
def remove_tag(tag_id: int = Query(...), s: Session = Depends(get_session), user: models.User = Depends(get_current_user)):
    user_tag = UserService.user_tag_by_id(s, user_id=user.id, tag_id=tag_id)
    if not user_tag:
        raise make_http_exception(['tag_id'], msg=f'tag_id is not exists or u dont have that one')
    s.delete(user_tag)
    s.commit()
    return [TagOut.from_orm(t) for t in user.tags]
