import datetime

from pydantic import BaseModel

from .profile import Profile


class CommentBase(BaseModel):
    body: str


class CommentDB(BaseModel):
    id: int
    author_id: int
    article_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class CommentInCreate(CommentBase):
    pass


class CommentForResponse(CommentBase):
    id: int
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    author: Profile


class CommentInResponse(BaseModel):
    comment: CommentForResponse


class MultipleCommentsForResponse(BaseModel):
    comments: list[CommentForResponse]
