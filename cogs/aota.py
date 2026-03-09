import discord
from discord.ext import commands
from discord import app_commands

class Aota(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="aota", description="Trigger message")
    @app_commands.describe(
        message="ข้อความที่ต้องการทริกเกอร์",
        amount="จำนวน (สูงสุด 3)"
    )
    async def aota(self, interaction: discord.Interaction, message: str, amount: int):

        if amount > 3:
            amount = 3
        if amount < 1:
            amount = 1

        # ตอบเฉพาะคนสั่ง
        await interaction.response.send_message(
            f"🚀 Triggering `{message}` x{amount}",
            ephemeral=True
        )

        channel = interaction.channel

        # ส่งข้อความจริงให้ทุกคนเห็น
        for i in range(amount):
            await channel.send(message)

async def setup(bot):
    await bot.add_cog(Aota(bot))