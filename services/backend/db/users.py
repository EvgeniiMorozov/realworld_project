from tortoise.fields import CharField

from db.database import BaseModel, TimestampMixin


class User(TimestampMixin, BaseModel):
    username = CharField(max_length=80, unique=True, null=False)
    email = CharField(max_length=100, unique=True, null=False)
    password = CharField(max_length=128, null=True)
    bio = CharField(max_length=300, null=True)
    image = CharField(max_length=120, null=True)
