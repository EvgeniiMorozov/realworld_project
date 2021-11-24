from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, Text, func

from db.base import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("username", String, index=True),
    Column("email", String, unique=True, index=True, nullable=False),
    Column("bio", String, index=True),
    Column("image", String, nullable=True),
    Column("hashed_password", String, nullable=False),
)

followers_assoc = Table(
    "followers_assoc",
    metadata,
    Column("follower", Integer, ForeignKey("users.id"), primary_key=True, index=True),
    Column("followed_by", Integer, ForeignKey("users.id"), primary_key=True, index=True),
)

tags = Table(
    "tags",
    metadata,
    Column("tag", String, primary_key=True, index=True),
)

articles = Table(
    "articles",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("slug", String, unique=True),
    Column("title", String),
    Column("description", String),
    Column("body", Text),
    Column("author_id", Integer, ForeignKey("users.id")),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False, server_default=func.now()),
    Column("updated_at", TIMESTAMP(timezone=True), nullable=True, server_onupdate=func.now()),
)

tags_assoc = Table(
    "tag_assoc",
    metadata,
    Column("article_id", Integer, primary_key=True, index=True),
    Column("tag", ForeignKey("tags.tag"), primary_key=True),
)

favoriter_assoc = Table(
    "favoriter_assoc",
    metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("article_id", Integer, ForeignKey("articles.id"), primary_key=True),
)

comments = Table(
    "comments",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("body", String),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("article_id", Integer, ForeignKey("articles.id")),
    Column("created_at", TIMESTAMP(timezone=True), nullable=False, server_default=func.now()),
    Column("updated_at", TIMESTAMP(timezone=True), nullable=True, server_onupdate=func.now()),
)
