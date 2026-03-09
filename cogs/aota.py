import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Aota(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="aota", description="Trigger message")
    @app_commands.describe(
        message="ข้อความที่จะทริกเกอร์",
        amount="จำนวน (สูงสุด 3)"
    )
    async def aota(self, interaction: discord.Interaction, message: str, amount: int):

        if amount > 3:
            amount = 3
        if amount < 1:
            amount = 1

        # ข้อความสถานะ (เห็นแค่คนสั่ง)
        await interaction.response.send_message(
            f"🚀 กำลัง Trigger `{message}` x{amount}",
            ephemeral=True
        )

        await asyncio.sleep(1)

        # บอทตอบข้อความให้ทุกคนเห็น
        for i in range(amount):
            await interaction.channel.send(message)

async def setup(bot):
    await bot.add_cog(Aota(bot))