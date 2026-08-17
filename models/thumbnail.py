from typing import Optional

from pydantic import BaseModel, Field


class ThumbnailConcept(BaseModel):

    episode_title: str = Field(
        min_length=1,
    )

    main_character: str = Field(
        min_length=1,
    )

    supporting_character: Optional[str] = None

    main_object: str = Field(
        min_length=1,
    )

    character_emotion: str = Field(
        min_length=1,
    )

    background: str = Field(
        min_length=1,
    )

    composition: str = Field(
        min_length=1,
    )

    visual_hook: str = Field(
        min_length=1,
    )

    image_prompt: str = Field(
        min_length=1,
    )