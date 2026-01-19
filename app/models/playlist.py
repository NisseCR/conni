from typing import List
from pydantic import BaseModel, Field


class Playlist(BaseModel):
    id: str
    background: str
    title: str = Field(pattern=r"^[A-Z][a-z]+\s+\d+$")
    tracks: List[str]
