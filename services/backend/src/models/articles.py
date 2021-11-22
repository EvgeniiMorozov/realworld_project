from datetime import datetime
from typing import List, Optional

from models.users import ProfileUser
from pydantic import BaseModel


class Article(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tagList: Optional[list[str]] = []
    createdAt: datetime
    updatedAt: datetime
    favorited: Optional[bool] = False
    favoritesCount: Optional[int] = 0
    author: ProfileUser

    class Config:
        orm_mode = True


class GetArticles(BaseModel):
    articles: list[Article]
    articlesCount: Optional[int] = 0

    class Config:
        orm_mode = True


class CreateArticle(BaseModel):
    title: str
    description: str
    body: str
    tagList: Optional[list[str]] = None


class CreateArticleRequest(BaseModel):
    article: CreateArticle


class CreateArticleResponce(BaseModel):
    article: Article


class GetArticle(BaseModel):
    article: Article

    class Config:
        orm_mode = True


class ChangeArticle(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None


class UpdateArticle(BaseModel):
    article: ChangeArticle


class Comment(BaseModel):
    id: int
    createdAt: datetime
    updatedAt: datetime
    body: str
    author: ProfileUser

    class Config:
        orm_mode = True


class GetCommentsResponce(BaseModel):
    comments: list[Comment]


class CreateCommentBody(BaseModel):
    body: str


class CreateComment(BaseModel):
    comment: CreateCommentBody


class GetCommentResponce(BaseModel):
    comment: Comment


class GetTags(BaseModel):
    tags: list[str]

    class Config:
        orm_mode = True
