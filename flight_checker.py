import os

MAX_PRICE = 600

def check_flights():
    # Tijdelijke testdata
    flight = {
        "route": "AMS → CUR",
        "date": "14 augustus - 25 augustus",
        "price": 499,
        "link": "https://www.google.com/flights"
    }

    if flight["price"] <= MAX_PRICE:
        return {
            "found": True,
            "route": flight["route"],
            "date": flight["date"],
            "price": flight["price"],
            "link": flight["link"]
        }

    return {
        "found": False
    }
