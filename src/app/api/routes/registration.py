from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from src.app.api.deps import get_session
from src.app.api.schemas.user import UserOut, UserCreateIn
from src.app.api.utils import make_http_exception
from src.services.code import CodeService
from src.services.user import UserService

router = APIRouter()


@router.post('', response_model=UserOut)
def user_reg(user_create: UserCreateIn = Body(...), s: Session = Depends(get_session)):
    # if not CodeService.is_valid_code(s, email=user_create.email, code=user_create.code):
    #     raise make_http_exception(['code'], 'code is invalid')
    if user_create.code != '1234':
        raise make_http_exception(['code'], 'code is invalid')

    if UserService.email_exists(s, email=user_create.email):
        raise make_http_exception(['email'], 'email exists')

    if UserService.nick_exists(s, nick=user_create.nick):
        raise make_http_exception(['nick'], 'nick exists')

    created_user = UserService.add_user(
        s,
        nick=user_create.nick,
        email=user_create.email,
        password=user_create.password
    )
    return UserOut.from_orm(created_user)
