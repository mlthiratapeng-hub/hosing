import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

child_webhooks = [
    "WEBHOOK_URL_BOT1",
    "WEBHOOK_URL_BOT2"
]

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"online {bot.user}")

@bot.tree.command(name="aaa", description="ปิ้วว")
@app_commands.describe(
    message="ข้อความ",
    amount="จำนวนครั้ง",
    channel1="ห้องที่1",
    channel2="ห้องที่2",
    channel3="ห้องที่3"
)
async def aaa(
    interaction: discord.Interaction,
    message: str,
    amount: int,
    channel1: discord.TextChannel,
    channel2: discord.TextChannel = None,
    channel3: discord.TextChannel = None
):

    channels = [c for c in [channel1, channel2, channel3] if c]

    await interaction.response.send_message("กำลังส่ง...", ephemeral=True)

    for i in range(amount):

        for ch in channels:
            await ch.send(message)

        for webhook in child_webhooks:
            async with bot.session.post(webhook, json={"content": message}):
                pass

        await asyncio.sleep(2)

bot.run(TOKEN)