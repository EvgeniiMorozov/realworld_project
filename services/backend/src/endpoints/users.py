from fastapi import HTTPException, APIRouter, Request
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, \
    HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from core.auth import encode_jwt
from db.base import get_session
from crud import users as users_crud
from db.users import User
from models.users import UserResponce, LoginUserRequest, NewUserRequest

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
    db_user = await users_crud.get_user_by_email(db, new_user.user.email)
    if db_user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Email {new_user.user.email} already registered")

    user = await users_crud.create_user(db, new_user)
    return UserResponce(user=user)



