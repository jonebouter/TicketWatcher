import os
import discord
from discord.ext import commands, tasks


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



@tasks.loop(minutes=CHECK_INTERVAL_MINUTES)
async def flight_check_loop():

    # Hier blijft later je echte checker draaien
    print("🔎 Flight checker interval actief")



@bot.command()
async def test(ctx):

    await ctx.send(
        "✅ Bot werkt! Discord verbinding is OK."
    )



bot.run(TOKEN)
