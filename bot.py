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


CHECK_INTERVAL_MINUTES = 10


@bot.event
async def on_ready():
    print(f"✅ Ingelogd als {bot.user}")

    if not flight_check_loop.is_running():
        flight_check_loop.start()


async def send_flight_alerts(results):

    if not results:
        return

    channel = bot.get_channel(CHANNEL_ID)

    if channel is None:
        print("❌ Kanaal niet gevonden")
        return


    for flight in results:

        message = f"""
🚨 **NIEUWE BETERE DEAL!**

✈️ {flight.get('origin')} → {flight.get('destination')}

📅 {flight.get('date')}

👥 {flight.get('passengers', 3)} personen

💶 €{flight.get('price')} p.p.

💰 Totaal: €{flight.get('total_price')}

✈️ {flight.get('airline', 'Onbekend')}

🧳 {flight.get('baggage', 'Niet bevestigd')}

🔗 {flight.get('link')}
"""

        await channel.send(message)



@tasks.loop(minutes=CHECK_INTERVAL_MINUTES)
async def flight_check_loop():

    print("🔎 Flight check gestart...")

    try:

        results = await asyncio.to_thread(
            check_flights
        )

        if results:
            await send_flight_alerts(results)

        else:
            print("Geen nieuwe deals gevonden")


    except Exception as e:

        print(
            f"❌ Flight checker fout: {e}"
        )



@bot.command()
async def test(ctx):

    await ctx.send(
        "✈️ Flight checker test gestart..."
    )

    try:

        results = await asyncio.to_thread(
            check_flights
        )


        if not results:

            await ctx.send(
                "✅ Test klaar. Geen deals gevonden."
            )

            return


        for flight in results:

            message = f"""
🚨 **TEST DEAL**

✈️ {flight.get('origin')} → {flight.get('destination')}

📅 {flight.get('date')}

👥 {flight.get('passengers', 3)} personen

💶 €{flight.get('price')} p.p.

✈️ {flight.get('airline', 'Onbekend')}

🧳 {flight.get('baggage', 'Niet bevestigd')}

🔗 {flight.get('link')}
"""

            await ctx.send(message)


    except Exception as e:

        await ctx.send(
            f"❌ Test fout: {e}"
        )



bot.run(TOKEN)
