import datetime
from typing import Optional

from slugify import slugify
from sqlalchemy import desc, func, select

import db
import models
from crud import crud_tag, crud_user
from db.base import database


async def add_article_tags(article_id: int, tags: list[str]) -> None:
    if tags:
        for tag in tags:
            if not await crud_tag.is_existing_tag(tag):
                await crud_tag.create(tag)
        values = [{"article_id": article_id, "tag": tag} for tag in tags]
        query = db.tags_assoc.insert().values(values)
        await database.execute(query=query)


async def remove_article_tags(article_id: int, tags: list[str]) -> None:
    if tags:
        query = (
            db.tags_assoc.delete().where(db.tags_assoc.c.article_id == article_id).where(db.tags_assoc.c.tag.in_(tags))
        )
        await database.execute(query=query)


async def get_article_tags(article_id: int) -> list[str]:
    query = (
        db.tags_assoc.select().with_only_columns([db.tags_assoc.c.tag]).where(article_id == db.tags_assoc.c.article_id)
    )
    tags = await database.fetch_all(query=query)
    return [tag.get("tag") for tag in tags]


async def create(payload: models.ArticleInCreate, author_id: int) -> int:
    slug = slugify(payload.title)
    query = db.articles.insert().values(
        title=payload.title,
        description=payload.description,
        body=payload.body,
        slug=slug,
        author_id=author_id,
    )
    article_id = await database.execute(query=query)
    if payload.tagList:
        for tag in payload.tagList:
            if not await crud_tag.is_existing_tag(tag):
                await crud_tag.create(tag)
        await add_article_tags(article_id, payload.tagList)
    return article_id


async def get(article_id: int) -> Optional[models.ArticleDB]:
    query = db.articles.select().where(article_id == db.articles.c.id)
    article_row = await database.fetch_one(query=query)

    return models.ArticleDB(**article_row) if article_row else None


async def get_article_by_slug(slug: str) -> Optional[models.ArticleDB]:
    query = db.articles.select().where(slug == db.articles.c.slug)
    article_row = await database.fetch_one(query=query)

    return models.ArticleDB(**article_row) if article_row else None


async def is_article_favorited_by_user(article_id: int, user_id: int) -> bool:
    query = (
        db.favoriter_assoc.select()
        .where(article_id == db.favoriter_assoc.c.article_id)
        .where(user_id == db.favoriter_assoc.c.user_id)
    )
    row = await database.fetch_one(query=query)
    return row is not None

