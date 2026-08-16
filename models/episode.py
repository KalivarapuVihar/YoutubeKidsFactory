from typing import List

from pydantic import BaseModel, Field

from models.scene import Scene


class Episode(BaseModel):

    title: str = Field(
        min_length=1
    )

    topic: str = Field(
        min_length=1
    )

    target_age: str = Field(
        min_length=1
    )

    learning_objective: str = Field(
        min_length=1
    )

    recurring_phrase: str = Field(
        min_length=1
    )

    characters: List[str] = Field(
        min_length=1
    )

    scenes: List[Scene] = Field(
        min_length=1
    )

    song_title: str = Field(
        min_length=1
    )

    song_lyrics: str = Field(
        min_length=1
    )

    estimated_duration_seconds: int = Field(
        ge=1
    )