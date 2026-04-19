from fastapi import APIRouter, HTTPException, Query

from app.services.vk import get_file_list_with_tags, get_group_id

router = APIRouter(prefix="/vk", tags=["files"])


@router.get("/files/{domain}")
async def files_get(
    domain: str,
    count: int = Query(200, ge=1, le=2000),
    limit: int | None = Query(None, ge=1),
):
    """Fetch documents (files) with tags from a VK community.

    ``domain`` is the group URL or screen_name; the numeric id is resolved
    automatically.
    """
    group_id = await get_group_id(domain)
    if group_id == 0:
        raise HTTPException(status_code=404, detail="Group not found")
    docs = await get_file_list_with_tags(group_id, count=count, limit=limit)
    return {"items": docs, "count": len(docs)}
