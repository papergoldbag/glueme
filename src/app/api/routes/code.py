from fastapi import APIRouter, Query, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

from src.app.api.deps import get_session
from src.app.api.schemas.code import CodeValidityOut, CodeSendingStatusOut
from src.app.api.utils import make_http_exception
from src.services.code import CodeService
from src.services.user import UserService
from src.utils.emailsender import EmailSender

router = APIRouter()


@router.get('.send', response_model=CodeSendingStatusOut)
def send_code(email: EmailStr = Query(...), s: Session = Depends(get_session)):
    if UserService.email_exists(s, email=email):
        raise make_http_exception(['email'], msg='email exists yet, u cannot send code on this email')
    code = CodeService.generate_code()
    EmailSender.send([email], 'GlueMe', f'Registration code: {code}')
    CodeService.add_code(s, email=email, code=code)
    return CodeSendingStatusOut(is_sent=True)


@router.get('.is_valid', response_model=CodeValidityOut)
def is_valid(email: EmailStr = Query(...), code: str = Query(...), s: Session = Depends(get_session)):
    # TODO: TEST, check if exists
    # if code == '1234':
    #     return CodeValidityOut(is_valid=True)
    return CodeValidityOut(is_valid=CodeService.is_valid_code(s, email=email, code=code))


