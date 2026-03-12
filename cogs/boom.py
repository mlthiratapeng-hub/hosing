import discord
from discord import Webhook, app_commands
from discord.ext import commands
import aiohttp
import asyncio

class boomCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="boom_webhook", description="Spam a webhook with messages")
    async def boom_webhook(self, interaction: discord.Interaction, webhook_url: str, count: int):
        """Spam a webhook with messages"""
        if count > 9999999:
            count = 9999999
        
        embed = discord.Embed(title="Webhook Spammer", description="กดเขียวเพื่อเริ่ม กดแดงเพื่อหยุด", color=discord.Color.green())
        
        class ControlButtons(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
                self.is_running = False
                self.message_count = 0
                
            @discord.ui.button(label="รันโปรเเกรม", style=discord.ButtonStyle.green)
            async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
                if self.is_running:
                    await interaction.response.send_message("กำลังสแปมอยู่แล้ว", ephemeral=True)
                    return
                    
                self.is_running = True
                await interaction.response.send_message("เริ่มสแปม webhook!", ephemeral=True)
                
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(webhook_url, session=session)
                    for i in range(count):
                        if not self.is_running:
                            break
                        try:
                            await webhook.send(f"@everyone  @here ファッキュファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキュファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューーファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューーファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューーファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューーファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューーファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューーファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューーファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューーファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューーファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューーファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューファッキューーファッキューファッキューファッキューファッキューファッキューファッキューファッキューファ")
                            self.message_count += 1
                            await asyncio.sleep(0.00000000000000000000000000000000001)
                        except Exception as e:
                            print(f"Error: {e}")
                            break
                            
                self.is_running = False
                await interaction.followup.send(f"สแปมเสร็จสิ้น! ส่งไปทั้งหมด {self.message_count} ข้อความ", ephemeral=True)
                            
            @discord.ui.button(label="หยุดโปรเเกรม", style=discord.ButtonStyle.red)
            async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
                if not self.is_running:
                    await interaction.response.send_message("ยังไม่ได้เริ่มสแปมอย่าโง่", ephemeral=True)
                    return
                    
                self.is_running = False
                await interaction.response.send_message("กำลังหยุดสแปมนะค่ะ", ephemeral=True)
        
        await interaction.response.send_message(embed=embed, view=ControlButtons())

async def setup(bot):
    await bot.add_cog(boomCog(bot))