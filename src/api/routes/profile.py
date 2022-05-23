from fastapi import APIRouter, Depends, Body, HTTPException, Query, Response
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette import status

from src.api.depends import get_current_user, get_session, http_bearer
from src.api.schemas.token import TokenDeviceOut
from src.api.schemas.user import UserOut, UserUpdateIn, UserUpdateNickIn
from src.glueme import models

router = APIRouter()


@router.get('', response_model=UserOut)
def get_my_profile(user: models.User = Depends(get_current_user)):
    return UserOut.from_orm(user)


@router.get('.tokens', response_model=list[TokenDeviceOut])
def my_tokens(user: models.User = Depends(get_current_user), ac: HTTPAuthorizationCredentials = Depends(http_bearer)):
    res = []
    for t in user.tokens:
        res.append(TokenDeviceOut(
            token_id=t.id,
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


@router.put('.update_nick')
def update_nick(u: UserUpdateNickIn = Body(...), user: models.User = Depends(get_current_user), s: Session = Depends(get_session)):
    if user.nick == u.nick:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'you already have this nick')
    if models.User.nick_exists(s, nick=u.nick):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'nick already exists')
    user.nick = u.nick
    s.commit()
    return UserOut.from_orm(user)


@router.delete('.deactivate_token')
def remove_token(token: str = Query(...), user: models.User = Depends(get_current_user), s: Session = Depends(get_session)):
    token = models.UserToken.by_token(s, token=token)
    if not token:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f'no token')
    s.delete(token)
    s.commit()
    return Response(status_code=status.HTTP_200_OK)


@router.delete('.deactivate_another_token')
def remove_token(token_id: int = Query(...), user: models.User = Depends(get_current_user), s: Session = Depends(get_session)):
    token = models.UserToken.by_id(s, _id=token_id)
    if not token:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f'no token')
    s.delete(token)
    s.commit()
    return Response(status_code=status.HTTP_200_OK)
