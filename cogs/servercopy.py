import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import aiohttp

class ServerCopy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @app_commands.command(name="copy", description="คัดลอกเซิร์ฟเวอร์จาก Token ผู้ใช้")
    @app_commands.describe(
        source_token="User Token ของเซิร์ฟต้นทาง",
        source_guild_id="ID ของเซิร์ฟต้นทาง",
        target_guild_id="ID ของเซิร์ฟปลายทาง"
    )
    async def copy_server(self, interaction: discord.Interaction, source_token: str, source_guild_id: str, target_guild_id: str):
        await interaction.response.defer(ephemeral=True)

        # สร้าง client สำหรับเซิร์ฟต้นทางและปลายทาง
        source_client = discord.Client(intents=discord.Intents.all())
        target_client = discord.Client(intents=discord.Intents.all())

        try:
            await source_client.login(source_token)
        except discord.LoginFailure:
            await interaction.followup.send("ไม่สามารถเข้าสู่ระบบด้วย User Token ที่ให้มาได้", ephemeral=True)
            return

        try:
            await source_client.connect()
            await target_client.connect()

            # ดึงข้อมูลเซิร์ฟเวอร์
            source_guild = source_client.get_guild(int(source_guild_id))
            target_guild = target_client.get_guild(int(target_guild_id))

            if not source_guild or not target_guild:
                await interaction.followup.send("ไม่พบเซิร์ฟเวอร์ต้นทางหรือปลายทาง", ephemeral=True)
                return

            # คัดลอกองค์ประกอบต่างๆ
            await self.copy_categories(source_guild, target_guild)
            await self.copy_roles(source_guild, target_guild)
            await self.copy_channels(source_guild, target_guild)
            await self.copy_emojis(source_guild, target_guild)

            await interaction.followup.send("การคัดลอกเซิร์ฟเวอร์เสร็จสิ้น", ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"เกิดข้อผิดพลาด: {str(e)}", ephemeral=True)
        finally:
            await source_client.close()
            await target_client.close()

    async def copy_categories(self, source_guild, target_guild):
        for category in source_guild.categories:
            new_category = await target_guild.create_category(
                name=category.name,
                overwrites=category.overwrites,
                position=category.position
            )
            await self.copy_channels(category, new_category)

    async def copy_roles(self, source_guild, target_guild):
        # คัดลอก roles เรียงตามตำแหน่ง
        roles_to_copy = sorted(
            [role for role in source_guild.roles if role.name != "@everyone"],
            key=lambda r: r.position,
            reverse=True
        )
        
        for role in roles_to_copy:
            await target_guild.create_role(
                name=role.name,
                permissions=role.permissions,
                color=role.color,
                hoist=role.hoist,
                mentionable=role.mentionable
            )

    async def copy_channels(self, source_category, target_category):
        for channel in source_category.channels:
            if isinstance(channel, discord.TextChannel):
                await target_category.create_text_channel(
                    name=channel.name,
                    overwrites=channel.overwrites,
                    topic=channel.topic,
                    slowmode_delay=channel.slowmode_delay,
                    nsfw=channel.nsfw,
                    position=channel.position
                )
            elif isinstance(channel, discord.VoiceChannel):
                await target_category.create_voice_channel(
                    name=channel.name,
                    overwrites=channel.overwrites,
                    bitrate=channel.bitrate,
                    user_limit=channel.user_limit,
                    position=channel.position
                )

    async def copy_emojis(self, source_guild, target_guild):
        for emoji in source_guild.emojis:
            try:
                async with self.session.get(str(emoji.url)) as resp:
                    if resp.status == 200:
                        emoji_data = await resp.read()
                        await target_guild.create_custom_emoji(
                            name=emoji.name,
                            image=emoji_data
                        )
            except Exception as e:
                print(f"Failed to copy emoji {emoji.name}: {str(e)}")

async def setup(bot):
    await bot.add_cog(ServerCopy(bot))