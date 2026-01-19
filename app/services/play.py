import requests
import logging
import json

from app.models.index_schema import IndexSchema

BASE_URL = "http://127.0.0.1:3333/v1"

def play_playlist(playlist_id: str) -> requests.Response | None:
    try:
        url = BASE_URL + "/playlist/play"
        payload = {"id": playlist_id}
        response =  requests.put(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response

    except Exception as e:
        logging.error(e)
        return None