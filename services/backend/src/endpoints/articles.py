from typing import Optional

from fastapi import APIRouter, HTTPException, Request, status, Response
from fastapi.params import Depends
from slugify.slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from core import utils
from db.base import get_session
from core import auth
from crud import articles as articles_crud
from crud import users
from db.users import User
from models.articles import GetArticles

articles_router = APIRouter()


@articles_router.get(
    "/articles/feed", response_model=GetArticles, tags=["Articles"]
)
def get_recent_articles_from_users_you_follow(
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
        db: AsyncSession = Depends(get_session),
        user: User = Depends(users.get_current_user_by_token),
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
        auth_user = users.get_current_user_by_token(db, token)
        articles = articles_crud.get_articles_auth_or_not(db, tag, author, favorited, limit, offset, auth_user)
    else:
        articles = articles_crud.get_articles_auth_or_not(db, tag, author, favorited, limit, offset)
    return GetArticles(articles=articles, articlesCount=len(articles))
