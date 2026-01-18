import requests
from app.config import IEEE_API_KEY, IEEE_BASE_URL

def fetch_ieee_papers(topic: str, max_results: int = 25):
    try:
        params = {
            "apikey": IEEE_API_KEY,
            "format": "json",
            "max_records": max_results,
            "sort_order": "desc",
            "sort_field": "publication_year",
            "querytext": topic
        }

        response = requests.get(IEEE_BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        return response.json().get("articles", [])

    except Exception as e:
        return []
