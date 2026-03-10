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
openai.api_base = "https://openrouter.ai/api/v1"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ai_channels = set()

# ================= READY =================

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)}")
    except Exception as e:
        print(e)

    print(f"Bot online: {bot.user}")

# ================= SLASH COMMAND =================

@bot.tree.command(name="ching_ai", description="เปิด AI ในห้องนี้")
@app_commands.checks.has_permissions(administrator=True)
async def ching_ai(interaction: discord.Interaction):

    ai_channels.add(interaction.channel.id)

    await interaction.response.send_message(
        "AI เปิดในห้องนี้แล้ว พิมพ์คุยได้เยยย",
        ephemeral=True
    )

# ================= AI CHAT =================

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if message.channel.id not in ai_channels:
        return

    try:

        async with message.channel.typing():

            response = openai.ChatCompletion.create(
                model="deepseek/deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": "คุณคือผู้หญิงที่พูดเรียบๆ สุภาพ คุยเหมือนเพื่อน ไม่ใช้ emoji ตอบสั้น กระชับ และช่วยเรื่องโค้ดทุกอย่าง คุณไม่◌ูดที่ทำร้ายจิตใจ เเละคุณเป็นคนที่ตอบไวไม่ชอบให้คนอื่นต้องรอ"
                    },
                    {
                        "role": "user",
                        "content": message.content
                    }
                ],
                temperature=0.7,
                max_tokens=150
            )

        reply = response.choices[0].message.content

        await message.reply(reply)

    except Exception as e:
        await message.reply(f"AI error: {e}")

    await bot.process_commands(message)

bot.run(TOKEN)