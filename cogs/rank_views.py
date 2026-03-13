import discord
import random

class RollView(discord.ui.View):

    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="🎲 สุ่มยศ", style=discord.ButtonStyle.secondary)
    async def roll(self, interaction: discord.Interaction, button: discord.ui.Button):

        await self.cog.roll(interaction)


    @discord.ui.button(label="💰 เช็คเงิน", style=discord.ButtonStyle.secondary)
    async def balance(self, interaction: discord.Interaction, button: discord.ui.Button):

        coins = self.cog.get_coin(interaction.user.id)

        embed = discord.Embed(
            title="ยอดเงิน",
            description=f"{coins} คอย",
            color=0x000000
        )

        await interaction.response.send_message(embed=embed,ephemeral=True)


    @discord.ui.button(label="🪙 รับคอย", style=discord.ButtonStyle.secondary)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):

        await self.cog.claim_coin(interaction)