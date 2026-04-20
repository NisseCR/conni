from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index() -> str:
    """
    Return a tiny UI placeholder.
    """
    return """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8">
        <title>Audio Mixer MVP</title>
      </head>
      <body>
        <h1>Audio Mixer MVP</h1>
        <p>UI placeholder. Add your controls here.</p>
      </body>
    </html>
    """