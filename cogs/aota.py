import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Aota(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="aota", description="Trigger message")
    async def aota(self, interaction: discord.Interaction, message: str, amount: int):

        if amount > 9:
            amount = 9
        if amount < 1:
            amount = 1

        trigger_text = f"🚀 Trigger {amount} x{amount}"

        # เห็นแค่คุณ
        await interaction.response.send_message(
            trigger_text,
            ephemeral=True
        )

        await asyncio.sleep(1)

        # หลอกให้เหมือน reply
        for i in range(amount):
            await interaction.channel.send(
                f"@{self.bot.user.name} {trigger_text}\n{message}"
            )

async def setup(bot):
    await bot.add_cog(Aota(bot))