from tortoise import fields
from database import BaseModel, TimestampMixin


class User(TimestampMixin, BaseModel):
    username = fields.CharField(max_length=80, unique=True, null=False)
    email = fields.CharField(max_length=100, unique=True, null=False)
    password_hash = fields.CharField(max_length=128, null=True)
    bio = fields.CharField(max_length=300, null=True)
    image = fields.CharField(max_length=120, null=True)

    class Meta:
        table = "users"


class Profile(User):
    follower = fields.ManyToManyField("modeles.Profile")


# class Follow(BaseModel):
#     user = fields.ForeignKeyField("models.Users", to_field="username")
#     author = fields.ForeignKeyField("models.Users", to_field="username")


class Article(TimestampMixin, BaseModel):
    slug = fields.CharField(max_length=100, unique=True, index=True)
    title = fields.CharField(max_length=100)
    description = fields.CharField(max_length=300)
    body = fields.TextField()
    author = fields.ForeignKeyField("models.Users", related_name="article")

    class Meta:
        table = "articles"

    def __str__(self) -> str:
        return f"{self.title}, {self.author} on {self.created_at}"


class Tag(BaseModel):
    name = fields.CharField(max_length=50, unique=True)

    class Meta:
        table = "tags"


class Comment(TimestampMixin, BaseModel):
    body = fields.TextField()
    author = fields.ForeignKeyField("models.Users", related_name="comment")
    article = fields.ForeignKeyField("models.Articles", related_name="comment", to_field="slug")

    class Meta:
        table = "comments"
