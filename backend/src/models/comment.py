import datetime

from pydantic import BaseModel

import models


class CommentBase(BaseModel):
    body: str


class CommentDB(CommentBase):
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
    author: models.Profile


class CommentInResponse(BaseModel):
    comment: CommentForResponse


class MultipleCommentsInResponse(BaseModel):
    comments: list[CommentForResponse]
