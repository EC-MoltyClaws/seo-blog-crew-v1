import os
import requests


def check_serper_api():
    response = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": os.getenv("SERPER_API_KEY"), "Content-Type": "application/json"},
        json={"q": "wanderpaws pet travel", "num": 1},
        timeout=10,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Serper returned {response.status_code}: {response.text}")
    if not response.json().get("organic"):
        raise RuntimeError("Serper returned no results")
