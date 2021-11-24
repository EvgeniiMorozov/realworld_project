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
