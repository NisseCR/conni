from __future__ import annotations

from pydantic import BaseModel, Field


class AmbienceLayer(BaseModel):
    """
    Represents one active ambience layer.
    """
    name: str
    path: str
    volume: float = 1.0
    is_fading: bool = False


class PlaybackState(BaseModel):
    """
    Current playback state shared by the UI, API, and hotkeys.
    """
    current_playlist: str | None = None
    current_track_index: int = 0
    active_ambience: list[AmbienceLayer] = Field(default_factory=list)
    music_volume: float = 1.0
    ambience_volume: float = 1.0
    master_volume: float = 1.0
    is_music_playing: bool = False
    max_ambience_layers: int = 4
    music_crossfade_ms: int = 10000
    ambience_crossfade_ms: int = 10000