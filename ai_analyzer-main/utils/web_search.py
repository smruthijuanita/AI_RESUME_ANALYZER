import logging
from duckduckgo_search import DDGS


def search_web(query: str, max_results: int = 5) -> str:
    """Run a lightweight web search and return a readable summary string."""
    results_text: list[str] = []
    try:
        with DDGS() as ddgs:
            for item in ddgs.text(query, max_results=max_results):
                title = item.get("title", "")
                snippet = item.get("body", "") or item.get("snippet", "")
                url = item.get("href", "") or item.get("url", "")
                piece = " - ".join(part for part in [title, snippet, url] if part)
                if piece:
                    results_text.append(piece)
    except Exception as exc:  # pragma: no cover
        logging.exception("web search failed", exc_info=exc)
        return "Web search temporarily unavailable."

    if not results_text:
        return "No web results found."

    return "\n".join(results_text)


def search_tutorials(query: str, max_results: int = 5) -> str:
    """Search for tutorial-focused web results and return a summary string."""
    enriched_query = query
    if "tutorial" not in query.lower() and "course" not in query.lower():
        enriched_query = f"{query} tutorial"
    return search_web(enriched_query, max_results)


# Backward-compatible alias for older imports.
def searchtutorials(query: str, max_results: int = 5) -> str:
    return search_tutorials(query, max_results)
