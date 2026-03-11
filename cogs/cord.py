import discord
from discord.ext import commands
import io

class CodeModal(discord.ui.Modal, title="สร้างไฟล์ code.py"):

    code = discord.ui.TextInput(
        label="พิมพ์โค้ดที่ต้องการ",
        style=discord.TextStyle.paragraph,
        placeholder="เช่น print('Hello World')",
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
            "📁 ดาวน์โหลดไฟล์ได้ด้านล่าง",
            file=file
        )


class Code(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="code", description="สร้างไฟล์ code.py")
    async def code(self, interaction: discord.Interaction):
        await interaction.response.send_modal(CodeModal())


async def setup(bot):
    await bot.add_cog(Code(bot))