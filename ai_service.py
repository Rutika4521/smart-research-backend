import json
import re
from typing import List, Dict, Any
from groq import Groq
from config import GROQ_API_KEY

_client = Groq(api_key=GROQ_API_KEY)
_MODEL = "llama-3.3-70b-versatile"


def _build_prompt(topic: str, papers: List[Dict[str, Any]]) -> str:
    papers_for_ai = papers[:15]
    papers_text = ""
    for i, p in enumerate(papers_for_ai, 1):
        keywords_str = ", ".join(p.get("keywords", [])) or "N/A"
        papers_text += f"""
Paper {i}:
  Title: {p.get('title', 'N/A')}
  Year: {p.get('year', 'N/A')}
  Abstract: {p.get('abstract', 'N/A')[:350]}
  Keywords: {keywords_str}
  Authors: {p.get('authors', 'N/A')}
"""

    return f"""You are a senior research analyst. Analyze {len(papers_for_ai)} research papers on: "{topic}".

Categorize each paper into ONE of three categories based on CONTENT (not just publication date):
1. FOUNDATIONAL — established methods, core concepts, seminal/proven techniques (Research Already Done)
2. ACTIVE_DEVELOPMENT — current benchmarks, ongoing experiments, iterative improvements (Ongoing Research)
3. EMERGING — novel paradigms, unexplored directions, early-stage ideas (Future Scope)

RULES:
- Assign each paper to ONE category based on its content.
- Select up to 4 best papers per category.
- For each: write a 2-sentence summary.
- For each CATEGORY: write 5 bullet-point sentences (no bullet symbols) that together give a reader a clear overview of what is known/ongoing/upcoming in this topic area. These should be insightful synthesis sentences, NOT just paper titles.

Return ONLY valid JSON (no markdown, no code fences):
{{
  "foundational": {{
    "overview": ["insight sentence 1", "insight sentence 2", "insight sentence 3", "insight sentence 4", "insight sentence 5"],
    "papers": [
      {{
        "summary": "2-sentence summary.",
        "paper_title": "Exact title from input",
        "year": 2020,
        "doi": null,
        "url": null,
        "authors": "Author names"
      }}
    ]
  }},
  "active_development": {{
    "overview": ["...", "...", "...", "...", "..."],
    "papers": []
  }},
  "emerging": {{
    "overview": ["...", "...", "...", "...", "..."],
    "papers": []
  }}
}}

Papers:
{papers_text}
"""


def _extract_json(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        text = text[start:end]
    return json.loads(text)


def _map_papers_by_title(papers: List[Dict[str, Any]]) -> Dict[str, Dict]:
    return {p["title"].lower().strip(): p for p in papers}


async def analyze_papers(topic: str, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not papers:
        empty_cat = {"overview": [], "papers": []}
        return {
            "foundational": empty_cat,
            "active_development": empty_cat,
            "emerging": empty_cat,
        }

    prompt = _build_prompt(topic, papers)
    paper_map = _map_papers_by_title(papers)

    chat_completion = _client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a research analysis assistant. Always respond with valid JSON only.",
            },
            {"role": "user", "content": prompt},
        ],
        model=_MODEL,
        temperature=0.2,
        max_tokens=4096,
    )

    raw_text = chat_completion.choices[0].message.content
    categorized = _extract_json(raw_text)

    # Enrich each paper with original URLs/DOIs from IEEE fetch
    for cat_key in ["foundational", "active_development", "emerging"]:
        cat_data = categorized.get(cat_key, {})
        # Handle both old list format and new dict format gracefully
        if isinstance(cat_data, list):
            categorized[cat_key] = {"overview": [], "papers": cat_data}
            cat_data = categorized[cat_key]
        for item in cat_data.get("papers", []):
            title_key = item.get("paper_title", "").lower().strip()
            original = paper_map.get(title_key)
            if original:
                item["url"] = item.get("url") or original.get("url")
                item["doi"] = item.get("doi") or original.get("doi")
                item["year"] = item.get("year") or original.get("year")
                item["authors"] = item.get("authors") or original.get("authors")

    return categorized
