import os
import requests
from datetime import datetime, timedelta

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

PASSENGERS = 3
MAX_PRICE_PER_PERSON = 1100

DEPARTURE_AIRPORTS = [
    "AMS",
    "BRU"
]

ARRIVAL_AIRPORT = "CUR"

BASE_DEPARTURE_DATE = "2026-08-14"
BASE_RETURN_DATE = "2026-08-25"


def create_date_variations(date_string):
    date = datetime.strptime(date_string, "%Y-%m-%d")

    dates = []

    for offset in range(-2, 3):
        new_date = date + timedelta(days=offset)
        dates.append(new_date.strftime("%Y-%m-%d"))

    return dates


def search_flights(departure, departure_date):

    params = {
        "engine": "google_flights",
        "departure_id": departure,
        "arrival_id": ARRIVAL_AIRPORT,
        "outbound_date": departure_date,
        "return_date": BASE_RETURN_DATE,
        "currency": "EUR",
        "hl": "nl",
        "gl": "nl",
        "adults": PASSENGERS,
        "api_key": SERPAPI_KEY
    }

    response = requests.get(
        "https://serpapi.com/search",
        params=params
    )

    data = response.json()

    return data


def check_flights():

    best_deal = None

    departure_dates = create_date_variations(BASE_DEPARTURE_DATE)

    for airport in DEPARTURE_AIRPORTS:

        for date in departure_dates:

            data = search_flights(
                airport,
                date
            )

            flights = data.get(
                "best_flights",
                []
            )

            for flight in flights:

                total_price = flight.get(
                    "price"
                )

                if not total_price:
                    continue


                price_per_person = (
                    total_price / PASSENGERS
                )


                if price_per_person <= MAX_PRICE_PER_PERSON:

                    airline = flight["flights"][0]["airline"]

                    google_link = (
                        data
                        .get("search_metadata", {})
                        .get("google_flights_url")
                    )


                    if (
                        best_deal is None
                        or price_per_person < best_deal["price"]
                    ):

                        best_deal = {
                            "found": True,
                            "route": f"{airport} → {ARRIVAL_AIRPORT}",
                            "date": date,
                            "airline": airline,
                            "price": round(price_per_person),
                            "total_price": total_price,
                            "link": google_link
                        }


    if best_deal:
        return best_deal


    return {
        "found": False
    }
