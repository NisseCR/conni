from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.dependencies import get_playback_service
from app.services.playback_service import PlaybackService

router = APIRouter()


class PlaylistRequest(BaseModel):
    """
    Request body for playlist actions.
    """
    playlist_name: str


class AmbienceRequest(BaseModel):
    """
    Request body for ambience actions.
    """
    name: str
    path: str
    volume: float = 1.0


@router.post("/play")
def play_playlist(
    payload: PlaylistRequest,
    playback_service: PlaybackService = Depends(get_playback_service),
) -> dict:
    """
    Start a playlist.
    """
    playback_service.play_playlist(payload.playlist_name)
    return {"ok": True}


@router.post("/switch")
def switch_playlist(
    payload: PlaylistRequest,
    playback_service: PlaybackService = Depends(get_playback_service),
) -> dict:
    """
    Switch to another playlist.
    """
    playback_service.switch_playlist(payload.playlist_name)
    return {"ok": True}


@router.post("/ambience/add")
def add_ambience(
    payload: AmbienceRequest,
    playback_service: PlaybackService = Depends(get_playback_service),
) -> dict:
    """
    Add a new ambience layer.
    """
    ok = playback_service.add_ambience(payload.name, payload.path, payload.volume)
    return {"ok": ok}


@router.post("/ambience/remove")
def remove_ambience(
    payload: PlaylistRequest,
    playback_service: PlaybackService = Depends(get_playback_service),
) -> dict:
    """
    Remove an active ambience layer by name.
    """
    ok = playback_service.remove_ambience(payload.playlist_name)
    return {"ok": ok}


@router.post("/ambience/clear")
def clear_ambience(
    playback_service: PlaybackService = Depends(get_playback_service),
) -> dict:
    """
    Remove all ambience layers.
    """
    playback_service.clear_ambience()
    return {"ok": True}