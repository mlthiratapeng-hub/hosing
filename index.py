import discord
from discord.ext import commands
from discord import app_commands
import openai
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ai_channels = set()

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot online: {bot.user}")

# เปิด AI ในห้อง
@bot.tree.command(name="ching_ai", description="เปิด AI ในห้องนี้")
@app_commands.checks.has_permissions(administrator=True)
async def ching_ai(interaction: discord.Interaction):

    ai_channels.add(interaction.channel.id)

    await interaction.response.send_message(
        "เปิด AI ในห้องนี้แล้ว พิมพ์คุยได้เลย 💬",
        ephemeral=True
    )

# ฟังข้อความ
@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if message.channel.id not in ai_channels:
        return

    try:

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are a friendly female Discord user.
                    Speak like a normal girl chatting with friends.
                    Be casual, fun, and helpful.
                    You can help with coding too.
                    Keep messages natural and not too long.
                    """
                },
                {
                    "role": "user",
                    "content": message.content
                }
            ]
        )

        reply = response["choices"][0]["message"]["content"]

        await message.reply(reply)

    except Exception as e:
        await message.reply(f"AI error: {e}")

    await bot.process_commands(message)

bot.run(TOKEN)