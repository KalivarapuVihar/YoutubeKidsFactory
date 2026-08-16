from typing import List, Optional

from pydantic import BaseModel, Field


class Scene(BaseModel):

    scene_number: int = Field(
        ge=1
    )

    duration_seconds: int = Field(
        ge=1,
        le=60
    )

    location: str = Field(
        min_length=1
    )

    characters: List[str] = Field(
        min_length=1
    )

    action: str = Field(
        min_length=1
    )

    emotion: str = Field(
        min_length=1
    )

    dialogue: List[str] = Field(
        default_factory=list
    )

    narration: str = Field(
        default=""
    )

    camera: str = Field(
        min_length=1
    )

    music: Optional[str] = None

    sound_effects: List[str] = Field(
        default_factory=list
    )

    caption_text: str = Field(
        default=""
    )

    image_prompt: str = Field(
        min_length=1
    )