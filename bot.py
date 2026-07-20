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
