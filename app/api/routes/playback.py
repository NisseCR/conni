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


class VolumeRequest(BaseModel):
    """
    Request body for volume actions.
    """
    target: str
    value: float
    ambience_name: str | None = None


@router.post("/play")
def play_playlist(
    payload: PlaylistRequest,
    playback_service: PlaybackService = Depends(get_playback_service),
) -> dict:
    """
    Start a playlist.
    """
    playback_service.switch_playlist(payload.playlist_name)
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


@router.post("/ambience/toggle")
def toggle_ambience(
    payload: AmbienceRequest,
    playback_service: PlaybackService = Depends(get_playback_service),
) -> dict:
    """
    Toggle an ambience layer.
    """
    active = playback_service.toggle_ambience(payload.name, payload.path)
    return {"ok": True, "active": active}


@router.post("/ambience/clear")
def clear_ambience(
    playback_service: PlaybackService = Depends(get_playback_service),
) -> dict:
    """
    Remove all ambience layers.
    """
    playback_service.clear_ambience()
    return {"ok": True}


@router.post("/volume")
def set_volume(
    payload: VolumeRequest,
    playback_service: PlaybackService = Depends(get_playback_service),
) -> dict:
    """
    Set a volume value for music, master, or an ambience layer.
    """
    if payload.target == "music":
        playback_service.mixer.set_music_volume(payload.value)
    elif payload.target == "master":
        playback_service.mixer.set_master_volume(payload.value)
    elif payload.target == "ambience" and payload.ambience_name:
        playback_service.mixer.set_ambience_layer_volume(payload.ambience_name, payload.value)

    return {"ok": True}