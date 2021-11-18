import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl, validator, constr


class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: EmailStr
    hashed_password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    bio: str
    image: HttpUrl
    token: str


class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str

    @validator("password2")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords don`t match")
        return v
