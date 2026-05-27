from fastapi import APIRouter, HTTPException, Query

from app.exceptions import VKAPIError
from app.schemas.files import FilesResponse
from app.services.vk import get_file_list_with_tags, get_group_id

router = APIRouter(prefix="/vk", tags=["files"])


@router.get("/files/{domain}", response_model=FilesResponse)
async def files_get(
    domain: str,
    count: int = Query(200, ge=1, le=2000),
    limit: int | None = Query(None, ge=1),
):
    """Fetch documents (files) with tags from a VK community.

    ``domain`` is the group URL or screen_name; the numeric id is resolved
    automatically.
    """
    try:
        group_id = await get_group_id(domain)
    except VKAPIError as e:
        status = 403 if e.code in (5, 15, 19) else 400
        raise HTTPException(status_code=status, detail=e.message)
    if group_id == 0:
        raise HTTPException(status_code=404, detail="Group not found")
    try:
        docs = await get_file_list_with_tags(group_id, count=count, limit=limit)
    except VKAPIError as e:
        status = 403 if e.code in (5, 15, 19) else 400
        raise HTTPException(status_code=status, detail=e.message)
    return FilesResponse(items=docs, count=len(docs))
