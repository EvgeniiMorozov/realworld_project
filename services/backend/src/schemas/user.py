from typing import Optional

from pydantic import BaseModel, EmailStr, Field, SecretStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = Field(None, example="example@example.ru")
    username: Optional[str] = Field(None, example="some_nickname")
    bio: Optional[str] = None
    image: Optional[str] = None


class UserDB(UserBase):
    id: int
    password_hash: str


class UserCreate(UserBase):
    email: EmailStr = Field(..., example="example@example.ru")
    username: str = Field(..., example="some_nickname")
    password: SecretStr = Field(..., example="change_password")


class UserWithToken(UserBase):
    token: str = Field(...)


class UserResponse(BaseModel):
    user: UserWithToken


class LoginUser(BaseModel):
    email: str
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = Field(None, example="change_password")
