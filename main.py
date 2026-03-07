import discord
from discord.ext import commands
from discord import app_commands

TOKEN = "TOKEN"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Main bot online: {bot.user}")

@bot.tree.command(name="aaa", description="ปิ้ว")
@app_commands.describe(
    message="ข้อความที่จะส่ง",
    amount="จำนวนครั้ง",
    channel1="ห้องที่ 1",
    channel2="ห้องที่ 2",
    channel3="ห้องที่ 3"
)
async def aaa(
    interaction: discord.Interaction,
    message: str,
    amount: int,
    channel1: discord.TextChannel,
    channel2: discord.TextChannel = None,
    channel3: discord.TextChannel = None
):

    channels = [c.id for c in [channel1, channel2, channel3] if c]

    trigger = f"TRIGGER|{message}|{amount}|{','.join(map(str, channels))}"

    await interaction.channel.send(trigger)

    await interaction.response.send_message("ส่ง trigger แล้ว", ephemeral=True)

bot.run(TOKEN)