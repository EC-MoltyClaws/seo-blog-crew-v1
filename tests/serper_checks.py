import os
import requests


def check_tinyfish_api():
    api_key = os.getenv("TINYFISH_API_KEY")
    if not api_key:
        raise ValueError("TINYFISH_API_KEY is not set in .env")

    response = requests.post(
        "https://agent.tinyfish.ai/v1/automation/run",
        headers={"X-API-Key": api_key, "Content-Type": "application/json"},
        json={
            "url": "https://www.google.com/search?q=wanderpaws+pet+travel",
            "goal": "Extract the top search results including title, URL, and snippet.",
        },
        timeout=60,
    )

    if response.status_code != 200:
        raise RuntimeError(f"Tinyfish returned {response.status_code}: {response.text}")

    data = response.json()
    if data.get("status") != "COMPLETED":
        error_msg = data.get("error", {}).get("message", "Unknown error")
        raise RuntimeError(f"Tinyfish automation did not complete: {error_msg}")

    if not data.get("result"):
        raise RuntimeError("Tinyfish returned no results")
