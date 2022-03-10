from fastapi import HTTPException
from starlette import status


def make_http_exception(loc: list[str], msg: str = None) -> HTTPException:
    return HTTPException(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        [{
            'loc': loc,
            'msg': msg
        }]
    )
