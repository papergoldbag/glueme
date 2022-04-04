from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from glueme.api.depends import get_session
from glueme.api.schemas.code import SentCodeOut
from glueme.api.schemas.forgotpass import UserForgotPass, PasswordWasChanged
from glueme.app.settings import DELAY_BETWEEN_FORGOTPASS_CODES, CodeTypes
from glueme.models import models
from glueme.services.code import CodeService
from glueme.services.user import UserService
from glueme.utils.mailgun import Mailgun

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
def send_forgotpass_code(email: str, s: Session = Depends(get_session)):
    if not models.User.email_exists(s, email=email):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'email not exists')
    if not CodeService.can_send_forgotpass_code(s, email=email):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f'wait {DELAY_BETWEEN_FORGOTPASS_CODES} sec before sending')
    code = CodeService.generate_code()
    try:
        Mailgun.send([email], 'GlueMe', f'Код для сброса пароля: {code}')
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'smth wrong with sending')
    added_code = CodeService.add_forgotpass_code(s, email=email, code=code)
    return SentCodeOut.from_orm(added_code)

