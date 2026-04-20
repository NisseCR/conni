from __future__ import annotations

from pydantic import BaseModel


class PlaylistItem(BaseModel):
    """
    Represents a music playlist discovered from a folder.
    """
    title: str
    path: str
    thumbnail: str | None = None


class AmbienceTrackItem(BaseModel):
    """
    Represents one audio file inside an ambience folder.
    """
    title: str
    path: str


class AmbienceFolderItem(BaseModel):
    """
    Represents an ambience collection discovered from a folder.
    """
    title: str
    path: str
    thumbnail: str | None = None
    tracks: list[AmbienceTrackItem]