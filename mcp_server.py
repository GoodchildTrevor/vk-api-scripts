"""MCP (Model Context Protocol) server exposing VK API tools for AI agents."""

from mcp.server.fastmcp import FastMCP

from app.services.vk import get_file_list_with_tags, get_group_id, get_group_info, get_text_posts

mcp = FastMCP("VK API")


@mcp.tool()
async def vk_get_wall_posts(domain: str, limit: int = 50) -> list[dict]:
    """Get text posts from a VK group wall by domain (screen_name).

    Args:
        domain: VK community screen name, e.g. "durov".
        limit: Maximum number of posts to return.
    """
    return await get_text_posts(domain, count=100, limit=limit)


@mcp.tool()
async def vk_get_group_info(group_id: str) -> dict:
    """Get basic info about a VK group by its id or screen_name.

    Args:
        group_id: Numeric id or screen_name of the VK group.
    """
    return await get_group_info(group_id)


@mcp.tool()
async def vk_get_files(domain: str, limit: int = 100) -> list[dict]:
    """Get documents (files) with tags from a VK group.

    Args:
        domain: VK community screen name or URL.
        limit: Maximum number of documents to return.
    """
    gid = await get_group_id(domain)
    if gid == 0:
        return []
    return await get_file_list_with_tags(gid, count=200, limit=limit)


if __name__ == "__main__":
    mcp.run(transport="stdio")
