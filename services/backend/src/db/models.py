from tortoise import fields
from database import BaseModel, TimestampMixin


class Users(TimestampMixin, BaseModel):
    username = fields.CharField(max_length=80, unique=True, null=False)
    email = fields.CharField(max_length=100, unique=True, null=False)
    password_hash = fields.CharField(max_length=128, null=True)
    bio = fields.CharField(max_length=300, null=True)
    image = fields.CharField(max_length=120, null=True)


class Follow(BaseModel):
    user = fields.ForeignKeyField("models.Users", to_field="username")
    author = fields.ForeignKeyField("models.Users", to_field="username")
    followers: fields.ManyToManyRelation[Users] = fields.ManyToManyField()
    followings: fields.ManyToManyRelation[Users] = fields.ManyToManyField()
