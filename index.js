import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot Online: {bot.user}")

@bot.tree.command(name="awe", description="ประกาศข้อความไปหลายห้อง")
@app_commands.describe(
    message="ข้อความที่จะประกาศ",
    amount="จำนวนห้อง (สูงสุด 3)"
)
async def awe(interaction: discord.Interaction, message: str, amount: int):

    if amount > 3:
        amount = 3
    if amount < 1:
        amount = 1

    sent = 0

    for channel in interaction.guild.text_channels:
        if sent >= amount:
            break

        try:
            await channel.send(f"📢 {message}")
            sent += 1
        except:
            pass

    await interaction.response.send_message(
        f"✅ ส่งประกาศไป {sent} ห้องแล้ว",
        ephemeral=True
    )

bot.run(TOKEN)