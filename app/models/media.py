from __future__ import annotations

from pydantic import BaseModel


class PlaylistItem(BaseModel):
    """
    Represents a music playlist discovered from a folder.
    """
    title: str
    path: str
    thumbnail: str | None = None


class AmbienceItem(BaseModel):
    """
    Represents a single ambience audio file.
    """
    title: str
    path: str
    thumbnail: str | None = None