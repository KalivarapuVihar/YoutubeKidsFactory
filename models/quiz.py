from pydantic import BaseModel
from typing import List


class QuizQuestion(BaseModel):
    question: str
    answer: str


class Quiz(BaseModel):
    questions: List[QuizQuestion]