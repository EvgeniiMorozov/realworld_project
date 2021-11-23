from fastapi import HTTPException, APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
)

from core.auth import encode_jwt
from db.base import get_session
from crud import users as users_crud
from db.users import User
from models.users import UserResponce, LoginUserRequest, NewUserRequest, UpdateUserRequest

users_router = APIRouter()


@users_router.post("/users/login", response_model=UserResponce, tags=["User and Authentication"])
async def authentication(user_login: LoginUserRequest, db: AsyncSession = Depends(get_session)) -> UserResponce:
    """Login for existing user."""
    token = encode_jwt(user_login.user.email, user_login.user.password)
    user = await users_crud.get_user_by_token(db, token)
    if user:
        return UserResponce(user=user)
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authorized")


@users_router.post("/users", response_model=UserResponce, status_code=201, tags=["User and Authentication"])
async def register_user(new_user: NewUserRequest, db: AsyncSession = Depends(get_session)) -> UserResponce:
    """Register a new user."""
    db_user = await users_crud.get_user_by_email(db, new_user.user.email)
    if db_user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Email {new_user.user.email} already registered")

    user = await users_crud.create_user(db, new_user)
    return UserResponce(user=user)


@users_router.get("/user", response_model=UserResponce, tags=["User and Authentication"])
async def current_user(user: User = Depends(users_crud.get_current_user_by_token)) -> UserResponce:
    """Gets the currently logged-in user."""
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authorized")
    return UserResponce(user=user)


@users_router.put("/user", response_model=UpdateUserRequest, tags=["User and Authentication"])
async def update_user(
    data: UpdateUserRequest,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(users_crud.get_current_user_by_token),
) -> UpdateUserRequest:
    """Update user information for current user."""
    if user:
        new_user = await users_crud.change_user(db, user, data)
        return UpdateUserRequest(user=new_user)
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authorized")
