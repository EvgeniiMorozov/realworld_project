from typing import Optional

from pydantic import BaseModel, EmailStr, Field, SecretStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = Field(None, example="example@example.com")
    username: Optional[str] = Field(None, example="perry")
    bio: Optional[str] = None
    image: Optional[str] = None


class UserDB(UserBase):
    id: int
    password_hash: str


class UserCreate(UserBase):
    email: EmailStr = Field(..., example="example@example.com")
    username: str = Field(..., example="perry")
    password: SecretStr = Field(..., example="change_it")


class UserWithToken(UserBase):
    token: str = Field(
        ...,
        example="",
    )


class UserResponse(BaseModel):
    user: UserWithToken


class LoginUser(BaseModel):
    email: str
    password: SecretStr

    class Config:
        schema_extra = {
            "example": {
                "email": "example@example.com",
                "password": "change_it",
            }
        }


class UserUpdate(UserBase):
    password: Optional[str] = Field(None, example="change_it")
