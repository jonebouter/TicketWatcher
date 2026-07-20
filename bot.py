import os
import discord
from discord.ext import commands, tasks

from flight_checker import check_flights


TOKEN = os.getenv("DISCORD_TOKEN")

CHANNEL_ID = 1528557273931055265


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():

    print(f"Bot online als {bot.user}")

    if not flight_check.is_running():
        flight_check.start()



@tasks.loop(minutes=15)
async def flight_check():

    try:

        print("Vluchten controleren...")

        result = check_flights()


        if result["found"]:

            channel = bot.get_channel(CHANNEL_ID)


            if channel:

                await channel.send(
                    f"🚨 **TicketWatcher DEAL!**\n\n"
                    f"✈️ Route: {result['route']}\n"
                    f"📅 Datum: {result['date']}\n"
                    f"👥 Personen: 3\n\n"
                    f"💶 Prijs: €{result['price']} p.p.\n"
                    f"💰 Totaal: €{result['total']}\n\n"
                    f"✈️ Airline: {result['airline']}\n"
                    f"🧳 Handbagage: {result['baggage']}\n\n"
                    f"🔗 Google Flights:\n{result['link']}"
                )


    except Exception as e:

        print(
            f"Fout bij vluchtcontrole: {e}"
        )



@flight_check.before_loop
async def before_flight_check():

    await bot.wait_until_ready()



@bot.command()
async def test(ctx):

    await ctx.send(
        "✈️ TicketWatcher werkt!"
    )



@bot.command()
async def check(ctx):

    await ctx.send(
        "🔎 Handmatige vluchtcontrole gestart..."
    )

    result = check_flights()


    if result["found"]:

        await ctx.send(
            f"🚨 Deal gevonden!\n"
            f"{result['route']}\n"
            f"€{result['price']} p.p."
        )

    else:

        await ctx.send(
            "Geen deal gevonden."
        )



bot.run(TOKEN)
