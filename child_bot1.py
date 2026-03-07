import discord
from discord.ext import commands
import asyncio

TOKEN = "CHILD_TOKEN2"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Child bot online: {bot.user}")

@bot.event
async def on_message(message):

    if message.author.bot and message.content.startswith("TRIGGER|"):

        data = message.content.split("|")

        text = data[1]
        amount = int(data[2])
        channels = data[3].split(",")

        for i in range(amount):

            for cid in channels:

                ch = bot.get_channel(int(cid))

                if ch:
                    await ch.send(text)

            await asyncio.sleep(2)

bot.run(TOKEN)