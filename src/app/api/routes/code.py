from fastapi import APIRouter, Query, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

from src.app.api.deps import get_session
from src.app.api.schemas.code import CodeValidityOut, CodeSendingStatusOut
from src.services.code import CodeService
from src.utils.emailsender import EmailSender

router = APIRouter()


@router.get('.send', response_model=CodeSendingStatusOut)
def send_code(email: EmailStr = Query(...), s: Session = Depends(get_session)):
    try:
        code = CodeService.generate_code()
        EmailSender.send([email], 'GlueMe', f'Registration code: {code}')
        CodeService.add_code(s, email=email, code=code)
    except Exception as e:
        raise HTTPException(200, detail=str(e))
    return CodeSendingStatusOut(is_sent=True)


@router.get('.is_valid', response_model=CodeValidityOut)
def is_valid(email: EmailStr = Query(...), code: str = Query(...), s: Session = Depends(get_session)):
    # TODO: TEST, check if exists
    # if code == '1234':
    #     return CodeValidityOut(is_valid=True)
    return CodeValidityOut(is_valid=CodeService.is_valid_code(s, email=email, code=code))


