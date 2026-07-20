import os
import requests
from datetime import datetime, timedelta


SERPAPI_KEY = os.getenv("SERPAPI_KEY")


PASSENGERS = 3
MAX_PRICE_PER_PERSON = 1100


DEPARTURE_AIRPORTS = [
    "AMS",
    "BRU",
    "EIN",
    "DUS"
]


ARRIVAL_AIRPORT = "CUR"


DEPARTURE_DATE = "2026-08-14"
RETURN_DATE = "2026-08-25"



def create_date_variations(date_string):

    base_date = datetime.strptime(
        date_string,
        "%Y-%m-%d"
    )

    dates = []

    for offset in range(-2, 3):

        new_date = base_date + timedelta(
            days=offset
        )

        dates.append(
            new_date.strftime("%Y-%m-%d")
        )

    return dates



def search_flights(origin, date):

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


    response = requests.get(
        "https://serpapi.com/search",
        params=params,
        timeout=30
    )


    return response.json()



def check_baggage(flight):

    text_parts = []


    for leg in flight.get("flights", []):

        extensions = leg.get(
            "extensions",
            []
        )

        text_parts.extend(
            extensions
        )


    text = " ".join(
        text_parts
    ).lower()


    if (
        "carry" in text
        or "handbagage" in text
        or "cabin" in text
    ):

        return "✅ Handbagage inbegrepen"


    return "⚠️ Handbagage niet bevestigd"




def check_flights():

    best_deal = None


    dates = create_date_variations(
        DEPARTURE_DATE
    )


    for airport in DEPARTURE_AIRPORTS:


        for date in dates:


            data = search_flights(
                airport,
                date
            )


            flights = (
                data.get(
                    "best_flights",
                    []
                )
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



                if price_per_person > MAX_PRICE_PER_PERSON:
                    continue



                airline = (
                    flight["flights"][0]
                    .get(
                        "airline",
                        "Onbekend"
                    )
                )


                baggage = check_baggage(
                    flight
                )


                link = (
                    data
                    .get(
                        "search_metadata",
                        {}
                    )
                    .get(
                        "google_flights_url",
                        ""
                    )
                )



                deal = {

                    "found": True,

                    "route": (
                        f"{airport} → "
                        f"{ARRIVAL_AIRPORT}"
                    ),

                    "date": date,

                    "price": round(
                        price_per_person
                    ),

                    "total": total_price,

                    "airline": airline,

                    "baggage": baggage,

                    "link": link
                }



                if (
                    best_deal is None
                    or deal["price"] < best_deal["price"]
                ):

                    best_deal = deal




    if best_deal:

        return best_deal



    return {
        "found": False
    }
