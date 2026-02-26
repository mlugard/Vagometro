def tag_job_title(job_title: str, match_terms: dict):
    if not job_title:
        return {
            "matched_term": None,
            "category": None
        }

    title_normalized = job_title.lower()

    for category, terms in match_terms.items():
        for term in terms:
            if term in title_normalized:
                return {
                    "matched_term": term,
                    "category": category
                }

    return {
        "matched_term": "other",
        "category": "other"
    }