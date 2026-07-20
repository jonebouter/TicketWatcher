import os
import json
import discord
from discord.ext import commands, tasks
from flight_checker import check_flights

TOKEN = os.getenv("DISCORD_TOKEN")

CHANNEL_ID = 1528557273931055265

LAST_FILE = "last_flight.json"


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


def load_last():
    try:
        with open(LAST_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "price": 0,
            "link": ""
        }


def save_last(data):
    with open(LAST_FILE, "w") as f:
        json.dump(data, f)


@bot.event
async def on_ready():
    print(f"Bot online als {bot.user}")

    if not flight_check.is_running():
        flight_check.start()


@tasks.loop(minutes=15)
async def flight_check():

    result = check_flights()

    if not result["found"]:
        return

    last = load_last()

    if (
        last["price"] == result["price"]
        and last["link"] == result["link"]
    ):
        print("Geen nieuwe vlucht gevonden")
        return


    channel = bot.get_channel(CHANNEL_ID)

    if channel:
        await channel.send(
            f"✈️ **Nieuwe goedkope vlucht gevonden!**\n\n"
            f"🌍 Route: {result['route']}\n"
            f"✈️ Airline: {result['airline']}\n"
            f"📅 Vertrek: {result['date']}\n"
            f"💶 Prijs: €{result['price']}\n"
            f"🔗 Link: {result['link']}"
        )

    save_last({
        "price": result["price"],
        "link": result["link"]
    })


@bot.command()
async def test(ctx):
    await ctx.send("✈️ TicketWatcher werkt!")


bot.run(TOKEN)
