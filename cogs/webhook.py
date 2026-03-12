import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import app_commands
import asyncio

class WebhookSpamView(View):
    def __init__(self, webhook_url):
        super().__init__()
        self.webhook_url = webhook_url

    @discord.ui.button(label="Spam Webhook", style=discord.ButtonStyle.danger)
    async def spam_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Enter the number of times to spam:", ephemeral=True)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await interaction.client.wait_for('message', timeout=30.0, check=check)
            spam_count = int(msg.content)
        except asyncio.TimeoutError:
            await interaction.followup.send("You took too long to respond.", ephemeral=True)
            return
        except ValueError:
            await interaction.followup.send("Invalid number.", ephemeral=True)
            return

        if spam_count <= 0:
            await interaction.followup.send("Number must be greater than 0.", ephemeral=True)
            return

        webhook = discord.SyncWebhook.from_url(self.webhook_url)
        for _ in range(spam_count):
            webhook.send("Spam message")

        await interaction.followup.send(f"Spammed {spam_count} times!", ephemeral=True)

class WebhookCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="webhook", description="Spam a webhook")
    async def webhook_command(self, interaction: discord.Interaction, webhook_url: str):
        embed = discord.Embed(
            title="Webhook Spammer",
            description="This command allows you to spam a webhook. Enter the webhook URL and press the button to start spamming.",
            color=0x000000
        )
        embed.set_footer(text="Use responsibly!")

        view = WebhookSpamView(webhook_url)
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(WebhookCog(bot))