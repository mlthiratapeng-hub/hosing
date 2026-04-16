import discord
from discord.ext import commands
import requests
import time

# ===== CONFIG =====
TOKEN = "DISCORD_TOKEN"
GEMINI_API_KEY = "GEMINI_API_KEY"

ALLOWED_CHANNEL = 1489678569960640824
ALLOWED_USER = 1127935823195668480

chat_enabled = False

# memory เก็บแชท
memory = []

# cooldown
last_used = {}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# ===== GEMINI FUNCTION =====
def ask_gemini(user_text, image_url=None):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    system_prompt = (
        "คุณคือผู้เชี่ยวชาญด้านโปรแกรมมิ่งขั้นเทพ "
        "อธิบายโค้ดเก่งมาก ฉลาด วิเคราะห์ลึก "
        "แต่พูดกันเอง กวนๆ นิดๆ คุยสนุกได้ "
        "สามารถนินทาเบาๆ แต่ไม่หยาบเกินไป"
    )

    # รวม memory ล่าสุด (5 ข้อความ)
    history_text = ""
    for m in memory[-5:]:
        history_text += f"{m}\n"

    parts = [
        {"text": system_prompt},
        {"text": f"บทสนทนาก่อนหน้า:\n{history_text}"},
        {"text": f"ผู้ใช้: {user_text}"}
    ]

    # รองรับรูป
    if image_url:
        try:
            img_data = requests.get(image_url).content
            parts.append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": img_data.hex()
                }
            })
        except:
            pass

    data = {
        "contents": [{
            "parts": parts
        }]
    }

    try:
        res = requests.post(url, json=data, timeout=10)
        return res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "บัค"

# ===== SLASH COMMAND =====
@bot.tree.command(name="st", description="เปิดระบบแชท")
async def start_chat(interaction: discord.Interaction):
    global chat_enabled

    if interaction.user.id != ALLOWED_USER:
        return await interaction.response.send_message("❌ ไม่มีสิทธิ์", ephemeral=True)

    if interaction.channel.id != ALLOWED_CHANNEL:
        return await interaction.response.send_message("❌ ใช้ได้เฉพาะห้องที่กำหนด", ephemeral=True)

    chat_enabled = True
    await interaction.response.send_message("✅ เปิดระบบแล้ว")

@bot.tree.command(name="off", description="ปิดระบบแชท")
async def stop_chat(interaction: discord.Interaction):
    global chat_enabled

    if interaction.user.id != ALLOWED_USER:
        return await interaction.response.send_message("❌ ไม่มีสิทธิ์", ephemeral=True)

    chat_enabled = False
    await interaction.response.send_message("🛑 ปิดระบบแล้ว")

# ===== MESSAGE =====
@bot.event
async def on_message(message):
    global chat_enabled

    if message.author.bot:
        return

    if message.channel.id != ALLOWED_CHANNEL:
        return

    if message.author.id != ALLOWED_USER:
        return

    if not chat_enabled:
        return

    # ===== กัน spam =====
    now = time.time()
    if message.author.id in last_used:
        if now - last_used[message.author.id] < 3:
            return
    last_used[message.author.id] = now

    # ===== จำกัดข้อความ =====
    if len(message.content) > 1000:
        return await message.reply("พิมพ์สั้นๆ หน่อย กูงง")

    await message.channel.typing()

    # ===== รูป =====
    image_url = None
    if message.attachments:
        image_url = message.attachments[0].url

    # ===== เรียก AI =====
    try:
        reply = ask_gemini(message.content, image_url)
    except:
        reply = "บัค"

    # ===== บันทึก memory =====
    memory.append(f"User: {message.content}")
    memory.append(f"AI: {reply}")

    # จำกัด memory
    if len(memory) > 20:
        memory.pop(0)

    # ===== EMBED =====
    embed = discord.Embed(
        title="4.8",
        description=reply,
        color=0x00ffcc
    )
    embed.set_footer(text="Gemini AI")

    await message.reply(embed=embed)

# ===== RUN =====
bot.run(TOKEN)