import requests
import logging
import json

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
        response = requests.get(url)
        response.raise_for_status()
        return response

    except Exception as e:
        logging.error(e)
        return None


def __save_playlists(schema: IndexSchema) -> None:
    data = {}
    for playlist in schema["playlists"]:
        title = playlist["title"]
        data[title] = playlist["id"]

    with open("data/playlists.json", "w") as f:
        f.write(json.dumps(data))



def index() -> None:
    response = __fetch_playlists()
    parsed_response =  __parse_playlists(response)
    __save_playlists(parsed_response)






