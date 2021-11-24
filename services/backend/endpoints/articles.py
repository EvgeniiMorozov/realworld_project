from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

import models
from endpoints import utils
from crud import crud_article, crud_profile

router = APIRouter()





@router.post(
    "",
    name="Create an article",
    description="Create an article. Auth is required",
    response_model=models.ArticleInResponse,
)
async def create_article(
        article_in: models.ArticleInCreate = Body(..., embed=True, alias="article"),
        current_user: models.UserDB = Depends(utils.get_current_user(required=True)),
) -> models.ArticleInResponse:
    article_id = await crud_article.create(article_in, author_id=current_user.id)
    article = await crud_article.get(article_id)
    profile = await crud_profile.get_profile_by_user_id(article.author_id, requested_user=current_user)
    tags = await crud_article.get_article_tags(article_id)
    favorited = await crud_article.is_article_favorited_by_user(article_id, current_user.id)
    favorites_count = await crud_article.count_article_favorites(article_id)

    return gen_article_in_response(
        article=article,
        favorited=favorited,
        favorites_count=favorites_count,
        profile=profile,
        tags=tags,
    )
