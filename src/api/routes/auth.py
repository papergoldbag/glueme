from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from src.api.depends import get_session
from src.api.schemas.token import TokenOut
from src.api.schemas.user import UserAuthIn
from src.glueme import models
from src.services.user import UserService

router = APIRouter()


@router.post('', response_model=TokenOut)
def user_auth(auth: UserAuthIn = Body(...), s: Session = Depends(get_session)):
    user = models.User.by_nick_or_email(s, nick_or_email=auth.nick_or_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='bad auth data')
    if not UserService.verify_password(auth.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='bad auth data')

    s.add(user)
    token = models.UserToken(
        token=UserService.generate_token(),
        user_agent=auth.user_agent,
    )
    user.tokens.append(token)
    s.commit()
    return TokenOut.from_orm(token)
