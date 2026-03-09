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

        # ข้อความหลัก (เห็นแค่คุณ)
        await interaction.response.send_message(
            f"🚀 Trigger {amount} x{amount}",
            ephemeral=True
        )

        await asyncio.sleep(1)

        # ข้อความที่ reply ใต้ trigger (ก็เห็นแค่คุณ)
        for i in range(amount):
            await interaction.followup.send(
                message,
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Aota(bot))