import asyncio

import httpx

from app.config import get_settings


def _settings():
    return get_settings()


def _base_params() -> dict:
    s = _settings()
    return {"access_token": s.vk_token, "v": s.vk_api_version}


async def _vk_get(client: httpx.AsyncClient, method: str, params: dict) -> dict:
    """Perform a single VK API request and return the JSON body."""
    s = _settings()
    url = f"{s.vk_base_url}{method}"
    all_params = {**_base_params(), **params}
    resp = await client.get(url, params=all_params)
    resp.raise_for_status()
    return resp.json()


# ── Group helpers ──────────────────────────────────────────────


def extract_domain(group_link: str) -> str:
    """Extract domain/screen_name from a VK group URL or return as-is."""
    # Use rsplit to avoid regex on user input (prevents ReDoS).
    stripped = group_link.rstrip("/")
    if "/" in stripped:
        return stripped.rsplit("/", 1)[-1]
    return stripped


async def get_group_info(group_id: str) -> dict:
    """Return basic info about a VK group by its id or screen_name."""
    async with httpx.AsyncClient(timeout=30) as client:
        data = await _vk_get(
            client,
            "groups.getById",
            {"group_ids": group_id, "fields": "description,members_count"},
        )
    if "response" in data:
        groups = data["response"].get("groups", data["response"])
        if isinstance(groups, list) and groups:
            return groups[0]
    return data


async def get_group_id(group_link: str) -> int:
    """Resolve a group URL / screen_name to a numeric group id."""
    domain = extract_domain(group_link)
    info = await get_group_info(domain)
    return int(info.get("id", 0))


# ── Wall posts ─────────────────────────────────────────────────


async def get_text_posts(
    domain: str,
    count: int = 100,
    limit: int | None = None,
) -> list[dict]:
    """Fetch wall posts that contain text from a VK community.

    Parameters
    ----------
    domain:  VK community screen_name (e.g. ``"durov"``).
    count:   Batch size per API request (max 100).
    limit:   Stop after collecting this many posts (``None`` = all).
    """
    s = _settings()
    posts: list[dict] = []
    offset = 0

    async with httpx.AsyncClient(timeout=30) as client:
        while True:
            data = await _vk_get(
                client,
                "wall.get",
                {
                    "domain": domain,
                    "offset": offset,
                    "count": count,
                    "extended": 1,
                },
            )

            if "response" not in data:
                break

            items = data["response"]["items"]
            for post in items:
                text = post.get("text", "")
                if not text:
                    continue

                post_data: dict = {
                    "owner_id": post.get("owner_id", 0),
                    "post_id": post.get("id", 0),
                    "text": text,
                    "date": post.get("date", 0),
                    "likes": post.get("likes", {}).get("count", 0),
                    "reposts": post.get("reposts", {}).get("count", 0),
                    "views": post.get("views", {}).get("count", 0),
                }

                for att in post.get("attachments", []):
                    if att["type"] == "photo":
                        post_data["image_url"] = att["photo"]["sizes"][-1].get(
                            "url", ""
                        )
                    elif att["type"] == "doc":
                        post_data["doc_url"] = att["doc"].get("url", "")
                        post_data["doc_id"] = att["doc"].get("id")
                        post_data["doc_title"] = att["doc"].get("title", "")
                        post_data["doc_ext"] = att["doc"].get("ext", "")

                owner_id = post_data["owner_id"]
                post_id = post_data["post_id"]
                post_data["url"] = f"https://vk.com/wall{owner_id}_{post_id}"
                posts.append(post_data)

            if len(items) < count:
                break
            offset += count

            if limit and len(posts) >= limit:
                break

            await asyncio.sleep(s.vk_request_delay)

    return posts[:limit] if limit else posts


# ── Documents / files ──────────────────────────────────────────


async def get_file_list_with_tags(
    group_id: int,
    count: int = 200,
    limit: int | None = None,
) -> list[dict]:
    """Fetch documents (files) with tags from a VK community.

    Parameters
    ----------
    group_id: Numeric community id (positive).
    count:    Batch size per API request (max 2000).
    limit:    Stop after collecting this many docs (``None`` = all).
    """
    s = _settings()
    docs: list[dict] = []
    offset = 0

    async with httpx.AsyncClient(timeout=30) as client:
        while True:
            data = await _vk_get(
                client,
                "docs.get",
                {
                    "owner_id": -group_id,
                    "offset": offset,
                    "count": count,
                    "return_tags": 1,
                },
            )

            if "response" not in data:
                break

            batch = data["response"]["items"]
            docs.extend(batch)

            if len(batch) < count:
                break
            offset += count

            if limit and len(docs) >= limit:
                break

            await asyncio.sleep(s.vk_request_delay)

    return docs[:limit] if limit else docs
