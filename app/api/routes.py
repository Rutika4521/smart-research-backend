from fastapi import APIRouter
from app.services.ieee_client import fetch_ieee_papers
from app.services.classifier import classify_papers
from app.services.summarizer import summarize_abstract

router = APIRouter()

@router.get("/research")
def research_topic(topic: str):
    papers = fetch_ieee_papers(topic)

    past, ongoing, future = classify_papers(papers)

    def format(paper_list):
        return [{
            "title": p.get("title"),
            "year": p.get("publication_year"),
            "summary": summarize_abstract(p.get("abstract")),
            "link": p.get("html_url")
        } for p in paper_list]

    return {
        "research_done": format(past),
        "ongoing_research": format(ongoing),
        "future_scope": format(future)
    }
