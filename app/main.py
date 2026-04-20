from __future__ import annotations

import threading

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes.library import router as library_router
from app.api.routes.playback import router as playback_router
from app.api.routes.state import router as state_router
from app.api.routes.ui import router as ui_router
from app.services.hotkey_service import HotkeyService
from app.services.library_service import LibraryService
from app.services.mixer_service import MixerService
from app.services.playback_service import PlaybackService


def create_app() -> FastAPI:
    """
    Create the FastAPI app and attach shared services.

    Returns:
        Configured FastAPI app instance.
    """
    app = FastAPI(title="Audio Mixer MVP")

    app.state.library_service = LibraryService()
    app.state.mixer_service = MixerService()
    app.state.playback_service = PlaybackService(app.state.mixer_service)

    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    app.mount("/media", StaticFiles(directory="media"), name="media")

    app.include_router(ui_router)
    app.include_router(library_router, prefix="/api")
    app.include_router(playback_router, prefix="/api")
    app.include_router(state_router, prefix="/api")

    return app


app = create_app()


def start_hotkeys() -> None:
    """
    Start the global hotkey listener using shared services.
    """
    HotkeyService(app.state.playback_service).run()