from typing import List
from pydantic import BaseModel


class Playlist(BaseModel):
    id: str
    background: str
    title: str
    tracks: List[str]
