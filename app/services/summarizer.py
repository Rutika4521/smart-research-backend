def summarize_abstract(abstract: str):
    if not abstract:
        return []

    sentences = abstract.split(".")
    return [s.strip() for s in sentences[:3] if s.strip()]
