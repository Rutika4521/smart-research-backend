from pydantic import BaseModel
from typing import List

class Paper(BaseModel):
    title: str
    year: int
    link: str
    summary: List[str]
