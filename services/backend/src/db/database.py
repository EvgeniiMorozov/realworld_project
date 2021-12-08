from tortoise.fields import DatetimeField, IntField
from tortoise.models import Model


class TimestampMixin:
    created_at = DatetimeField(auto_now_add=True, description="Дата создания")
    updated_at = DatetimeField(auto_now=True, description="Дата обновления")


class BaseModel(Model):
    id = IntField(pk=True, index=True, description="ID")

    class Meta:
        abstract = True
