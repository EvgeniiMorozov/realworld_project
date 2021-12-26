from tortoise import fields, models
from database import BaseModel, TimestampMixin


class User(TimestampMixin, BaseModel):
    username = fields.CharField(max_length=80, unique=True, null=False)
    email = fields.CharField(max_length=100, unique=True, null=False)
    password_hash = fields.CharField(max_length=128, null=True)

    class Meta:
        table = "users"


class Profile(models.Model):
    user: fields.OneToOneRelation[User] = fields.OneToOneField("models.User", related_name="profile")
    bio = fields.CharField(max_length=300, null=True)
    image = fields.CharField(max_length=120, null=True)
    follows: fields.ManyToManyRelation["Profile"] = fields.ManyToManyField("models.Profile", related_name="followed_by")
    favorites: fields.ManyToManyRelation["Profile"] = fields.ManyToManyField(
        "models.Profile", related_name="favorited_by"
    )

    class Meta:
        table = "profiles"

    def __str__(self):
        return self.user.username


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
