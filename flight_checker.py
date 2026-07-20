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


    r = requests.get(
        "https://serpapi.com/search",
        params=params,
        timeout=30
    )


    return r.json()



def check_flights():

    flights = []


    for origin in ORIGINS:

        for outbound in OUTBOUND_DATES:

            for returning in RETURN_DATES:


                print(
                    f"Zoeken {origin} naar {DESTINATION}"
                )


                data = search_flights(
                    origin,
                    outbound,
                    returning
                )


                flights.extend(
                    data.get("best_flights", [])
                )

                flights.extend(
                    data.get("other_flights", [])
                )



    cheapest = None
    cheapest_pp = None



    for flight in flights:


        try:

            first = flight["flights"][0]


            arrival = first["arrival_airport"]["id"]


            # Alleen Curaçao toestaan
            if arrival != DESTINATION:
                continue


            price = flight.get("price")


            if not price:
                continue


            price_pp = price / PASSENGERS


            if price_pp > MAX_PRICE_PER_PERSON:
                continue



            if (
                cheapest_pp is None
                or price_pp < cheapest_pp
            ):

                cheapest_pp = price_pp
                cheapest = flight



        except Exception:

            continue



    if not cheapest:

        return {
            "found": False
        }



    first = cheapest["flights"][0]


    return {

        "found": True,

        "route":
            f"{first['departure_airport']['id']} → {first['arrival_airport']['id']}",


        "date":
            first["departure_airport"]["time"][:10],


        "price":
            round(cheapest_pp),


        "total":
            cheapest["price"],


        "airline":
            first.get(
                "airline",
                "Onbekend"
            ),


        "link":
            "https://www.google.com/travel/flights"

    }
