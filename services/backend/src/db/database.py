from tortoise.fields import DatetimeField, IntField
from tortoise.models import Model


class TimestampMixin:
    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)


class BaseModel(Model):
    id = IntField(pk=True)

    class Meta:
        abstract = True
        # table = cls.__name__.lower()
