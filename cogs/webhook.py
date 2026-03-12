import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import app_commands
import asyncio
import aiohttp

class WebhookSpamView(View):
    def __init__(self, webhook_url, max_spam, message):
        super().__init__()
        self.webhook_url = webhook_url
        self.max_spam = max_spam
        self.message = message
        self.is_spamming = False

    @discord.ui.button(label="Start Spam", style=discord.ButtonStyle.success)
    async def start_button(self, interaction: discord.Interaction, button: Button):
        if self.is_spamming:
            await interaction.response.send_message("Spamming is already in progress.", ephemeral=True)
            return

        self.is_spamming = True
        await interaction.response.send_message("กำลังเริ่มสเเปม", ephemeral=True)

        async with aiohttp.ClientSession() as session:
            for i in range(self.max_spam):
                if not self.is_spamming:
                    break
                try:
                    async with session.post(self.webhook_url, json={"content": self.message}) as response:
                        if response.status != 204:
                            await interaction.followup.send("สเเปมสำเร็จ หรือ webhookผิด", ephemeral=True)
                            self.is_spamming = False
                            return
                except Exception as e:
                    await interaction.followup.send(f"Spamming failed: {str(e)}", ephemeral=True)
                    self.is_spamming = False
                    return

        await interaction.followup.send(f"Spammed {self.max_spam} times!", ephemeral=True)

    @discord.ui.button(label="Stop Spam", style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: Button):
        if not self.is_spamming:
            await interaction.response.send_message("หยุดเเล้ว", ephemeral=True)
            return

        self.is_spamming = False
        await interaction.response.send_message("หยุดโปรเเกรมเเล้ว", ephemeral=True)

class WebhookCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup_webhook", description="Setup webhook spam")
    @app_commands.default_permissions(administrator=True)
    async def setup_webhook_command(self, interaction: discord.Interaction, webhook_url: str, max_spam: int, message: str):
        if max_spam > 999999999999999999999999:
            await interaction.response.send_message("Maximum spam count is 999999999999999999999999.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Webhook Spammer",
            description="ใส่ลิ้งWebhook ตามด้วยจำนวนเเละคำ กดปุ่มเขียวเพื่อเริ่มโปรเเกรม เเดงเพื่อหยุดโปรเเกรม",
            color=0x000000
        )
        embed.set_footer(text="Use responsibly!")

        view = WebhookSpamView(webhook_url, max_spam, message)
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(WebhookCog(bot))