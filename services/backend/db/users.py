from tortoise.fields import IntField, CharField, DatetimeField
from tortoise.models import Model


class User(Model):
    id = IntField(pk=True)
    username = CharField(max_length=80, unique=True, null=False)
    email = CharField(max_length=100, unique=True, null=False)
    password = CharField(max_length=128, null=True)
    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)
    bio = CharField(max_length=300, null=True)
    image = CharField(max_length=120, null=True)

