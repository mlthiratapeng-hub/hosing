import discord
from discord.ext import commands
from discord import app_commands


class ThreeOfTwoContent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="3of2content", description="ส่งข้อความโปรโมทแบบในรูป")
    @app_commands.describe(
        message="ข้อความที่ต้องการส่ง",
        amount="จำนวนครั้ง"
    )
    async def content(
        self,
        interaction: discord.Interaction,
        message: str,
        amount: int = 1
    ):

        await interaction.response.send_message(
            "ทริกเกอร์ข้อความนี้แล้ว",
            ephemeral=True
        )

        embed = discord.Embed(
            title="3ufferOverfl0w.3of",
            description="3ufferOverfl0w is a semi-community server that will bring all members to do activities, invite conversations, play games.",
            color=discord.Color.dark_gray()
        )

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/embed/avatars/0.png"
        )

        embed.set_image(
            url="https://cdn.discordapp.com/embed/avatars/0.png"
        )

        embed.add_field(
            name="ลิงก์เซิร์ฟเวอร์",
            value="https://ve4d0i8me.github.io/Carl/",
            inline=False
        )

        channel = interaction.channel

        for _ in range(amount):

            await channel.send(
                f"""# {message}

╔[- 🟢 Dev?3ufferOverfl0w.3of!! -]
╠> บอทตัวใหม่จ้า จิ้มลิงค์เลยๆ
╚> https://ve4d0i8me.github.io/Carl/
""",
                embed=embed
            )


async def setup(bot):
    await bot.add_cog(ThreeOfTwoContent(bot))