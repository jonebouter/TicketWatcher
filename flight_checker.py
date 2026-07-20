import os
import requests

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


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

    airline = vlucht["flights"][0]["airline"]

    vertrek = vlucht["flights"][0]["departure_airport"]["time"]

    aankomst = vlucht["flights"][0]["arrival_airport"]["time"]


    return {
        "found": True,
        "route": "AMS → CUR",
        "date": f"{vertrek} - {aankomst}",
        "price": prijs,
        "airline": airline,
        "link": data["search_metadata"]["google_flights_url"]
    }
