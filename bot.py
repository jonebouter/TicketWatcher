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



@bot.command()
async def test(ctx):

    await ctx.send(
        "✅ Bot werkt. Discord verbinding en commands zijn actief."
    )



@bot.command()
async def best(ctx):

    await ctx.send(
        "🔎 Goedkoopste vlucht zoeken..."
    )

    try:

        result = await asyncio.to_thread(
            check_flights
        )


        # nieuwe flight_checker geeft 1 dict terug
        if not result.get("found"):

            await ctx.send(
                "❌ Geen geschikte vlucht gevonden."
            )

            return


        message = f"""
🏆 **GOEDKOOPSTE VLUCHT OP DIT MOMENT**

✈️ Route:
{result.get('route')}

📅 Datum:
{result.get('date')}

💶 Prijs:
€{result.get('price')} p.p.

💰 Totaal:
€{result.get('total')}

✈️ Maatschappij:
{result.get('airline')}

🔗 Link:
{result.get('link')}
"""

        await ctx.send(message)


    except Exception as e:

        await ctx.send(
            f"❌ Fout bij zoeken: {e}"
        )



@tasks.loop(minutes=CHECK_INTERVAL_MINUTES)
async def flight_check_loop():

    print("🔎 Automatische flight check gestart...")

    try:

        result = await asyncio.to_thread(
            check_flights
        )


        if result.get("found"):

            channel = bot.get_channel(
                CHANNEL_ID
            )

            if channel:

                await channel.send(
                    f"""
🚨 **NIEUWE DEAL GEVONDEN**

✈️ {result.get('route')}

📅 {result.get('date')}

💶 €{result.get('price')} p.p.

💰 Totaal: €{result.get('total')}

✈️ {result.get('airline')}

🔗 {result.get('link')}
"""
                )


    except Exception as e:

        print(
            f"❌ Flight checker fout: {e}"
        )



bot.run(TOKEN)
