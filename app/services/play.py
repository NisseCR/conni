import requests
import logging
import json


BASE_URL = "http://127.0.0.1:3333/v1"


def __title_to_id(title: str) -> str | None:
    with open("data/playlists.json", "r") as f:
        data = json.load(f)

    try:
        return data[title]

    except KeyError:
        logging.error(f"'{title}' not found in playlists.json")


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


def play(title: str) -> None:
    playlist_id = __title_to_id(title)

    if playlist_id is None:
        return

    __play_playlist(playlist_id)