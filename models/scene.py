from pydantic import BaseModel, Field


class Scene(BaseModel):

    scene_number: int = Field(
        ge=1
    )

    narration: str = Field(
        min_length=1
    )

    image_prompt: str = Field(
        min_length=1
    )

    duration_seconds: int = Field(
        ge=1,
        le=60
    )