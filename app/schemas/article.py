import datetime
from typing import Optional

from pydantic import BaseModel

from .profile import Profile


class ArticleBase(BaseModel):
    title: str
    description: str
    body: str


class ArticleDB(ArticleBase):
    id: int
    slug: str
    author_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ArticleInCreate(BaseModel):
    title: str
    description: str
    body: str
    tagList: Optional[list[str]]


class ArticleForResponse(ArticleBase):
    slug: str
    author: Profile
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    tagList: Optional[list[str]]
    favorited: bool
    favoritesCount: int


class ArticleInResponse(BaseModel):
    article: ArticleForResponse


class ArticleInUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    body: Optional[str]
    tagList: Optional[list[str]]


class MultipleArticlesInResponse(BaseModel):
    articles: list[ArticleForResponse]
    articlesCount: int
