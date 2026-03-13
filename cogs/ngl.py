import discord
from discord.ext import commands
from discord import app_commands
import requests
import asyncio

ngl_api_url = "https://ngl.link/api/submit"

class NglCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ngl", description="สเเปมngl")
    @app_commands.describe(username="The NGL username to send the message to", 
                          message="The message to send", 
                          count="Number of messages to send (max 50)")
    async def ngl(self, interaction: discord.Interaction, username: str, message: str, count: int):
        if count > 50:
            await interaction.response.send_message("Maximum number of messages is 50.", ephemeral=True)
            return

        embed = discord.Embed(title="NGL Message Sender", 
                            description=f"Send {count} messages to {username}?", 
                            color=discord.Color.blue())
        embed.add_field(name="Message", value=message, inline=False)
        embed.add_field(name="Count", value=count, inline=False)
        view = NglConfirmationView(username, message, count)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class NglConfirmationView(discord.ui.View):
    def __init__(self, username, message, count):
        super().__init__()
        self.username = username
        self.message = message
        self.count = count
        self.is_running = False

    @discord.ui.button(label="เริ่มย◌ิง", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.is_running:
            await interaction.response.send_message("Already running.", ephemeral=True)
            return

        self.is_running = True
        await interaction.response.send_message("กำลังยิง", ephemeral=True)

        sent_count = 0
        for _ in range(self.count):
            if not self.is_running:
                break
                
            payload = {
                "username": self.username,
                "question": self.message,
                "deviceId": "discord-bot",
                "gameSlug": "",
                "referrer": ""
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            try:
                response = requests.post(ngl_api_url, data=payload, headers=headers)
                sent_count += 1
                await asyncio.sleep(1)  # To avoid rate limiting
            except Exception as e:
                print(f"Error sending message: {e}")

        await interaction.followup.send(f"Sent {sent_count} messages to {self.username}!", ephemeral=True)
        self.is_running = False

    @discord.ui.button(label="หยุด", style=discord.ButtonStyle.red)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.is_running:
            await interaction.response.send_message("Not running.", ephemeral=True)
            return

        self.is_running = False
        await interaction.response.send_message("Stopped sending messages.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(NglCog(bot))