import os
import asyncio
import discord
from discord.ext import commands, tasks

from flight_checker import check_flights


TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


CHECK_INTERVAL_MINUTES = 15

last_best_price = None



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



@bot.command()
async def best(ctx):

    await ctx.send(
        "🔎 Zoek goedkoopste vlucht..."
    )

    try:

        flight = await asyncio.to_thread(
            check_flights
        )


        if not flight["found"]:

            await ctx.send(
                "❌ Geen vlucht gevonden."
            )

            return


        await ctx.send(
f"""
🏆 **GOEDKOOPSTE VLUCHT**

✈️ {flight['route']}

📅 {flight['date']}

💶 €{flight['price']} p.p.

💰 Totaal: €{flight['total']}

✈️ {flight['airline']}

🔗 {flight['link']}
"""
        )


    except Exception as e:

        await ctx.send(
            f"❌ Fout: {e}"
        )



@tasks.loop(minutes=CHECK_INTERVAL_MINUTES)
async def flight_check_loop():

    global last_best_price


    print("🔎 Automatische prijscheck...")


    try:

        flight = await asyncio.to_thread(
            check_flights
        )


        if not flight["found"]:
            return



        price = flight["price"]


        if price > 1100:
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


    except Exception as e:

        print(
            f"❌ Automatische check fout: {e}"
        )



bot.run(TOKEN)
