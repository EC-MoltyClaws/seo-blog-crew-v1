import os
import requests
from crewai.tools import tool


@tool("Web Search")
def web_search_tool(query: str) -> str:
    """Search the web using Tinyfish and return the top results as text."""
    api_key = os.getenv("TINYFISH_API_KEY")
    if not api_key:
        raise ValueError("TINYFISH_API_KEY is not set in .env")

    search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}"

    response = requests.post(
        "https://agent.tinyfish.ai/v1/automation/run",
        headers={"X-API-Key": api_key, "Content-Type": "application/json"},
        json={
            "url": search_url,
            "goal": "Extract the top search results. For each result return the title, URL, and snippet/description.",
        },
        timeout=60,
    )

    if response.status_code != 200:
        raise RuntimeError(f"Tinyfish search failed: {response.status_code} {response.text}")

    data = response.json()

    if data.get("status") != "COMPLETED":
        error_msg = data.get("error", {}).get("message", "Unknown error")
        raise RuntimeError(f"Tinyfish automation did not complete: {error_msg}")

    result = data.get("result")
    if not result:
        return "No results found."

    # Result may be a list of dicts or a plain string depending on what Tinyfish extracted
    if isinstance(result, list):
        formatted = "\n\n".join(
            f"{r.get('title', '')}\n{r.get('url', r.get('link', ''))}\n{r.get('snippet', r.get('description', ''))}"
            for r in result
            if isinstance(r, dict)
        )
        return formatted or str(result)

    return str(result)
