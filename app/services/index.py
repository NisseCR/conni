from typing import Any

import requests
import logging

from app.models.index_schema import IndexSchema


BASE_URL = "http://127.0.0.1:3333/v1"


def __parse_playlists(response: requests.Response) -> IndexSchema | None:
    try:
        return IndexSchema(**response.json()).model_dump()
    except Exception as e:
        logging.error(e)
        return None


def __fetch_playlists() -> requests.Response | None:
    try:
        url = BASE_URL + "/playlist"
        return requests.get(url)

    except Exception as e:
        logging.error(e)
        return None


def index_playlists() -> IndexSchema | None:
    response = __fetch_playlists()

    if response is None:
        return None

    return __parse_playlists(response)



