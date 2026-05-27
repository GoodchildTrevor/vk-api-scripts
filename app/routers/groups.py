from fastapi import APIRouter, HTTPException

from app.exceptions import VKAPIError
from app.schemas.groups import GroupResponse
from app.services.vk import get_group_info

router = APIRouter(prefix="/vk", tags=["groups"])


@router.get("/groups/{group_id}", response_model=GroupResponse)
async def groups_get(group_id: str):
    """Get basic info about a VK group by its id or screen_name."""
    try:
        info = await get_group_info(group_id)
    except VKAPIError as e:
        status = 403 if e.code in (5, 15, 19) else 400
        raise HTTPException(status_code=status, detail=e.message)
    if not info or info.get("id", 0) == 0:
        raise HTTPException(status_code=404, detail="Group not found")
    return GroupResponse(group=info)
