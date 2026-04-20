from __future__ import annotations

import threading

import uvicorn

from app.main import app, start_audio_watcher, start_hotkeys


def main() -> None:
    """
    Start the web server and background listeners.
    """
    threading.Thread(target=start_hotkeys, daemon=True).start()
    threading.Thread(target=start_audio_watcher, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()