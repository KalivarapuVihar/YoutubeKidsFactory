from typing import List

from pydantic import BaseModel

from models.activity import Activity
from models.metadata import Metadata
from models.quiz import Quiz
from models.song import Song


class Lesson(BaseModel):
    topic: str
    introduction: str
    examples: List[str]

    activity: Activity
    quiz: Quiz
    song: Song
    metadata: Metadata

    difficulty: str
    estimated_duration_minutes: int
    language: str