from fastapi import APIRouter, HTTPException, Depends, Body
from loguru import logger
from sqlalchemy.orm import Session
from starlette import status

from glueme.api.depends import get_session
from glueme.api.schemas.code import SentCodeOut
from glueme.api.schemas.forgotpass import UserForgotPass, PasswordWasChanged
from glueme.app.settings import DELAY_BETWEEN_FORGOTPASS_CODES, CodeTypes
from glueme.models import models
from glueme.services.code import CodeService
from glueme.services.user import UserService
from glueme.utils.emailsender import EmailSender

router = APIRouter()


@router.post('', response_model=PasswordWasChanged)
def change_password(fp: UserForgotPass = Body(...), s: Session = Depends(get_session)):
    user = models.User.by_nick_or_email(s, nick_or_email=fp.nick_or_email)
    valid_code = CodeService.get_valid_code(s, email=user.email, code=fp.code, code_type_name=CodeTypes.FORGOT_PASS)
    if not valid_code:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'code is invalid')
    valid_code.is_used = True
    user.password_hash = UserService.password_hash(fp.new_password)
    s.commit()
    return PasswordWasChanged(password_was_changed=True)


@router.get('.send_code', response_model=SentCodeOut)
def send_forgotpass_code(nick_or_email: str, s: Session = Depends(get_session)):
    user = models.User.by_nick_or_email(s, nick_or_email=nick_or_email)
    if not user:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'user not exists')
    if not CodeService.can_send_forgotpass_code(s, email=user.email):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f'wait {DELAY_BETWEEN_FORGOTPASS_CODES} sec before sending')
    code = CodeService.generate_code()
    try:
        EmailSender.send(user.email, 'Код для сброса пароля', f'{code}')
    except Exception as e:
        logger.opt(exception=e).error(e)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'smth wrong with sending')
    sent_code = CodeService.add_forgotpass_code(s, email=user.email, code=code)
    return SentCodeOut.from_orm(sent_code)

