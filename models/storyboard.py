from pydantic import BaseModel, Field

from models.scene import Scene


class Storyboard(BaseModel):

    topic: str = Field(
        min_length=1
    )

    scenes: list[Scene] = Field(
        min_length=1
    )