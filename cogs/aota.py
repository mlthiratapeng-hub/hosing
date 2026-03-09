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

        # ส่งข้อความหลัก
        main_msg = await interaction.channel.send(
            f"🚀 Trigger `{message}` x{amount}"
        )

        await interaction.response.defer(ephemeral=True)

        await asyncio.sleep(1)

        # ส่งข้อความแบบ reply ใต้ข้อความหลัก
        for i in range(amount):
            await interaction.channel.send(
                message,
                reference=main_msg
            )

async def setup(bot):
    await bot.add_cog(Aota(bot))