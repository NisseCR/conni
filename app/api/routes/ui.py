from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index() -> str:
    """
    Return the main control UI page from a template file.
    """
    template_path = Path("app/templates/index.html")
    return template_path.read_text(encoding="utf-8")


@router.get("/ambience/{folder_name}", response_class=HTMLResponse)
def ambience_folder(folder_name: str) -> str:
    """
    Return the ambience detail page for a specific folder.
    """
    template_path = Path("app/templates/ambience.html")
    return template_path.read_text(encoding="utf-8").replace("{{FOLDER_NAME}}", folder_name)