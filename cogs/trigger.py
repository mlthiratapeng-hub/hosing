import discord
from discord.ext import commands
from discord import app_commands

class Trigger(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.triggers = {}

    @app_commands.command(name="send_message", description="ข้อความ")
    async def send_message(
        self,
        interaction: discord.Interaction,
        trigger: str,
        message: str,
        amount: int
    ):

        self.triggers[trigger.lower()] = (message, amount)

        embed = discord.Embed(
            title="สำเร็จ",
            description=f"""
Trigger: `{trigger}`
Message: `{message}`
Amount: `{amount}`
""",
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        msg = message.content.lower()

        for trigger, data in self.triggers.items():

            text, amount = data

            if trigger in msg:

                for _ in range(amount):
                    await message.channel.send(f"# {text}")

                break

async def setup(bot):
    await bot.add_cog(Trigger(bot))
