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
