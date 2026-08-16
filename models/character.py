from typing import Optional

from pydantic import BaseModel, Field


class Character(BaseModel):

    name: str = Field(min_length=1)

    role: str = Field(min_length=1)

    species: str = Field(min_length=1)

    age: str = Field(min_length=1)

    personality: list[str] = Field(min_length=1)

    appearance: list[str] = Field(min_length=1)

    clothing: list[str] = Field(default_factory=list)

    signature_features: list[str] = Field(min_length=1)

    voice_personality: str = Field(min_length=1)

    speech_style: str = Field(min_length=1)

    catchphrase: Optional[str] = None

    likes: list[str] = Field(default_factory=list)

    dislikes: list[str] = Field(default_factory=list)

    animation_style: str = Field(min_length=1)

    character_prompt: str = Field(min_length=1)
