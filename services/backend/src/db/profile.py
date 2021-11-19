from tortoise.fields import ForeignKeyField, OneToOneRelation
from tortoise.fields.base import CASCADE
from tortoise.fields.relational import ManyToManyField
from tortoise.models import Model

from src.db.database import BaseModel
from src.db.users import User


class UserProfile(BaseModel):
    user: OneToOneRelation[User] = ForeignKeyField("users.User", related_name="user", on_delete=CASCADE)
    follows = ManyToManyField("")