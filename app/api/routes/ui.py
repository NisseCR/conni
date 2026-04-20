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