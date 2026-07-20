import os
import requests


SERPAPI_KEY = os.getenv("SERPAPI_KEY")

ORIGINS = [
    "AMS",
    "BRU",
    "EIN",
    "DUS"
]

DESTINATION = "CUR"

OUTBOUND_DATES = [
    "2026-08-13",
    "2026-08-14",
    "2026-08-15",
    "2026-08-16"
]

RETURN_DATES = [
    "2026-08-24",
    "2026-08-25",
    "2026-08-26"
]

PASSENGERS = 3

MAX_PRICE_PER_PERSON = 1100


def search_flights(origin, outbound, returning):

    params = {
        "engine": "google_flights",
        "api_key": SERPAPI_KEY,

        "hl": "nl",
        "gl": "nl",
        "currency": "EUR",

        "departure_id": origin,
        "arrival_id": DESTINATION,

        "outbound_date": outbound,
        "return_date": returning,

        "travel_class": 1,

        "adults": PASSENGERS
    }


    response = requests.get(
        "https://serpapi.com/search",
        params=params,
        timeout=30
    )

    return response.json()



def check_flights():

    all_flights = []


    for origin in ORIGINS:

        for outbound in OUTBOUND_DATES:

            for returning in RETURN_DATES:

                print(
                    f"Zoeken: {origin} {outbound} - {returning}"
                )


                data = search_flights(
                    origin,
                    outbound,
                    returning
                )


                all_flights.extend(
                    data.get("best_flights", [])
                )

                all_flights.extend(
                    data.get("other_flights", [])
                )


    cheapest_flight = None
    cheapest_price_pp = None



    for flight in all_flights:

        flights = flight.get("flights", [])

        if not flights:
            continue


        arrival = flights[-1].get(
            "arrival_airport",
            {}
        ).get("id")


        # Alleen Curaçao toestaan
        if arrival != DESTINATION:
            continue


        total_price = flight.get("price")


        if not total_price:
            continue


        price_pp = total_price / PASSENGERS


        if price_pp <= MAX_PRICE_PER_PERSON:

            if (
                cheapest_price_pp is None
                or price_pp < cheapest_price_pp
            ):

                cheapest_price_pp = price_pp
                cheapest_flight = flight



    if cheapest_flight:

        first = cheapest_flight["flights"][0]


        departure = first["departure_airport"]["id"]
        arrival = first["arrival_airport"]["id"]


        if arrival != DESTINATION:
            return {
                "found": False
            }


        airline = first.get(
            "airline",
            "Onbekend"
        )


        return {

            "found": True,

            "route":
                f"{departure} → {arrival}",


            "date":
                first["departure_airport"]["time"][:10],


            "price":
                round(cheapest_price_pp),


            "total":
                cheapest_flight["price"],


            "airline":
                airline,


            "link":
                "https://www.google.com/travel/flights"

        }



    return {
        "found": False
    }
