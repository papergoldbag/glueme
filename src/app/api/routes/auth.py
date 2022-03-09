from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from src.app.api.deps import get_session
from src.app.api.schemas.token import TokenOut
from src.app.api.schemas.user import UserAuthIn
from src.services.user import UserService

router = APIRouter()


@router.post('', response_model=TokenOut)
def auth(user_auth: UserAuthIn = Body(...), s: Session = Depends(get_session)):
    user = UserService.by_nick_or_email(s, user_auth.nick_or_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='bad auth data')
    if not UserService.verify_password(user_auth.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='bad auth data')

    token = UserService.add_token(s, user.id, user_auth.user_agent)
    return TokenOut.from_orm(token)

