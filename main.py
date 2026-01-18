import logging

from app.services.index import index_playlists


logging.basicConfig(
    filename='app.log',
    encoding='utf-8',
    level=logging.ERROR,
)


def main():
    data = index_playlists()

    for playlist in data['playlists']:
        print(playlist['title'])

if __name__ == "__main__":
    main()