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
