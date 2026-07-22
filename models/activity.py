from pydantic import BaseModel


class Activity(BaseModel):
    title: str
    instructions: str