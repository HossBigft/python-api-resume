import uuid
from pydantic import BaseModel, Field


class ResumeIn(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1, max_length=1000)
    model_config = {"from_attributes": True}


class ResumeOut(ResumeIn):
    id: uuid.UUID
