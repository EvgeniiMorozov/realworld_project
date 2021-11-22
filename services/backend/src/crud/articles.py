from typing import Optional

from slugify import slugify
from sqlalchemy import delete
from sqlalchemy import desc
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql.expression import or_

from core import utils
from crud import users
from db.articles import Article
from db.articles import Favorite
from db.comments import Comment
from db.tags import Tag
from db.users import Follow
from db.users import User
from models.articles import CreateArticleRequest
from models.articles import CreateComment
from models.articles import UpdateArticle


def get_articles_auth_or_not(
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
        query = query.join(Article.tag).options(contains_eager(Article.tag)).filter(or_(tag is None, Tag.name == tag))
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


def feed_article(db: AsyncSession, user: User, limit: int, offset: int) -> list[Article]:
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


def create_article(db: AsyncSession, data: CreateArticleRequest, user: User) -> Article:
    """Creating an article, based on data from a pydantic query model."""
    tags = []
    if data.article.tagList:
        tags = [tag_name for tag_name in db.query(Tag).filter(Tag.name.in_(data.article.tagList)).all()]

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


def get_single_article_auth_or_not_auth(
    db: AsyncSession, slug: str, current_user: Optional[User] = None
) -> Article or None:
    """Get single Article or None on slug. Auth is optional."""
    articles = db.query(Article).where(Article.slug == slug).all()

    if not articles:
        return None

    articles = utils.add_tags_authors_favorites_time_in_articles(db, articles)
    if current_user:
        articles = utils.add_favorited(db, articles, current_user)
        for article in articles:
            subscribe = users.check_subscribe(db, current_user.username, article.author.username)
            if subscribe:
                article.author.following = True
    db.close()
    return articles[0]


def change_article(db: AsyncSession, slug: str, article_data: UpdateArticle, user: User) -> Article:
    """Edit Article by slug."""
    upd_article = (
        update(Article)
        .where(Article.slug == slug)
        .values(author=user.username, **article_data.article.dict(exclude_unset=True))
        .execution_options(synchronize_session="fetch")
    )
    db.execute(upd_article)
    db.commit()
    db.close()

    return get_single_article_auth_or_not_auth(db, slug)


def delete_article(db: AsyncSession, slug: str) -> None:
    """Delete Article by slug."""
    del_article = delete(Article).where(Article.slug == slug).execution_options(synchronize_session="fetch")
    db.execute(del_article)
    db.commit()


def get_comments(db: AsyncSession, slug: str, auth_user: Optional[User] = None) -> list[Comment]:
    """Get article comments on slug. Auth is optional."""
    comments = db.query(Comment).where(Comment.article == slug).all()
    for comment in comments:
        comment.author = db.query(User).where(User.id == comment.author).first()
        if auth_user:
            comment.author = utils.add_following(db, comment.author, auth_user)
        comment.createdAt = comment.created_at
        comment.updatedAt = comment.updated_at
    return comments


def create_comment(db: AsyncSession, data: CreateComment, slug: str, user: User) -> Comment:
    """Create a comment for an article by slug and user."""
    db_comment = Comment(body=data.comment.body, author=user.id, article=slug)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    db_comment.author = user
    db_comment.createdAt = db_comment.created_at
    db_comment.updatedAt = db_comment.updated_at
    return db_comment


def delete_comment(db: AsyncSession, slug: str, comment_id: str, user: User) -> None:
    """Delete the comment on slug and author of the article."""
    del_comment = (
        delete(Comment)
        .where(Comment.article == slug, Comment.id == comment_id)
        .execution_options(synchronize_options="fetch")
    )
    db.execute(del_comment)
    db.commit()


def get_comment(db: AsyncSession, slug: str, comment_id: str) -> Comment:
    """Get single comment for an article by slug and comment id"""
    return db.query(Comment).where(Comment.article == slug, Comment.id == comment_id).first()


def create_favorite(db: AsyncSession, slug: str, user: User):
    """Create Favorite model by article slug."""
    favorite = Favorite(article=slug, user=user.username)
    db.add(favorite)
    db.commit()


def delete_favorite(db: AsyncSession, slug: str, user: User) -> None:
    """Delete Favorite model by article slug and user."""
    del_favorite = delete(Favorite).where(Favorite.article == slug, Favorite.user == user.username)
    db.execute(del_favorite)
    db.commit()


def select_tags(db: AsyncSession) -> list[str]:
    """Get all tags."""
    db_tags = db.query(Tag).all()
    return [tag.name for tag in db_tags]
