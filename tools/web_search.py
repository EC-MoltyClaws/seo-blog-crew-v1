import os
import requests
from crewai.tools import tool


@tool("Web Search")
def web_search_tool(query: str) -> str:
    """Search the web using Serper and return the top results as text."""
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY is not set in .env")

    response = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
        json={"q": query, "num": 5},
    )

    if response.status_code != 200:
        raise RuntimeError(f"Serper search failed: {response.status_code} {response.text}")

    results = response.json().get("organic", [])
    formatted = "\n\n".join(
        f"{r['title']}\n{r['link']}\n{r.get('snippet', '')}"
        for r in results
    )
    return formatted or "No results found."
