from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

import models
from endpoints import utils
from crud import crud_article, crud_profile

router = APIRouter()


def gen_article_in_response(
    article: models.ArticleDB,
    favorited: bool,
    favorites_count: int,
    profile: models.Profile,
    tags: list[str],
) -> models.ArticleInResponse:
    return models.ArticleInResponse(
        article=models.ArticleForResponse(
            slug=article.slug,
            title=article.title,
            description=article.description,
            body=article.body,
            createdAt=article.created_at,
            updatedAt=article.updated_at,
            author=profile,
            tagList=tags,
            favorited=favorited,
            favoritesCount=favorites_count,
        )
    )


@router.post(
    "",
    name="Create an article",
    description="Create an article. Auth is required.",
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


@router.get(
    "/feed",
    name="Get articles from users you follow",
    description="Get most recent articles from users you follow. Use query parameters to limit. Auth is required.",
    response_model=models.MultipleArticlesInResponse,
)
async def feed_articles(
    current_user: models.UserDB = Depends(utils.get_current_user(required=True)),
    limit: int = 20,
    offset: int = 0,
) -> models.MultipleArticlesInResponse:
    article_dbs = await crud_article.feed(limit=limit, offset=offset, follow_by=current_user.id)
    articles = []
    for article_db in article_dbs:
        profile = await crud_profile.get_profile_by_user_id(article_db.author_id, requested_user=current_user)
        tags = await crud_article.get_article_tags(article_db.id)
        favorited = await crud_article.is_article_favorited_by_user(article_db.id, current_user.id)
        favorites_count = await crud_article.count_article_favorites(article_db.id)
        article_for_response = models.ArticleForResponse(
            slug=article_db.slug,
            title=article_db.title,
            description=article_db.description,
            body=article_db.body,
            createdAt=article_db.created_at,
            updatedAt=article_db.updated_at,
            author=profile,
            tagList=tags,
            favorited=favorited,
            favoritesCount=favorites_count,
        )
        articles.append(article_for_response)
    return models.MultipleArticlesInResponse(articles=articles, articlesCount=len(articles))
