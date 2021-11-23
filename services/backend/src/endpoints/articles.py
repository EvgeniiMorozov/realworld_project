from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from slugify.slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from core import auth
from crud import articles as articles_crud
from crud import users as users_crud
from db.base import get_session
from db.users import User
from models.articles import GetArticles, CreateArticleResponce, CreateArticleRequest, GetArticle

articles_router = APIRouter()


@articles_router.get(
    "/articles/feed", response_model=GetArticles, tags=["Articles"]
)
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
    article = articles_crud.get_single_article_auth_or_not_auth(db, slug)
    if article:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="An article with this title already exists.")

    article = articles_crud.create_article(db, article_data, user)
    return CreateArticleResponce(article=article)


@articles_router.get("/articles/{slug}", response_model=GetArticle, tags=["Articles"])
def get_article(request: Request, slug: str, db: AsyncSession = Depends(get_session)):
    """Get an article. Auth not required."""
    authorization = request.headers.get("authorization")
    if authorization:
        token = auth.clear_token(authorization)
        auth_user = users_crud.get_current_user_by_token(db, token)
        article = articles_crud.get_single_article_auth_or_not_auth(db, slug, auth_user)
    else:
        article = articles_crud.get_single_article_auth_or_not_auth(db, slug)

    if not article:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Article not found")

    return GetArticle(article=article)
