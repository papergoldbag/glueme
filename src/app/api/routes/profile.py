from fastapi import APIRouter, Depends, Body
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.app.api.deps import get_current_user, get_session, http_bearer
from src.app.api.schemas.token import TokenDevicesOut
from src.app.api.schemas.user import UserOut, UserUpdateIn
from src.db import models

router = APIRouter()


@router.get('', response_model=UserOut)
def get_my_profile(user: models.User = Depends(get_current_user)):
    return UserOut.from_orm(user)


@router.get('.connected_device', response_model=list[TokenDevicesOut])
def connected_device(user: models.User = Depends(get_current_user), ac: HTTPAuthorizationCredentials = Depends(http_bearer)):
    res = []
    for t in user.tokens:
        res.append(TokenDevicesOut(
            id=t.id,
            user_agent=t.user_agent,
            is_me=True if t.token == ac.credentials else False
        ))
    return res


@router.put('.update', response_model=UserOut)
def update_user(u: UserUpdateIn = Body(...), user: models.User = Depends(get_current_user), s: Session = Depends(get_session)):
    data_update = u.dict(exclude_unset=True)
    if data_update:
        if 'name' in data_update:
            user.name = data_update['name'].strip()
        if 'bio' in data_update:
            user.bio = data_update['bio'].strip()
        s.commit()
    return UserOut.from_orm(user)
