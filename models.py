from pydantic import BaseModel
from typing import List, Optional


class ResearchRequest(BaseModel):
    topic: str
    start_year: int = 2015
    end_year: int = 2024
    sort_by: str = "relevance"


class PaperPoint(BaseModel):
    summary: str
    paper_title: str
    year: Optional[int] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    authors: Optional[str] = None


class CategoryResult(BaseModel):
    category: str            # "foundational" | "active_development" | "emerging"
    label: str               # "Research Already Done" | "Ongoing Research" | "Future Scope"
    description: str
    overview: List[str]      # 5-6 bullet-point sentences summarising the category
    papers: List[PaperPoint]


class ResearchResponse(BaseModel):
    topic: str
    total_papers: int
    categories: List[CategoryResult]
