from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import HttpUrl


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class NewUser(LoginUser):
    username: str


class LoginUserRequest(BaseModel):
    user: LoginUser


class NewUserRequest(BaseModel):
    user: NewUser


class User(LoginUser):
    token: str
    username: str
    bio: str
    image: HttpUrl

    class Config:
        orm_mode = True


class UserInResponce(BaseModel):
    email: EmailStr
    token: str
    username: str
    bio: str
    image: HttpUrl

    class Config:
        orm_mode = True


class UserResponce(BaseModel):
    user: UserInResponce


class UpdateUser(BaseModel):
    email: Optional[EmailStr] = None
    token: Optional[str] = None
    username: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None

    class Config:
        orm_mode = True


class UpdateUserRequest(BaseModel):
    user: Optional[UpdateUser] = None


class ProfileUser(BaseModel):
    username: str
    bio: str
    image: HttpUrl
    following: Optional[bool] = False

    class Config:
        orm_mode = True


class ProfileUserResponce(BaseModel):
    profile: ProfileUser
