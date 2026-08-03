from datetime import datetime

from pydantic import BaseModel


class RunMetadata(BaseModel):

    run_id: str

    topic: str

    status: str

    created_at: datetime

    updated_at: datetime