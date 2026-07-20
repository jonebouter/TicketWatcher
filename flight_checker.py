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


    try:

        response = requests.get(
            "https://serpapi.com/search",
            params=params,
            timeout=30
        )


        data = response.json()


        if "error" in data:

            print(
                "SerpAPI fout:",
                data["error"]
            )

            return {}


        return data


    except Exception as e:

        print(
            "API fout:",
            e
        )

        return {}




def check_flights():

    cheapest = None

    cheapest_price = None



    for origin in ORIGINS:


        for outbound in OUTBOUND_DATES:


            for returning in RETURN_DATES:


                print(
                    f"Zoeken {origin} {outbound} - {returning}"
                )


                data = search_flights(
                    origin,
                    outbound,
                    returning
                )


                flights = []


                flights.extend(
                    data.get(
                        "best_flights",
                        []
                    )
                )


                flights.extend(
                    data.get(
                        "other_flights",
                        []
                    )
                )



                for flight in flights:


                    price = flight.get(
                        "price"
                    )


                    if not price:
                        continue



                    price_pp = price / PASSENGERS



                    if price_pp > MAX_PRICE_PER_PERSON:

                        continue



                    if (
                        cheapest_price is None
                        or price_pp < cheapest_price
                    ):


                        cheapest = flight

                        cheapest_price = price_pp




    if not cheapest:


        return {

            "found": False

        }




    first = cheapest.get(
        "flights",
        [{}]
    )[0]



    departure = first.get(
        "departure_airport",
        {}
    ).get(
        "id",
        "?"
    )


    arrival = first.get(
        "arrival_airport",
        {}
    ).get(
        "id",
        "?"
    )



    airline = first.get(
        "airline",
        "Onbekend"
    )



    return {


        "found": True,


        "origin": departure,


        "destination": arrival,


        "route":
            f"{departure} → {arrival}",


        "date":
            first.get(
                "departure_airport",
                {}
            ).get(
                "time",
                ""
            )[:10],



        "price":
            round(
                cheapest_price
            ),



        "total":
            cheapest.get(
                "price"
            ),



        "airline":
            airline,


        "passengers":
            PASSENGERS,


        "link":
            "https://www.google.com/travel/flights"

    }
