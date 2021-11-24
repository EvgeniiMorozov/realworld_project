import db
from db.base import database


async def get_all_tags() -> list[str]:
    query = db.tags.select()
    result = await database.fetch_all(query=query)
    return [tag.__getitem__("tag") for tag in result]


async def create(tag: str) -> str:
    query = db.tags.insert().values(tag=tag)
    return await database.execute(query=query)


async def is_existing_tag(tag: str) -> bool:
    query = db.tags.insert().values(tag=tag)
    tag_row = await database.fetch_one(query=query)
    return tag_row is not None
