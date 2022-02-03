from os import getenv

import jwt
from fastapi import Security
from fastapi.exceptions import HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED

from consts import token_description

SECRET = getenv("RW_AUTH_SECRET")
ALGORITHM = getenv("RW_AUTH_ALGORITHM")

api_key_header = APIKeyHeader(
    scheme_name="Token",
    name="Authorization",
    description=token_description,
    auto_error=False,
)


def clear_token(token: str) -> str:
    try:
        split_token = token.split()
    except AttributeError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    if len(split_token) == 2:
        scheme, credentials = split_token
        if scheme == "Token":
            return credentials

    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


def encode_jwt(email: str, password: str) -> str:
    return jwt.encode({email: password}, SECRET, algorithm=ALGORITHM)


def check_token(raw_token: str = Security(api_key_header)) -> str:
    return clear_token(raw_token)
