import discord
from discord.ext import commands
from discord import app_commands

class Rep(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="spam",
        description="ส่งข้อความ"
    )
    @app_commands.describe(
        message="ข้อความที่ต้องการส่ง",
        amount="จำนวนครั้ง"
    )
    async def rep(self, interaction: discord.Interaction, message: str, amount: int):

        if amount > 50:
            await interaction.response.send_message("จำนวนมากเกินไป (สูงสุด 50)", ephemeral=True)
            return

        await interaction.response.send_message("กำลังส่งข้อความ...", ephemeral=True)

        for i in range(amount):
            await interaction.channel.send(f"# {message}")

async def setup(bot):
    await bot.add_cog(Rep(bot))