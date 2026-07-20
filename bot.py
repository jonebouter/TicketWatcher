import os
import discord
from discord.ext import commands, tasks
from flight_checker import check_flights

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

CHANNEL_ID = 1528557273931055265 Hier komt straks je meldingskanaal ID


@bot.event
async def on_ready():
    print(f"Bot online als {bot.user}")
    flight_check.start()


@tasks.loop(hours=24)
async def flight_check():
    result = check_flights()

if result["found"]:
    channel = bot.get_channel(CHANNEL_ID)

    if channel:
        await channel.send(
            f"✈️ **Goedkope vlucht gevonden!**\n"
            f"🌍 Route: {result['route']}\n"
            f"📅 Datum: {result['date']}\n"
            f"💶 Prijs: €{result['price']} p.p."
        )
        
        


@bot.command()
async def test(ctx):
    await ctx.send("✈️ TicketWatcher werkt!")


bot.run(TOKEN)
