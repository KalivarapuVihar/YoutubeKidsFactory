from pydantic import BaseModel, Field
from typing import List


class YouTubeMetadata(BaseModel):

    title: str = Field(
        min_length=1,
        max_length=100,
    )

    description: str = Field(
        min_length=1,
    )

    tags: List[str] = Field(
        min_length=1,
        max_length=30,
    )

    hashtags: List[str] = Field(
        min_length=1,
        max_length=15,
    )

    category: str = "Education"

    audience: str = "Made for Kids"

    playlist: str = "Wonderland Valley - Learning Adventures"

    thumbnail_concept: str = Field(
        min_length=1,
    )

    learning_objective: str = Field(
        min_length=1,
    )

    age_range: str = "2-6 years"