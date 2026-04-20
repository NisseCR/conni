from fastapi import Request

from app.services.library_service import LibraryService
from app.services.mixer_service import MixerService
from app.services.playback_service import PlaybackService


def get_library_service(request: Request) -> LibraryService:
    """
    Return the shared library service instance.
    """
    return request.app.state.library_service


def get_mixer_service(request: Request) -> MixerService:
    """
    Return the shared mixer service instance.
    """
    return request.app.state.mixer_service


def get_playback_service(request: Request) -> PlaybackService:
    """
    Return the shared playback service instance.
    """
    return request.app.state.playback_service