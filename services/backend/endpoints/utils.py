from typing import Callable, Optional

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status

import models
from core import security
from crud import crud_user


JWT_TOKEN_PREFIX = "Token"


def authorization_header_token_required(api_key: str = Depends(APIKeyHeader(name="Authorization"))) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="unsupported authorization type")

    if token_prefix != JWT_TOKEN_PREFIX:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="unsupported authorization type")
    return token


def authorization_header_token_optional(
    api_key: str = Depends(APIKeyHeader(name="Authorization", auto_error=False))
) -> Optional[str]:
    if api_key is None:
        return None
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        return None
    if token_prefix != JWT_TOKEN_PREFIX:
        return None
    return token
