from pydantic import BaseModel


class Song(BaseModel):
    title: str
    lyrics: str
    mood: str
    duration_seconds: int