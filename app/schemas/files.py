from pydantic import BaseModel


class Document(BaseModel):
    id: int = 0
    title: str = ""
    ext: str = ""
    date: int = 0
    url: str = ""
    tags: list[str] = []


class FilesResponse(BaseModel):
    items: list[Document]
    count: int
