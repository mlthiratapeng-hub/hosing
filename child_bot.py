import discord
from discord.ext import commands
import os

TOKEN = os.getenv("CHILD_TOKEN1")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"child online {bot.user}")

bot.run(TOKEN)