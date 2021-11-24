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


async def get_follow_user(
        username: str, requested_user: models.UserDB
) -> models.UserDB:
    follower_user = await crud_user.get_user_by_username(username=username)
    if follower_user is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="user with this username is not existed")

    if follower_user.id == requested_user.id:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="cannot follow yourself")
    return follower_user


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


@router.post(
    "/{username}/follow",
    name="Follow a user",
    description="Follow a user by username",
    response_model=models.ProfileResponse,
)
async def follow_user(
        username: str,
        requested_user: models.UserDB = Depends(utils.get_current_user),
) -> models.ProfileResponse:
    follower_user = await get_follow_user(requested_user=requested_user, username=username)
    if await crud_profile.is_following(follower_user, requested_user):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="you follow this user already")
    await crud_profile.follow(follower_user, requested_user)
    return await get_profile_response(requested_user=requested_user, username=username)
