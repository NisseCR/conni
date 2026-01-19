import requests
import logging
import json

from app.models.index_schema import IndexSchema

BASE_URL = "http://127.0.0.1:3333/v1"


def __keybind_to_id(keybind: str) -> str | None:
    with open("data/playlists.json", "r") as f:
        data = json.load(f)

    try:
        return data[keybind]

    except KeyError:
        logging.error(f"'{keybind}' not found in playlists.json")


def __play_playlist(keybind: str) -> requests.Response | None:
    try:
        url = BASE_URL + "/playlist/play"
        payload = {"id": keybind}
        response =  requests.put(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response

    except Exception as e:
        logging.error(e)
        return None


def play(keybind: str) -> None:
    playlist_id = __keybind_to_id(keybind)

    if playlist_id is None:
        return

    __play_playlist(playlist_id)