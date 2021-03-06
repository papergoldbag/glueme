from fastapi import APIRouter, HTTPException, Depends, Body, Query
from loguru import logger
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from src.api.depends import get_session
from src.api.schemas.code import SentCodeOut, CodeValidityOut
from src.api.schemas.forgotpass import UserForgotPass, PasswordWasChanged
from src.glueme import models
from src.glueme.settings import DELAY_BETWEEN_FORGOTPASS_CODES
from src.services.code import CodeService
from src.services.user import UserService
from src.utils.emailsender import send_mail

router = APIRouter()


@router.post('', response_model=PasswordWasChanged)
def change_password(fp: UserForgotPass = Body(...), s: Session = Depends(get_session)):
    user = models.User.by_nick_or_email(s, nick_or_email=fp.nick_or_email)
    if not user:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'no user')
    valid_code = CodeService.get_valid_code(
        s,
        email=user.email,
        code=fp.code,
        code_type_name=models.CodeType.Types.FORGOT_PASS
    )
    if not valid_code:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'code is invalid')
    valid_code.is_used = True
    user.password_hash = UserService.password_hash(fp.new_password)
    s.commit()
    return PasswordWasChanged(password_was_changed=True)


@router.get('.send_code', response_model=SentCodeOut)
def send_forgotpass_code(nick_or_email: str, s: Session = Depends(get_session)):
    nick_or_email = nick_or_email.strip()
    user = models.User.by_nick_or_email(s, nick_or_email=nick_or_email)
    if not user:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'user not exists')
    if not CodeService.can_send_forgotpass_code(s, email=user.email):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f'wait {DELAY_BETWEEN_FORGOTPASS_CODES} sec before sending')
    code = CodeService.generate_code()
    try:
        send_mail(user.email, 'Код для сброса пароля', f'{code}')
    except Exception as e:
        logger.opt(exception=e).error(e)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'smth wrong with sending')
    sent_code = CodeService.add_forgotpass_code(s, email=user.email, code=code)
    return SentCodeOut.from_orm(sent_code)


@router.get('.is_valid_code', response_model=CodeValidityOut)
def is_valid_code(email: EmailStr = Query(...), code: str = Query(...), s: Session = Depends(get_session)):
    return CodeValidityOut(is_valid=CodeService.is_valid_forgotpass_code(s, email=email.strip(), code=code.strip()))
