import discord
from discord.ext import tasks
import os
import asyncio

from flight_checker import check_flights


TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))


intents = discord.Intents.default()

bot = discord.Client(
    intents=intents
)


sent_deals = set()


@bot.event
async def on_ready():
    print(f"Ingelogd als {bot.user}")

    if not flight_check.is_running():
        flight_check.start()


@tasks.loop(minutes=10)
async def flight_check():

    print("Flight check gestart...")

    try:

        # BELANGRIJK:
        # requests blijft werken zonder Discord te blokkeren
        results = await asyncio.to_thread(
            check_flights
        )


        if not results:
            print("Geen nieuwe deals")
            return


        channel = bot.get_channel(
            CHANNEL_ID
        )


        for flight in results:


            deal_id = (
                flight.get("origin"),
                flight.get("date"),
                flight.get("price")
            )


            # voorkomt dubbele meldingen
            if deal_id in sent_deals:
                continue


            sent_deals.add(deal_id)


            message = f"""
🚨 **NIEUWE BETERE DEAL!**

✈️ {flight.get('origin')} → {flight.get('destination')}

📅 Datum:
{flight.get('date')}

👥 Personen:
{flight.get('passengers', 3)}

💶 Prijs:
€{flight.get('price')} p.p.

💰 Totaal:
€{flight.get('total')}

✈️ Airline:
{flight.get('airline', 'Onbekend')}

🧳 Bagage:
{flight.get('baggage', '⚠️ Niet bevestigd')}

🔗 Link:
{flight.get('link')}
"""


            await channel.send(message)


    except Exception as e:

        print("Fout bij flight check:")
        print(e)



bot.run(TOKEN)
