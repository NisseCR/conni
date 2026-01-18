from typing import List
from pydantic import BaseModel

from app.models.playlist import Playlist
from app.models.track import Track


class IndexSchema(BaseModel):
    playlists: List[Playlist]
    tracks: List[Track]
