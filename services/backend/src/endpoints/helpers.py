from typing import Optional

from crud import articles as articles_crud
from db.users import User
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND


async def check_article_status_and_return_if_positive(
    db, slug, user: Optional[User] = None
):
    article = await articles_crud.get_single_article_auth_or_not_auth(db, slug, user)
    if not article:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Article with slug: '{slug}' not found",
        )
    return article
