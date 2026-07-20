import os
import discord
from discord.ext import commands, tasks

from flight_checker import check_flights


TOKEN = os.getenv("DISCORD_TOKEN")

CHANNEL_ID = 1528557273931055265

PRICE_FILE = "last_deal.txt"


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


def get_last_price():

    try:
        with open(PRICE_FILE, "r") as file:
            return float(file.read())

    except:
        return 99999



def save_price(price):

    with open(PRICE_FILE, "w") as file:
        file.write(str(price))



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

            last_price = get_last_price()


            # alleen melden als hij goedkoper is
            if result["price"] < last_price:


                channel = bot.get_channel(CHANNEL_ID)


                if channel:

                    await channel.send(
                        f"🚨 **NIEUWE BETERE DEAL!**\n\n"
                        f"✈️ {result['route']}\n"
                        f"📅 {result['date']}\n"
                        f"👥 3 personen\n\n"
                        f"💶 €{result['price']} p.p.\n"
                        f"💰 Totaal: €{result['total']}\n\n"
                        f"✈️ {result['airline']}\n"
                        f"🧳 {result['baggage']}\n\n"
                        f"🔗 {result['link']}"
                    )


                save_price(result["price"])


    except Exception as e:

        print(
            f"Controle fout: {e}"
        )



@flight_check.before_loop
async def before_flight_check():

    await bot.wait_until_ready()



@bot.command()
async def test(ctx):

    await ctx.send(
        "✈️ TicketWatcher werkt!"
    )



bot.run(TOKEN)
