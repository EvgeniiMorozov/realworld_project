from tortoise.fields import IntField
from tortoise.models import Model


class PKModel(Model):
    id = IntField(pk=True)
