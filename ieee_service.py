import httpx
from typing import List, Dict, Any
from config import IEEE_API_KEY

IEEE_BASE_URL = "https://ieeexploreapi.ieee.org/api/v1/search/articles"


async def fetch_papers(
    topic: str,
    start_year: int = 2015,
    end_year: int = 2024,
    max_results: int = 50,
    sort_by: str = "relevance",
) -> List[Dict[str, Any]]:
    """
    Fetch papers from IEEE Xplore API for a given topic and year range.
    Returns a list of paper dictionaries with title, abstract, year, doi, authors, keywords.
    """
    sort_field = "article_title" if sort_by == "date" else "article_number"
    sort_order = "desc"

    params = {
        "apikey": IEEE_API_KEY,
        "querytext": topic,
        "start_year": start_year,
        "end_year": end_year,
        "max_records": min(max_results, 200),
        "sort_field": sort_field,
        "sort_order": sort_order,
        "start_record": 1,
        "format": "json",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(IEEE_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

    articles = data.get("articles", [])
    papers = []

    for article in articles:
        article_number = article.get("article_number", "")
        ieee_url = (
            f"https://ieeexplore.ieee.org/document/{article_number}"
            if article_number
            else None
        )

        authors_data = article.get("authors", {}).get("authors", [])
        author_names = ", ".join(
            a.get("full_name", "") for a in authors_data[:3]
        )
        if len(authors_data) > 3:
            author_names += " et al."

        index_terms = article.get("index_terms", {})
        keywords = []
        for term_group in index_terms.values():
            keywords.extend(term_group.get("terms", []))

        paper = {
            "title": article.get("title", "Untitled"),
            "abstract": article.get("abstract", ""),
            "year": article.get("publication_year"),
            "doi": article.get("doi"),
            "url": ieee_url,
            "authors": author_names,
            "keywords": keywords[:10],  # limit keyword list
            "publication_title": article.get("publication_title", ""),
            "article_number": article_number,
            "citations": article.get("citing_paper_count", 0),
        }
        papers.append(paper)

    return papers
