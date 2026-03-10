import discord
from discord.ext import commands
from discord import app_commands
import openai
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

ai_channels = set()

async def load_cogs():
    await bot.load_extension("cogs.mystery_box")
    await bot.load_extension("cogs.voice_coin")

@bot.event
async def on_ready():

    await load_cogs()

    try:
        synced = await bot.tree.sync()
        print(f"Slash commands: {len(synced)}")
    except Exception as e:
        print(e)

    print(f"Bot online: {bot.user}")

@bot.tree.command(name="ching_ai")
@app_commands.checks.has_permissions(administrator=True)
async def ching_ai(interaction:discord.Interaction):

    ai_channels.add(interaction.channel.id)

    await interaction.response.send_message(
        "AI เปิดในห้องนี้แล้ว",
        ephemeral=True
    )

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if message.channel.id not in ai_channels:
        await bot.process_commands(message)
        return

    try:

        async with message.channel.typing():

            response = openai.ChatCompletion.create(
                model="deepseek/deepseek-chat",
                messages=[
                    {
                        "role":"system",
                        "content":"คุณคือผู้หญิงที่พูดเรียบๆ สุภาพ คุยเหมือนเพื่อน ไม่ใช้ emojiเด็ดขาด เป็นคนช่างคุยเเต่ก็ไม่ชอบให้ใครดูถูก"
                    },
                    {
                        "role":"user",
                        "content":message.content
                    }
                ],
                max_tokens=150
            )

        reply = response.choices[0].message.content

        await message.reply(reply)

    except Exception as e:

        await message.reply(f"AI error: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())