import logging
from pynput import keyboard
from functools import partial

from app.services.index import index
from app.services.play import play


# Initialise logger.
logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    level=logging.ERROR,
)


def main():
    # Index the playlist and soundboard files
    index()

    # Initialise keyboar listener.
    with keyboard.GlobalHotKeys({
            "<shift>+a+2": partial(play, "Atmosphere 2"),
            "<shift>+b+2": partial(play, "Borealis 2"),
            "<shift>+b+3": partial(play, "Borealis 3"),
    }) as h:
        h.join()


if __name__ == "__main__":
    main()