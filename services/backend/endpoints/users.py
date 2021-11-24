from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

import models
from core import security
from endpoints import utils
from crud import crud_user


router = APIRouter()


@router.get(
    "",
    name="Get current user",
    description="Gets the currently logged-in user",
    response_model=models.UserResponse,
)
async def retrieve_current_user(current_user: models.UserDB = Depends(utils.get_current_user)) -> models.UserResponse:
    token = security.create_access_token(current_user.id)
    return models.UserResponse(
        user=models.UserWithToken(
            username=current_user.username,
            email=current_user.email,
            bio=current_user.bio,
            image=current_user.image,
            token=token,
        )
    )
