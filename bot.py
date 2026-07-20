import discord
from discord.ext import tasks
import os

from flight_checker import check_flights


TOKEN = os.getenv("DISCORD_TOKEN")

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))


intents = discord.Intents.default()

bot = discord.Client(
    intents=intents
)


last_results = set()


@bot.event
async def on_ready():
    print(f"Ingelogd als {bot.user}")

    if not flight_check.is_running():
        flight_check.start()


@tasks.loop(minutes=10)
async def flight_check():

    print("Vluchten controleren...")

    try:
        results = await check_flights()

        if not results:
            print("Geen deals gevonden")
            return


        channel = bot.get_channel(CHANNEL_ID)

        for flight in results:

            flight_id = (
                flight["date"],
                flight["origin"],
                flight["price"]
            )


            # voorkomt spam
            if flight_id in last_results:
                continue


            last_results.add(flight_id)


            message = f"""
🚨 **NIEUWE BETERE DEAL!**

✈️ {flight['origin']} → {flight['destination']}

📅 Vertrek:
{flight['date']}

👥 Personen:
{flight['passengers']}

💶 Prijs:
€{flight['price']} p.p.

💰 Totaal:
€{flight['total']}

✈️ Airline:
{flight['airline']}

🧳 Bagage:
{flight['baggage']}

🔗 Link:
{flight['link']}
"""


            await channel.send(message)


    except Exception as e:
        print("Fout tijdens check:")
        print(e)



bot.run(TOKEN)
