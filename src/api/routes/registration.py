from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from loguru import logger
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from src.api.depends import get_session
from src.api.schemas.code import CodeValidityOut, SentCodeOut
from src.api.schemas.registration import RegistrationIn, IsEmailExistsOut, IsNickExistsOut
from src.api.schemas.user import UserOut
from src.glueme import models
from src.glueme.settings import DELAY_BETWEEN_REG_CODES
from src.services.code import CodeService
from src.services.user import UserService
from src.utils.dtutc import dt_to_utc
from src.utils.emailsender import send_mail

router = APIRouter()


@router.post('', response_model=UserOut)
def registration(reg: RegistrationIn = Body(...), s: Session = Depends(get_session)):
    valid_code = CodeService.get_valid_code(
        s,
        email=reg.email,
        code=reg.code,
        code_type_name=models.CodeType.Types.REG
    )
    if not valid_code:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'code is invalid')
    if models.User.email_exists(s, email=reg.email):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'email exists')
    if models.User.nick_exists(s, nick=reg.nick):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'nick exists')
    for tag_id in reg.tag_ids:
        if not models.Tag.id_exists(s, _id=tag_id):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f'no tag_id {tag_id}')
    valid_code.is_used = False
    new_user = models.User(
        nick=reg.nick,
        email=reg.email,
        password_hash=UserService.password_hash(reg.password),
        created=dt_to_utc(datetime.now())
    )
    s.add(new_user)
    s.commit()
    for tag_id in reg.tag_ids:
        s.add(models.TagToUser(
            user_id=new_user.id,
            tag_id=tag_id
        ))
    s.commit()
    send_mail(new_user.email, 'Регистрация', f'Поздравляем с регистрацией, {new_user.nick}!!!')
    return UserOut.from_orm(new_user)


@router.get('.send_code', response_model=SentCodeOut)
def send_code(email: EmailStr = Query(...), s: Session = Depends(get_session)):
    if models.User.email_exists(s, email=email):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, 'email exists yet, u cannot send code on this email')
    if not CodeService.can_send_reg_code(s, email=email):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f'wait {DELAY_BETWEEN_REG_CODES} sec before sending')
    code = CodeService.generate_code()
    try:
        send_mail(email, 'Код для регистрации', f'{code}')
    except Exception as e:
        logger.opt(exception=e).error(e)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'smth wrong with email sending')
    sent_code = CodeService.add_reg_code(s, email=email, code=code)
    return SentCodeOut.from_orm(sent_code)


@router.get('.is_valid_code', response_model=CodeValidityOut)
def is_valid(email: EmailStr = Query(...), code: str = Query(...), s: Session = Depends(get_session)):
    return CodeValidityOut(is_valid=CodeService.is_valid_reg_code(s, email=email, code=code))


@router.get('.is_email_exists', response_model=IsEmailExistsOut)
def is_email_exists(email: str = Query(...), s: Session = Depends(get_session)):
    return IsEmailExistsOut(exists=models.User.email_exists(s, email=email))


@router.get('.is_nick_exists', response_model=IsNickExistsOut)
def is_nick_exists(nick: str = Query(...), s: Session = Depends(get_session)):
    return IsNickExistsOut(exists=models.User.nick_exists(s, nick=nick))
