from fastapi import APIRouter, Depends

from app.api.dependencies import get_mixer_service
from app.services.mixer_service import MixerService

router = APIRouter()


@router.get("/state")
def get_state(mixer_service: MixerService = Depends(get_mixer_service)) -> dict:
    """
    Return the current playback state.
    """
    return mixer_service.state.model_dump()