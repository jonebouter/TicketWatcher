import os

MAX_PRICE = 600

def check_flights():
    # Tijdelijke testvlucht
    # Later vervangen we dit gedeelte door een echte vlucht-API

    flight = {
        "route": "AMS → CUR",
        "date": "14 augustus - 25 augustus",
        "price": 499,
        "link": "https://www.google.com/travel/flights"
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
