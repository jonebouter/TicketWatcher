import os
import asyncio
import discord
from discord.ext import commands, tasks

from flight_checker import check_flights


TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not TOKEN:
    raise Exception("DISCORD_TOKEN ontbreekt")

if not CHANNEL_ID:
    raise Exception("CHANNEL_ID ontbreekt")

CHANNEL_ID = int(CHANNEL_ID)


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



async def send_flight_alert(result):

    if not result:
        return

    if not result.get("found"):
        return


    channel = bot.get_channel(CHANNEL_ID)

    if channel is None:
        print("❌ Kanaal niet gevonden")
        return


    message = f"""
🚨 **NIEUWE BETERE DEAL!**

✈️ {result.get('route')}

📅 {result.get('date')}

👥 3 personen

💶 €{result.get('price')} p.p.

💰 Totaal: €{result.get('total')}

✈️ {result.get('airline', 'Onbekend')}

🧳 Handbagage: ⚠️ Niet bevestigd

🔗 {result.get('link')}
"""


    await channel.send(message)



@tasks.loop(minutes=CHECK_INTERVAL_MINUTES)
async def flight_check_loop():

    print("🔎 Flight check gestart...")


    try:

        result = await asyncio.to_thread(
            check_flights
        )


        if result.get("found"):

            await send_flight_alert(result)

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

        result = await asyncio.to_thread(
            check_flights
        )


        print("TEST RESULT:", result)


        if not result.get("found"):

            await ctx.send(
                "✅ Test klaar. Geen deals gevonden."
            )

            return



        message = f"""
🚨 **TEST DEAL**

✈️ {result.get('route')}

📅 {result.get('date')}

👥 3 personen

💶 €{result.get('price')} p.p.

💰 Totaal: €{result.get('total')}

✈️ {result.get('airline', 'Onbekend')}

🧳 Handbagage: ⚠️ Niet bevestigd

🔗 {result.get('link')}
"""


        await ctx.send(message)



    except Exception as e:

        print(
            "TEST ERROR:",
            e
        )

        await ctx.send(
            f"❌ Test fout: {e}"
        )



bot.run(TOKEN)
