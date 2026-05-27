from fastapi import APIRouter, HTTPException, Query

from app.exceptions import VKAPIError
from app.schemas.wall import WallResponse
from app.services.vk import get_text_posts

router = APIRouter(prefix="/vk", tags=["wall"])


@router.get("/wall/{domain}", response_model=WallResponse)
async def wall_get(
    domain: str,
    count: int = Query(100, ge=1, le=100),
    limit: int | None = Query(None, ge=1),
):
    """Fetch text-only wall posts from a VK community by its screen_name."""
    try:
        posts = await get_text_posts(domain, count=count, limit=limit)
    except VKAPIError as e:
        status = 403 if e.code in (5, 15, 19) else 400
        raise HTTPException(status_code=status, detail=e.message)
    return WallResponse(items=posts, count=len(posts))
