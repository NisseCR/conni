import logging

from app.services.index import index_playlists
from app.services.play import play_playlist


logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    level=logging.ERROR,
)


def main():
    # index
    index_playlists()

if __name__ == "__main__":
    main()