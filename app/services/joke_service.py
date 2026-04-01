import requests
from fastapi import HTTPException, status


def fetch_random_joke() -> dict:
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "id": data.get("id"),
            "type": data.get("type"),
            "setup": data.get("setup", "No setup"),
            "punchline": data.get("punchline", "No punchline"),
            "source": "Official Joke API",
        }
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Joke service timeout. Please try again.",
        )
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to fetch joke from external API.",
        )