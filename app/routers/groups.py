from fastapi import APIRouter

from app.services.vk import get_group_info

router = APIRouter(prefix="/vk", tags=["groups"])


@router.get("/groups/{group_id}")
async def groups_get(group_id: str):
    """Get basic info about a VK group by its id or screen_name."""
    info = await get_group_info(group_id)
    return {"group": info}
