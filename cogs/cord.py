import discord
from discord.ext import commands
from discord import app_commands
import io

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class CodeModal(discord.ui.Modal, title="สร้างไฟล์ code.py"):

    code = discord.ui.TextInput(
        label="พิมพ์โค้ดที่ต้องการ",
        style=discord.TextStyle.paragraph,
        placeholder="เช่น print('hello world')",
        required=True,
        max_length=2000
    )

    async def on_submit(self, interaction: discord.Interaction):
        file_content = self.code.value

        file = discord.File(
            fp=io.BytesIO(file_content.encode()),
            filename="code.py"
        )

        await interaction.response.send_message(
            content="📁 นี่คือไฟล์ code.py ของคุณ",
            file=file
        )

@bot.tree.command(name="code", description="สร้างไฟล์ code.py")
async def code(interaction: discord.Interaction):
    await interaction.response.send_modal(CodeModal())

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot online: {bot.user}")

bot.run("BOT_TOKEN")