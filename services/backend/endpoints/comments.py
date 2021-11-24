from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

import models
from crud import crud_article, crud_comment, crud_profile
from endpoints.utils import get_current_user

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


@router.get(
    "",
    name="Get comments for an article",
    description="Get comments for an article. Auth is optional.",
    response_model=models.MultipleCommentsInResponse,
)
async def get_comments_from_an_article(
    slug: str,
    current_user: models.UserDB = Depends(get_current_user(required=False)),
) -> models.MultipleCommentsInResponse:
    article_db = await crud_article.get_article_by_slug(slug=slug)
    if article_db is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=SLUG_NOT_FOUND)

    comment_dbs = await crud_comment.get_comments_from_an_article(article_id=article_db.id)
    comments = []
    for comment_db in comment_dbs:
        profile = await crud_profile.get_profile_by_user_id(comment_db.author_id, requested_user=current_user)
        comments.append(
            models.CommentForResponse(
                id=comment_db.id,
                body=comment_db.body,
                createdAt=comment_db.created_at,
                updatedAt=comment_db.updated_at,
                author=profile,
            )
        )
    return models.MultipleCommentsInResponse(comments=comments)


@router.delete(
    "/{comment_id}",
    name="Delete a comment for an article",
    description="Delete a comment for an article. Auth is required.",
)
async def delete_comment_for_article(
    slug: str,
    comment_id: int,
    current_user: models.UserDB = Depends(get_current_user(required=True)),
) -> None:
    article_db = await crud_article.get_article_by_slug(slug=slug)
    if article_db is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=SLUG_NOT_FOUND)

    comment_db = await crud_comment.get(comment_id)
    if comment_db is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="comment with this id not found")

    if comment_db.article_id != article_db.id:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="this comment is not belong to this article")

    if comment_db.author_id != current_user.id:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="You can not delete a comment ids not belong to yourself"
        )
    await crud_comment.delete(comment_id)
