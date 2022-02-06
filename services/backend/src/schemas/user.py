from src.db.models import User
from tortoise.contrib.pydantic.creator import pydantic_model_creator

UserDB = pydantic_model_creator(
    User, name="UserDB", exclude=("created_at", "updated_at")
)
