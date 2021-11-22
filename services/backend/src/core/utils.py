from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from db.articles import Article
from db.articles import Favorite
from db.users import User
from repositories.users import UserRepository


def add_following(db: AsyncSession, user: User, follower: User) -> User:
    subscribe = UserRepository.check_subscribe(db, follower.username, user.username)
    if subscribe:
        user.following = True
    return user


def check_favorite(db: AsyncSession, slug: str, username: str) -> bool:
    check = db.query(Favorite).filter(Favorite.user == username, Favorite.article == slug)
    return db.query(check.exists()).scalar()


def add_favorited(db: AsyncSession, articles: list[Article], current_user: User) -> list[Article]:
    """Change field "favorited" in Article pydantic model for articles. If there is authorization."""
    favorites_user = db.query(Favorite).where(Favorite.user == current_user.username).all()
    favorites_user_article = {favorite.article: favorite.user for favorite in favorites_user}
    for article in articles:
        if article.slug in favorites_user_article:
            article.favorited = True
    return articles


def add_tags_authors_favorites_time_in_articles(db: AsyncSession, articles: list[Article]) -> list[Article]:
    """Add tags, authors, created and updated time in articles for Article pydantic model."""
    favorites = db.query(Favorite.article, func.count(Favorite.article)).group_by(Favorite.article).all()
    count_favorite_articles = {article[0]: article[1] for article in favorites}
    for article in articles:
        article.author = article.authors
        # article.tagList = [tag.name for tag in article.tagList]
        article.tagList = [tag.name for tag in article.tag]
        if article.slug in count_favorite_articles:
            article.favoritesCount = count_favorite_articles[article.slug]
            article.createdAt = article.created_at
            article.updatedAt = article.updated_at
    return articles
