"""Sender and brand investigator, using Tavily web search."""
from tavily import TavilyClient

import config

_client = TavilyClient(api_key=config.TAVILY_API_KEY) if config.TAVILY_API_KEY else None


def _search(query: str) -> dict:
    try:
        res = _client.search(query, max_results=3)
    except Exception as e:  # keep the graph running if a search fails
        return {"query": query, "error": str(e), "results": []}
    return {
        "query": query,
        "results": [
            {"title": r.get("title"), "url": r.get("url"),
             "snippet": (r.get("content") or "")[:300]}
            for r in res.get("results", [])
        ],
    }


def research(entities: dict) -> list[dict]:
    if _client is None:
        return []
    queries = []
    for contact in entities.get("phones", []) + entities.get("emails", []):
        queries.append(f'"{contact}" scam')
    brand = entities.get("claimed_brand")
    if brand:
        queries.append(f"{brand} official warning scam text messages")
    return [_search(q) for q in queries[: config.MAX_TAVILY_SEARCHES]]
