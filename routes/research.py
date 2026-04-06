from fastapi import APIRouter, HTTPException, Request
from models import ResearchRequest, ResearchResponse, CategoryResult, PaperPoint
import ieee_service
import ai_service

router = APIRouter()

CATEGORY_META = {
    "foundational": {
        "label": "Research Already Done",
        "description": "Seminal and foundational work that established the core theories, methods, and baselines in this field.",
    },
    "active_development": {
        "label": "Ongoing Research",
        "description": "Active ongoing research — benchmarks, optimizations, domain applications, and iterative improvements.",
    },
    "emerging": {
        "label": "Future Scope",
        "description": "Novel paradigms, open research gaps, early-stage ideas, and future research directions.",
    },
}


@router.post("/research", response_model=ResearchResponse)
async def research(request: Request, body: ResearchRequest):
    topic = body.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")

    # 1. Fetch papers from IEEE
    try:
        papers = await ieee_service.fetch_papers(
            topic=topic,
            start_year=body.start_year,
            end_year=body.end_year,
            sort_by=body.sort_by
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"IEEE API error: {str(e)}")

    if not papers:
        raise HTTPException(status_code=404, detail="No papers found for this topic.")

    # 2. Analyse with Groq AI
    try:
        categorized = await ai_service.analyze_papers(topic, papers)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI analysis error: {str(e)}")

    # 3. Build response
    categories: list[CategoryResult] = []
    for cat_key in ["foundational", "active_development", "emerging"]:
        meta = CATEGORY_META[cat_key]
        cat_data = categorized.get(cat_key, {})

        # Support both formats (dict with overview/papers, or plain list)
        if isinstance(cat_data, list):
            overview_bullets = []
            raw_papers = cat_data
        else:
            overview_bullets = cat_data.get("overview", [])
            raw_papers = cat_data.get("papers", [])

        paper_points = [
            PaperPoint(
                summary=p.get("summary", ""),
                paper_title=p.get("paper_title", ""),
                year=p.get("year"),
                doi=p.get("doi"),
                url=p.get("url"),
                authors=p.get("authors"),
            )
            for p in raw_papers
        ]

        categories.append(
            CategoryResult(
                category=cat_key,
                label=meta["label"],
                description=meta["description"],
                overview=overview_bullets,
                papers=paper_points,
            )
        )

    return ResearchResponse(
        topic=topic,
        total_papers=len(papers),
        categories=categories,
    )


@router.get("/health")
async def health():
    return {"status": "ok"}
