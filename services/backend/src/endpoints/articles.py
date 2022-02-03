from typing import Optional

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.params import Depends
from slugify.slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_200_OK

from core import auth
from core import utils
from crud import articles as articles_crud
from crud import users as users_crud
from db.base import get_session
from db.users import User
from endpoints.helpers import check_article_status_and_return_if_positive
from models.articles import (
    GetArticles,
    CreateArticleResponce,
    CreateArticleRequest,
    GetArticle,
    UpdateArticle,
    GetCommentsResponce,
    CreateComment,
    GetCommentResponce,
    GetTags,
)

articles_router = APIRouter()


@articles_router.get("/articles/feed", response_model=GetArticles, tags=["Articles"])
def get_recent_articles_from_users_you_follow(
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(users_crud.get_current_user_by_token),
):
    """
    Get most recent articles from users you follow.
    Use query parameters to limit. Auth is required.
    """
    articles = articles_crud.feed_article(db, user, limit, offset)
    return GetArticles(articles=articles, articlesCount=len(articles))


@articles_router.get("/articles", response_model=GetArticles, tags=["Articles"])
def get_articles(
    request: Request,
    tag: Optional[str] = None,
    author: Optional[str] = None,
    favorited: Optional[str] = None,
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
    db: AsyncSession = Depends(get_session),
):
    """
    Get most recent articles globally.
    Use query parameters to filter results.
    Auth is optional.
    """
    authorization = request.headers.get("authorization")
    if authorization:
        token = auth.clear_token(authorization)
        auth_user = users_crud.get_current_user_by_token(db, token)
        articles = articles_crud.get_articles_auth_or_not(db, tag, author, favorited, limit, offset, auth_user)
    else:
        articles = articles_crud.get_articles_auth_or_not(db, tag, author, favorited, limit, offset)
    return GetArticles(articles=articles, articlesCount=len(articles))


@articles_router.post("/articles", response_model=CreateArticleResponce, status_code=HTTP_201_CREATED)
def set_up_article(
    article_data: CreateArticleRequest,
    db: AsyncSession,
    user: User,
):
    """Create an article. Auth is required."""
    slug = slugify(article_data.article.title)
    article = await check_article_status_and_return_if_positive(db, slug, user)

    article = articles_crud.create_article(db, article_data, user)
    return CreateArticleResponce(article=article)


@articles_router.get("/articles/{slug}", response_model=GetArticle, tags=["Articles"])
def get_article(request: Request, slug: str, db: AsyncSession = Depends(get_session)):
    """Get an article. Auth not required."""
    authorization = request.headers.get("authorization")
    if authorization:
        token = auth.clear_token(authorization)
        auth_user = users_crud.get_current_user_by_token(db, token)
        article = await check_article_status_and_return_if_positive(db, slug, auth_user)
    else:
        article = await check_article_status_and_return_if_positive(db, slug)

    return GetArticle(article=article)


@articles_router.put("/articles/{slug}", response_model=GetArticle, tags=["Articles"])
async def change_article(
    article_data: UpdateArticle,
    slug: str,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(users_crud.get_current_user_by_token),
) -> GetArticle:
    """Update an article. Auth is required."""
    check = await articles_crud.get_single_article_auth_or_not_auth(db, slug)

    if check.author.username != user.username:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="You are not the author of this article")

    article = await articles_crud.change_article(db, slug, article_data, user)
    return GetArticle(article=article)


@articles_router.delete("/articles/{slug}", response_description="OK", tags=["Articles"])
async def remove_article(
    slug: str,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(users_crud.get_current_user_by_token),
) -> Response:
    """Delete an article.Auth is required."""
    article = await check_article_status_and_return_if_positive(db, slug, user)

    if article.author.username != user.username:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="You can`t delete this article. You are not the author of this article",
        )
    articles_crud.delete_article(db, slug)
    return Response(status_code=HTTP_200_OK)


@articles_router.get("/articles/{slug}/comments", response_model=GetCommentsResponce)
async def select_comment(request: Request, slug: str, db: AsyncSession = Depends(get_session)) -> GetCommentsResponce:
    """Get the comments for an article. Auth is optional."""
    await check_article_status_and_return_if_positive(db, slug)

    authorization = await request.headers.get("authorization")
    if authorization:
        token = auth.clear_token(authorization)
        auth_user = await users_crud.get_current_user_by_token(db, token)
        comments = articles_crud.get_comments(db, slug, auth_user)
    else:
        comments = articles_crud.get_comments(db, slug)

    return GetCommentsResponce(comments=comments)


@articles_router.post("/articles/{slug}/comments", response_model=GetCommentResponce, tags=["Comments"])
async def post_comment(
    slug: str,
    comment: CreateComment,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(users_crud.get_current_user_by_token),
) -> GetCommentResponce:
    """Create a comment for an article. Auth is required."""
    await check_article_status_and_return_if_positive(db, slug, user)

    comment = await articles_crud.create_comment(db, comment, slug, user)
    return GetCommentResponce(comment=comment)


@articles_router.delete("/articles/{slug}/comments/{id}", response_description="OK", tags=["Comments"])
async def remove_comment(
    slug: str,
    comment_id: int,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(users_crud.get_current_user_by_token),
) -> Response:
    """Delete a comment for an article. Auth is required."""
    article = await check_article_status_and_return_if_positive(db, slug, user)

    if article.author != user:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="You can only delete your own article.")

    comment = await articles_crud.get_comment(db, slug, comment_id)
    if not comment:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Comment not found")

    articles_crud.delete_comment(db, slug, comment_id, user)
    return Response(status_code=HTTP_200_OK)


@articles_router.post("/articles/{slug}/favorite", response_model=CreateArticleResponce, tags=["Favorites"])
async def post_favorite(
    slug: str,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(users_crud.get_current_user_by_token),
) -> CreateArticleResponce:
    """Favorite an article. Auth is required."""
    article = await check_article_status_and_return_if_positive(db, slug, user)

    favorite = utils.check_favorite(db, slug, user.username)
    if favorite:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="You have already added this article to your favorites"
        )
    await articles_crud.create_favorite(db, slug, user)
    article.favorited = True
    return CreateArticleResponce(article=article)


@articles_router.delete("/articles/{slug}/favorite", response_model=CreateArticleResponce, tags=["Favorites"])
async def remove_favorite(
    slug: str,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(users_crud.get_current_user_by_token),
) -> CreateArticleResponce:
    """Unfavorite an article. Auth is required."""
    article = await check_article_status_and_return_if_positive(db, slug, user)
    favorite = utils.check_favorite(db, slug, user.username)
    if not favorite:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="You have already added this article to your favorites"
        )

    articles_crud.delete_favorite(db, slug, user)
    return CreateArticleResponce(article=article)


@articles_router.get("/tags", response_model=GetTags, tags=["default"])
async def get_tags(db: AsyncSession = Depends(get_session)) -> GetTags:
    """Get tags. Auth not required."""
    tags = articles_crud.select_tags(db)
    return GetTags(tags=tags)