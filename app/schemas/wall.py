from pydantic import BaseModel


class WallPost(BaseModel):
    owner_id: int | str = ""
    post_id: int | str = ""
    text: str = ""
    date: int | str = ""
    likes: int = 0
    reposts: int = 0
    views: int = 0
    url: str = ""
    image_url: str | None = None
    doc_url: str | None = None
    doc_id: int | str | None = None
    doc_title: str | None = None
    doc_ext: str | None = None


class WallResponse(BaseModel):
    items: list[WallPost]
    count: int
