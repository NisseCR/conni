from pydantic import BaseModel


class Track(BaseModel):
    url: str
    title: str
    id: str
