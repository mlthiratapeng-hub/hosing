import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio

ALLOWED_USERS = [1127935823195668480, 1155481097753337916]

class VoiceTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_users = {}
        self.update_timer.start()

    # /v command
    @app_commands.command(name="v", description="ให้บอทเข้า voice")
    async def join_voice(self, interaction: discord.Interaction):

        if interaction.user.id not in ALLOWED_USERS:
            await interaction.response.send_message("คุณไม่มีสิทธิ์ใช้คำสั่งนี้", ephemeral=True)
            return

        if not interaction.user.voice:
            await interaction.response.send_message("คุณต้องอยู่ในห้องเสียงก่อน", ephemeral=True)
            return

        channel = interaction.user.voice.channel

        if interaction.guild.voice_client:
            await interaction.guild.voice_client.move_to(channel)
        else:
            await channel.connect()

        await interaction.response.send_message(f"บอทเข้า {channel.name} แล้ว")

    # ตรวจจับเข้าออก voice
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if member.bot:
            return

        loop = asyncio.get_event_loop()

        # เข้า voice
        if before.channel is None and after.channel is not None:
            self.voice_users[member.id] = loop.time()

        # ออก voice
        if before.channel is not None and after.channel is None:
            self.voice_users.pop(member.id, None)

    # อัปเดตเวลาทุก 5 วิ
    @tasks.loop(seconds=5)
    async def update_timer(self):

        if not self.voice_users:
            return

        loop = asyncio.get_event_loop()
        now = loop.time()

        total_time = 0

        for start in self.voice_users.values():
            total_time += int(now - start)

        avg_time = total_time // len(self.voice_users)

        minutes = avg_time // 60
        seconds = avg_time % 60

        for guild in self.bot.guilds:
            for channel in guild.voice_channels:

                try:
                    base = channel.name.split("|")[0].strip()
                    new_name = f"{base} | {minutes:02}:{seconds:02}"

                    if channel.name != new_name:
                        await channel.edit(name=new_name)

                except:
                    pass


async def setup(bot):
    await bot.add_cog(VoiceTime(bot))