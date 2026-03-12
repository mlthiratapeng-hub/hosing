import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import app_commands
import asyncio

class WebhookSpamView(View):
    def __init__(self, webhook_url, gif_url, max_spam):
        super().__init__()
        self.webhook_url = webhook_url
        self.gif_url = gif_url
        self.max_spam = max_spam
        self.is_spamming = False

    @discord.ui.button(label="Start Spam", style=discord.ButtonStyle.success)
    async def start_button(self, interaction: discord.Interaction, button: Button):
        if self.is_spamming:
            await interaction.response.send_message("Spamming is already in progress.", ephemeral=True)
            return

        self.is_spamming = True
        await interaction.response.send_message("Spamming started!", ephemeral=True)

        webhook = discord.SyncWebhook.from_url(self.webhook_url)
        for _ in range(self.max_spam):
            if not self.is_spamming:
                break
            webhook.send(embed=discord.Embed().set_image(url=self.gif_url))
            await asyncio.sleep(1)

        await interaction.followup.send(f"Spammed {self.max_spam} times!", ephemeral=True)

    @discord.ui.button(label="Stop Spam", style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: Button):
        if not self.is_spamming:
            await interaction.response.send_message("No spamming in progress.", ephemeral=True)
            return

        self.is_spamming = False
        await interaction.response.send_message("Spamming stopped!", ephemeral=True)

class WebhookCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="webhook", description="Spam a webhook")
    @app_commands.default_permissions(administrator=True)
    async def webhook_command(self, interaction: discord.Interaction, webhook_url: str, gif_url: str, max_spam: int):
        if max_spam > 9999999999:
            await interaction.response.send_message("Maximum spam count is 9999999999.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Webhook Spammer",
            description="This command allows you to spam a webhook. Enter the webhook URL, GIF URL, and the maximum number of times to spam.",
            color=0x000000
        )
        embed.set_footer(text="Use responsibly!")

        view = WebhookSpamView(webhook_url, gif_url, max_spam)
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(WebhookCog(bot))