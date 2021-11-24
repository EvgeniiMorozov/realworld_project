from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

import models
from endpoints.utils import get_current_user
from crud import crud_article, crud_comment, crud_profile

SLUG_NOT_FOUND = "article with this slug not found"

router = APIRouter()


@router.post(
    "",
    name="Create a comment for an article",
    description="Create a comment for an article. Auth is required.",
    response_model=models.CommentInResponse,
)
async def create_article_comment(
    slug: str,
    comment_in: models.CommentInCreate = Body(..., embed=True, alias="comment"),
    current_user: models.UserDB = Depends(get_current_user(required=True)),
) -> models.CommentInResponse:
    article_db = await crud_article.get_article_by_slug(slug=slug)
    if article_db is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=SLUG_NOT_FOUND)

    comment_id = await crud_comment.create(payload=comment_in, article_id=article_db.id, author_id=current_user.id)
    comment_db = await crud_comment.get(comment_id)
    profile = await crud_profile.get_profile_by_user_id(comment_db.author_id, requested_user=current_user)

    return models.CommentInResponse(
        comment=models.CommentForResponse(
            id=comment_db.id,
            body=comment_db.body,
            createdAt=comment_db.created_at,
            updatedAt=comment_db.updated_at,
            author=profile,
        )
    )
