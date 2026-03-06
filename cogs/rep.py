import discord
from discord.ext import commands
from discord import app_commands

class Rep(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="spam", description="ข้อความ")
    @app_commands.describe(
        message="ข้อความที่ต้องการส่ง",
        amount="จำนวนครั้ง"
    )
    async def rep(self, interaction: discord.Interaction, message: str, amount: int):

        if amount > 50:
            await interaction.response.send_message(
                "จำนวนสูงสุดคือ 50",
                ephemeral=True
            )
            return

        # ข้อความแบบในรูป
        await interaction.response.send_message(
            "ทริกเกอร์ข้อความนี้แล้ว"
        )

        for i in range(amount):
            await interaction.channel.send(f"# {message}")

async def setup(bot):
    await bot.add_cog(Rep(bot))