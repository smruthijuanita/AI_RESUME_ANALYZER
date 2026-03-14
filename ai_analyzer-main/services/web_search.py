from duckduckgo_search import DDGS


def search_resources(skill):

    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(f"learn {skill} tutorial", max_results=5):
            results.append(r["href"])

    return results