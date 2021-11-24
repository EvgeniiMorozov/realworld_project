from typing import Optional

from pydantic import BaseModel, EmailStr, Field, SecretStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = Field(None, example="johndow@gmail.com")
    username: Optional[str] = Field(None, example="baloon")
    bio: Optional[str] = None
    image: Optional[str] = None


class UserDB(UserBase):
    id: int
    hashed_password: str


class UserCreate(UserBase):
    email: EmailStr = Field(..., example="johndow@gmail.com")
    username: str = Field(..., example="baloon")
    password: SecretStr = Field(..., example="changeit")


class UserWithToken(UserBase):
    token: str = Field(...)


class UserResponse(BaseModel):
    user: UserWithToken


class LoginUser(BaseModel):
    email: EmailStr
    password: SecretStr

    class Config:
        schema_extra = {
            "example": {
                "email": "qwer@gmail.com",
                "password": "changeit",
            }
        }


class UserUpdate(UserBase):
    password: Optional[str] = Field(None, example="changeit")
