from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

import models
from endpoints import utils
from crud import crud_article, crud_profile

SLUG_NOT_FOUND = "article with this slug not found"
AUTHOR_NOT_EXISTED = "This article's author not existed"

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


async def get_article_response_by_slug(slug: str, current_user: models.UserDB) -> models.ArticleInResponse:
    article = await crud_article.get_article_by_slug(slug=slug)
    if article is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=SLUG_NOT_FOUND)

    profile = await crud_profile.get_profile_by_user_id(article.author_id, requested_user=current_user)
    tags = await crud_article.get_article_tags(article.id)
    if current_user:
        favorited = await crud_article.is_article_favorited_by_user(article.id, current_user.id)
    else:
        favorited = False
    favorites_count = await crud_article.count_article_favorites(article.id)
    return gen_article_in_response(
        article=article,
        favorited=favorited,
        favorites_count=favorites_count,
        profile=profile,
        tags=tags,
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


@router.get(
    "/{slug}",
    name="Get an article",
    description="Get an article. Auth not required.",
    response_model=models.ArticleInResponse,
)
async def get_article(
    slug: str,
    current_user: models.UserDB = Depends(utils.get_current_user),
) -> models.ArticleInResponse:
    return await get_article_response_by_slug(slug=slug, current_user=current_user)


@router.put(
    "/{slug}",
    name="Update an article",
    description="Update an article. Auth is required.",
    response_model=models.ArticleInResponse,
)
async def update_article(
    slug: str,
    article_in: models.ArticleInUpdate = Body(..., embed=True, alias="article"),
    current_user: models.UserDB = Depends(utils.get_current_user(required=True)),
) -> models.ArticleInResponse:
    article_db = await crud_article.get_article_by_slug(slug)
    if article_db is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=SLUG_NOT_FOUND)
    await crud_article.update(article_db, payload=article_in)

    return await get_article_response_by_slug(slug=slug, current_user=current_user)


@router.delete("/{slug}", name="Delete an article", description="Delete an article. Auth is required.")
async def delete_article(
    slug: str,
    current_user: models.UserDB = Depends(utils.get_current_user(required=True)),
) -> None:
    article_db = await crud_article.get_article_by_slug(slug=slug)
    if article_db is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=SLUG_NOT_FOUND)

    if article_db.author_id != current_user.id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="cannot delete an article owner by other user")

    await crud_article.delete(article_db)
