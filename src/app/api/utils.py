from fastapi import HTTPException


def make_http_exception(loc: list[str], msg: str = None) -> HTTPException:
    return HTTPException(
        422,
        [{
            'loc': loc,
            'msg': msg
        }]
    )
