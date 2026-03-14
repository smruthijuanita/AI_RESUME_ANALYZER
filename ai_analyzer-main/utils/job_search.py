from utils.web_search import search_web


def search_jobs(query: str) -> str:
    """Search for jobs by reusing the generic web search tool."""
    enriched_query = query
    if "job" not in query.lower():
        enriched_query = f"{query} jobs"
    return search_web(enriched_query)
