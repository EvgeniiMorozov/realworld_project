import datetime
from typing import Optional

import db
import schemas
from crud import crud_tag, crud_user
from slugify import slugify
from sqlalchemy import desc, func, select

# from db import models as db
# from db.base import database


async def add_article_tags(article_id: int, tags: list[str]) -> None:
    if tags:
        for tag in tags:
            if not await crud_tag.is_existing_tag(tag):
                await crud_tag.create(tag)
        values = [{"article_id": article_id, "tag": tag} for tag in tags]
        query = db.tags_assoc.insert().values(values)
        await db.database.execute(query=query)


async def remove_article_tags(article_id: int, tags: list[str]) -> None:
    if tags:
        query = (
            db.tags_assoc.delete()
            .where(db.tags_assoc.c.article_id == article_id)
            .where(db.tags_assoc.c.tag.in_(tags))
        )
        await db.database.execute(query=query)


async def get_article_tags(article_id: int) -> list[str]:
    query = (
        db.tags_assoc.select()
        .with_only_columns([db.tags_assoc.c.tag])
        .where(article_id == db.tags_assoc.c.article_id)
    )
    tags = await db.database.fetch_all(query=query)
    return [tag.get("tag") for tag in tags]


async def create(payload: schemas.ArticleInCreate, author_id: int) -> int:
    slug = slugify(payload.title)
    query = db.articles.insert().values(
        title=payload.title,
        description=payload.description,
        body=payload.body,
        slug=slug,
        author_id=author_id,
    )
    article_id = await db.database.execute(query=query)
    if payload.tagList:
        for tag in payload.tagList:
            if not await crud_tag.is_existing_tag(tag):
                await crud_tag.create(tag)
        await add_article_tags(article_id, payload.tagList)
    return article_id


async def get(article_id: int) -> Optional[schemas.ArticleDB]:
    query = db.articles.select().where(article_id == db.articles.c.id)
    article_row = await db.database.fetch_one(query=query)

    return schemas.ArticleDB(**article_row) if article_row else None


async def get_article_by_slug(slug: str) -> Optional[schemas.ArticleDB]:
    query = db.articles.select().where(slug == db.articles.c.slug)
    article_row = await db.database.fetch_one(query=query)

    return schemas.ArticleDB(**article_row) if article_row else None


async def is_article_favorited_by_user(article_id: int, user_id: int) -> bool:
    query = (
        db.favoriter_assoc.select()
        .where(article_id == db.favoriter_assoc.c.article_id)
        .where(user_id == db.favoriter_assoc.c.user_id)
    )
    row = await db.database.fetch_one(query=query)
    return row is not None


async def count_article_favorites(article_id: int) -> int:
    query = (
        select([func.count()])
        .select_from(db.favoriter_assoc)
        .where(db.favoriter_assoc.c.article_id == article_id)
    )
    row = await db.database.fetch_one(query=query)
    return dict(**row).get("count_1", 0)


async def update(
    article_db: schemas.ArticleDB, payload: schemas.ArticleInUpdate
) -> None:
    update_data = payload.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.datetime.utcnow()
    new_tags = update_data.pop("tagList", None)
    old_tags = await get_article_tags(article_db.id) if new_tags is not None else []
    query = (
        db.articles.update()
        .where(article_db.id == db.articles.c.id)
        .values(update_data)
        .returning(db.articles.c.id)
    )
    await db.database.execute(query=query)
    if new_tags is not None:
        add_tags = list(set(new_tags) - set(old_tags))
        remove_tags = list(set(old_tags) - set(new_tags))
        await add_article_tags(article_db.id, add_tags)
        await remove_article_tags(article_db.id, remove_tags)


async def delete(article_db: schemas.ArticleDB) -> None:
    query = db.articles.delete().where(article_db.id == db.articles.c.id)
    await db.database.execute(query=query)


async def get_all(
    limit: int = 20,
    offset: int = 0,
    tag: str = None,
    author: str = None,
    favorited: str = None,
) -> list[schemas.ArticleDB]:
    need_join = False
    j = db.articles
    query = (
        select([db.articles])
        .limit(limit)
        .offset(offset)
        .order_by(desc(db.articles.c.created_at))
    )
    if tag:
        need_join = True
        j = j.join(db.tags_assoc, db.articles.c.id == db.tags_assoc.c.article_id)
        query = query.where(db.tags_assoc.c.tag == tag)
    if author:
        user_db = await crud_user.get_user_by_username(username=author)
        if user_db:
            author_id = user_db.id
            query = query.where(author_id == db.articles.c.author_id)
    if favorited:
        user_db = await crud_user.get_user_by_username(username=favorited)
        if user_db:
            favorited_id = user_db.id
            need_join = True
            j = j.join(
                db.favoriter_assoc, db.articles.c.id == db.favoriter_assoc.c.article_id
            )
            query = query.where(favorited_id == db.favoriter_assoc.c.user_id)
    if need_join:
        query = query.select_from(j)
    articles = await db.database.fetch_all(query=query)
    return [schemas.ArticleDB(**article) for article in articles]


async def feed(
    follow_by: int, limit: int = 20, offset: int = 0
) -> list[schemas.ArticleDB]:
    query = (
        select([db.articles])
        .limit(limit)
        .offset(offset)
        .order_by(desc(db.articles.c.created_at))
    )
    j = db.articles.join(
        db.followers_assoc, db.articles.c.author_id == db.followers_assoc.c.follower
    )
    query = query.where(db.followers_assoc.c.followed_by == follow_by).select_from(j)
    articles = await db.database.fetch_all(query=query)
    return [schemas.ArticleDB(**article) for article in articles]


async def favorite(article_id: int, user_id: int) -> None:
    query = db.favoriter_assoc.insert().values(user_id=user_id, article_id=article_id)
    await db.database.execute(query=query)


async def unfavorite(article_id: int, user_id: int) -> None:
    query = (
        db.favoriter_assoc.delete()
        .where(user_id == db.favoriter_assoc.c.user_id)
        .where(article_id == db.favoriter_assoc.c.article_id)
    )
    await db.database.execute(query=query)
