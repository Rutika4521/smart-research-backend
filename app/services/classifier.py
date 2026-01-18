from datetime import datetime

def classify_papers(papers):
    current_year = datetime.now().year

    past, ongoing, future = [], [], []

    for paper in papers:
        year = int(paper.get("publication_year", 0))

        if year < current_year - 4:
            past.append(paper)
        else:
            ongoing.append(paper)

        if "future" in (paper.get("abstract", "") or "").lower():
            future.append(paper)

    return past, ongoing, future
