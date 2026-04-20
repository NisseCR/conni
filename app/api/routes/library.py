from fastapi import APIRouter, Depends

from app.api.dependencies import get_library_service
from app.services.library_service import LibraryService

router = APIRouter()


@router.get("/library")
def get_library(library_service: LibraryService = Depends(get_library_service)) -> dict:
    """
    Return the scanned library.
    """
    return library_service.scan()