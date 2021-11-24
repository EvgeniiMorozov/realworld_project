from fastapi import APIRouter

from crud import crud_tag

router = APIRouter()


@router.get("", name="Get tags", description="Get tags. Auth not required.", response_model=dict[str, list[str]])
async def list_all_tags() -> dict[str, list[str]]:
    tags = await crud_tag.get_all_tags()
    return {"tags": tags}
