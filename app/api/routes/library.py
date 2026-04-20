from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_library_service
from app.services.library_service import LibraryService

router = APIRouter()


@router.get("/library")
def get_library(library_service: LibraryService = Depends(get_library_service)) -> dict:
    """
    Return the scanned library.
    """
    return library_service.scan()


@router.get("/library/ambience/{folder_name}")
def get_ambience_folder(
    folder_name: str,
    library_service: LibraryService = Depends(get_library_service),
) -> dict:
    """
    Return the contents of a single ambience folder.
    """
    folder = library_service.get_ambience_folder(folder_name)
    if folder is None:
        raise HTTPException(status_code=404, detail="Ambience folder not found")
    return folder.model_dump()