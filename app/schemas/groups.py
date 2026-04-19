from pydantic import BaseModel


class GroupInfo(BaseModel):
    id: int = 0
    name: str = ""
    screen_name: str = ""
    description: str = ""
    members_count: int = 0


class GroupResponse(BaseModel):
    group: dict
