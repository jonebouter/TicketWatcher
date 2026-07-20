import os
import requests

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

MAX_PRICE = 800


def check_flights():

    params = {
        "engine": "google_flights",
        "departure_id": "AMS",
        "arrival_id": "CUR",
        "outbound_date": "2026-08-14",
        "return_date": "2026-08-25",
        "currency": "EUR",
        "hl": "nl",
        "gl": "nl",
        "adults": 1,
        "children": 0,
        "api_key": SERPAPI_KEY
    }

    response = requests.get(
        "https://serpapi.com/search",
        params=params
    )

    data = response.json()

    if "best_flights" not in data:
        return {
            "found": False
        }

    vlucht = data["best_flights"][0]

    prijs = vlucht["price"]

    if prijs > MAX_PRICE:
        return {
            "found": False
        }

    return {
        "found": True,
        "route": "AMS → CUR",
        "date": vlucht["flights"][0]["departure_airport"]["time"],
        "price": prijs,
        "airline": vlucht["flights"][0]["airline"],
        "link": data["search_metadata"]["google_flights_url"]
    }
