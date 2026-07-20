import os
import requests
from datetime import datetime, timedelta

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

PASSENGERS = 3
MAX_PRICE_PER_PERSON = 1100

DEPARTURE_AIRPORTS = ["AMS", "BRU"]
ARRIVAL_AIRPORT = "CUR"

DEPARTURE_DATE = "2026-08-14"
RETURN_DATE = "2026-08-25"


def date_range(date):
    base = datetime.strptime(date, "%Y-%m-%d")

    return [
        (base + timedelta(days=x)).strftime("%Y-%m-%d")
        for x in range(-2, 3)
    ]


def search_google_flights(origin, date):

    params = {
        "engine": "google_flights",
        "departure_id": origin,
        "arrival_id": ARRIVAL_AIRPORT,
        "outbound_date": date,
        "return_date": RETURN_DATE,
        "currency": "EUR",
        "hl": "nl",
        "gl": "nl",
        "adults": PASSENGERS,
        "api_key": SERPAPI_KEY
    }

    r = requests.get(
        "https://serpapi.com/search",
        params=params
    )

    return r.json()


def check_baggage(flight):

    extensions = []

    for leg in flight.get("flights", []):
        extensions.extend(
            leg.get("extensions", [])
        )

    text = " ".join(extensions).lower()

    if "carry" in text or "handbagage" in text:
        return "✅ Inbegrepen"

    return "⚠️ Niet bevestigd"


def check_flights():

    best = None

    for airport in DEPARTURE_AIRPORTS:

        for date in date_range(DEPARTURE_DATE):

            data = search_google_flights(
                airport,
                date
            )

            flights = data.get(
                "best_flights",
                []
            )

            for flight in flights:

                total = flight.get("price")

                if not total:
                    continue

                price_pp = total / PASSENGERS

                if price_pp > MAX_PRICE_PER_PERSON:
                    continue


                baggage = check_baggage(flight)

                airline = (
                    flight["flights"][0]
                    .get("airline", "Onbekend")
                )


                if (
                    best is None
                    or price_pp < best["price"]
                ):

                    best = {
                        "found": True,
                        "route": f"{airport} → {ARRIVAL_AIRPORT}",
                        "date": date,
                        "price": round(price_pp),
                        "total": total,
                        "airline": airline,
                        "baggage": baggage,
                        "link": data["search_metadata"]
                        ["google_flights_url"]
                    }


    if best:
        return best


    return {
        "found": False
    }
