from typing import Optional

import db
import models
from db.base import database


async def create(payload: models.CommentInCreate, article_id: int, author_id: int) -> int:
    query = db.comments.insert().values(
        body=payload.body,
        author_id=author_id,
        article_id=article_id,
    )
    return await database.execute(query=query)


async def get(comment_id: int) -> Optional[models.CommentDB]:
    query = db.comments.select().where(comment_id == db.comments.c.id)
    comment_row = await database.fetch_one(query=query)
    return models.CommentDB(**comment_row) if comment_row else None


async def get_comments_from_an_article(article_id: int) -> list[models.CommentDB]:
    query = db.comments.select().where(article_id == db.comments.c.article_id)
    comment_rows = await database.fetch_all(query=query)
    return [models.CommentDB(**row) for row in comment_rows]
