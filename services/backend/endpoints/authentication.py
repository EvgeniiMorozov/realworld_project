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
