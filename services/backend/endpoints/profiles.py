from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

import models
from crud import crud_profile, crud_user
from endpoints import utils

FOLLOW_SOMETHING_WRONG = "you cannot follow this user because something wrong"

router = APIRouter()


async def get_profile_response(username: str, requested_user: models.UserDB) -> models.ProfileResponse:
    profile = await crud_profile.get_profile_by_username(username, requested_user=requested_user)
    if profile is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="user not existed")
    return models.ProfileResponse(profile=profile)


@router.get(
    "/{username}",
    name="Get a profile",
    description="Get a profile of a user of the system. Auth is optional",
    response_model=models.ProfileResponse,
)
async def get_profile(
        username: str,
        requested_user: models.UserDB = Depends(utils.get_current_user(required=False)),
) -> models.ProfileResponse:
    return await get_profile_response(requested_user=requested_user, username=username)