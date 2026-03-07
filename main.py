import discord
from discord.ext import commands
from discord import app_commands
import asyncio

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="announce", description="ส่งข้อความประกาศ")
@app_commands.describe(message="ข้อความ", amount="จำนวนครั้ง")
async def announce(interaction: discord.Interaction, message: str, amount: int):

    channel = interaction.channel
    await interaction.response.send_message("กำลังส่งข้อความ...", ephemeral=True)

    for i in range(amount):
        await channel.send(message)
        await asyncio.sleep(2)

bot.run("TOKEN")