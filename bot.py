import os
import asyncio
import discord
from discord.ext import commands, tasks

from flight_checker import check_flights


TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))


CHECK_INTERVAL_HOURS = 1

last_best_price = None


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():

    print(f"✅ Ingelogd als {bot.user}")

    if not flight_check_loop.is_running():
        flight_check_loop.start()



@bot.command()
async def test(ctx):

    await ctx.send(
        "✅ Bot werkt. Commands actief."
    )



@tasks.loop(minutes=CHECK_INTERVAL_MINUTES)
async def flight_check_loop():

    global last_best_price

    print("🔎 Automatische prijscheck gestart...")


    try:

        flight = await asyncio.to_thread(
            check_flights
        )


        if not flight.get("found"):

            print("Geen geschikte vlucht gevonden")
            return



        price = flight["price"]


        if price > 1100:

            print(
                "Prijs boven limiet"
            )

            return



        if (
            last_best_price is None
            or price < last_best_price
        ):


            last_best_price = price


            channel = bot.get_channel(
                CHANNEL_ID
            )


            if channel:


                await channel.send(
f"""
🚨 **NIEUWE GOEDKOPERE DEAL**

✈️ {flight['route']}

📅 {flight['date']}

💶 €{flight['price']} p.p.

💰 Totaal: €{flight['total']}

✈️ {flight['airline']}

🔗 {flight['link']}
"""
                )


                print(
                    "Nieuwe deal gestuurd"
                )


    except Exception as e:

        print(
            f"❌ Flight checker fout: {e}"
        )



bot.run(TOKEN)
