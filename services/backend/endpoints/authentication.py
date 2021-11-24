from fastapi import APIRouter, Body, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

import models
from core import security
from crud import crud_user


router = APIRouter()


@router.post(
    "",
    name="Register a new user",
    description="Register a new user",
    response_model=models.UserResponse,
)
async def register(user_in: models.UserCreate = Body(..., embed=True, alias="user")) -> models.UserResponse:
    user_db = await crud_user.get_user_by_email(email=user_in.email)
    if user_db:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"The user with username '{user_in.username}' already exists in the system"
        )
    user_id = await crud_user.create(user_in)
    token = security.create_access_token(user_id)
    return models.UserResponse(
        user=models.UserWithToken(
            username=user_in.username,
            email=user_in.email,
            bio=user_in.bio,
            image=user_in.image,
            token=token,
        )
    )


@router.post(
    "/login",
    name="Login and remember token",
    description="Login for existing user",
    response_model=models.UserResponse,
)
async def login(
        user_login: models.LoginUser = Body(..., embed=True, alias="user", name="Credentials to use"),
) -> models.UserResponse:
    user = await crud_user.authenticate(email=user_login.email, password=user_login.password)
    if not user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    token = security.create_access_token(user.id)
    return models.UserResponse(
        user=models.UserWithToken(
            username=user.username,
            email=user.email,
            bio=user.bio,
            image=user.image,
            token=token,
        )
    )
