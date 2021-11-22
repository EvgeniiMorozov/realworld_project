from typing import Optional

from slugify import slugify
from sqlalchemy import delete, update, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql.expression import or_

from core import utils
from models.articles import CreateArticleRequest
from db.articles import Article, Favorite
from db.comments import Comment
from db.tags import Tag
from db.users import User, Follow
from repositories.users import UserRepository


class ArticleRepository:
    def get_articles_auth_or_not(
        self,
        db: AsyncSession,
        tag: Optional[str] = None,
        author: Optional[str] = None,
        favorited: Optional[str] = None,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0,
        current_user: Optional[User] = None,
    ) -> list[Article]:
        """
        Get list Article for pydantic model. Auth is optional.
        Filtering by tag name, author username, favorited username.
        Optional receipt of articles by limit (default 20), offset (default 0).
        """
        query = db.query(Article)
        if tag:
            query = (
                query.join(Article.tag).options(contains_eager(Article.tag)).filter(or_(tag is None, Tag.name == tag))
            )
        if author:
            query = query.filter(or_(author is None, Article.author == author))
        if favorited:
            query = query.join(Favorite).where(Favorite.user == favorited)
        articles = query.order_by(desc(Article.created_at)).offset(offset).limit(limit).all()
        articles = utils.add_tags_authors_favorites_time_in_articles(db, articles)
        if current_user:
            articles = utils.add_favorited(db, articles, current_user)
            for article in articles:
                article.author = utils.add_following(db, article.author, current_user)
        return articles

    def feed_article(self, db: AsyncSession, user: User, limit: int, offset: int) -> list[Article]:
        """
        Get articles from users you follow.
        Optional receipt of articles by limit(default 20), offset(default 0).
        """
        articles = (
            db.query(Article)
            .join(Follow, Follow.author == Article.author)
            .where(Follow.user == user.username)
            .order_by(desc(Article.created_at))
            .offset(offset)
            .limit(limit)
            .all()
        )
        articles = utils.add_tags_authors_favorites_time_in_articles(db, articles)
        articles = utils.add_favorited(db, articles, user)
        for article in articles:
            article.author = utils.add_following(db, article.author, user)
        return articles

    def create_article(self, db: AsyncSession, data: CreateArticleRequest, user: User) -> Article:
        """Creating an article, based on data from a pydantic query model."""
        tags = []
        if data.article.tagList:
            tags = [
                tag_name
                for tag_name in db.query(Tag)
                .filter(Tag.name.in_(data.article.tagList))
                .all()
            ]

        db_article = Article(
            slug=slugify(data.article.title),
            title=data.article.title,
            description=data.article.description,
            body=data.article.body,
            author=user.username,
            tag=tags,
        )
        db.add(db_article)
        db.commit()
        db.refresh(db_article)

        db_article.tagList = [tag.name for tag in db_article.tag]
        db_article.author = user
        db_article.createdAt = db_article.created_at
        db_article.updatedAt = db_article.updated_at
        return db_article
