def route_query(question: str) -> str:
    """Route the question to the appropriate tool name."""
    q = question.lower()
    if "job" in q:
        return "job"
    if any(keyword in q for keyword in ["tutorial", "course", "resource", "learn", "roadmap"]):
        return "tutorial"
    if "company" in q or "linkedin" in q:
        return "web"
    if "skill" in q:
        return "hybrid"
    return "resume"
