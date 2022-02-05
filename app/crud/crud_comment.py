from typing import Optional

import db
import schemas

# from db import models as db
# from db.base import database


async def create(
    payload: schemas.CommentInCreate, article_id: int, author_id: int
) -> int:
    query = db.comments.insert().values(
        body=payload.body,
        author_id=author_id,
        article_id=article_id,
    )
    return await db.database.execute(query=query)


async def get(comment_id: int) -> Optional[schemas.CommentDB]:
    query = db.comments.select().where(comment_id == db.comments.c.id)
    comment_row = await db.database.fetch_one(query=query)
    return schemas.CommentDB(**comment_row) if comment_row else None


async def get_comments_from_an_article(article_id: int) -> list[schemas.CommentDB]:
    query = db.comments.select().where(article_id == db.comments.c.article_id)
    comment_rows = await db.database.fetch_all(query=query)
    return [schemas.CommentDB(**row) for row in comment_rows]


async def delete(comment_id: int) -> None:
    query = db.comments.delete().where(comment_id == db.comments.c.id)
    await db.database.execute(query=query)
