from fastapi import APIRouter, Query

from app.services.vk import get_text_posts

router = APIRouter(prefix="/vk", tags=["wall"])


@router.get("/wall/{domain}")
async def wall_get(
    domain: str,
    count: int = Query(100, ge=1, le=100),
    limit: int | None = Query(None, ge=1),
):
    """Fetch text-only wall posts from a VK community by its screen_name."""
    posts = await get_text_posts(domain, count=count, limit=limit)
    return {"items": posts, "count": len(posts)}
