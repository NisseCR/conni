import logging

from app.services.index import index
from app.services.play import play


logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    level=logging.ERROR,
)


def main():
    play(keybind="A2")

if __name__ == "__main__":
    main()