from pydantic import BaseModel
from typing import List


class Metadata(BaseModel):
    title: str
    description: str
    tags: List[str]