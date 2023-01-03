from pydantic import BaseModel

class RulingBase(BaseModel):
    id: str
    content: str
    additional_data: str
    summary: str


class RulingCreate(RulingBase):
    pass

class Ruling(RulingBase):
    id: str
    content: str
    additional_data: str
    summary: str
