import discord
from discord.ext import commands
from discord import app_commands, SelectOption, ButtonStyle
from discord.ui import Select, Button, View
import random
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

class RankSetupView(View):
    def __init__(self):
        super().__init__()
        self.ranks = []
        self.time_options = ["10 นาที", "20 นาที", "30 นาที", "1 ชั่วโมง"]
        self.coin_options = ["10 คอย", "20 คอย", "30 คอย", "40 คอย", "50 คอย", "100 คอย"]
        self.attempt_options = ["1 ครั้ง", "2 ครั้ง", "3 ครั้ง", "4 ครั้ง", "5 ครั้ง", "ไม่จำกัด"]
        self.selected_time = None
        self.selected_coins = None
        self.selected_attempts = None

    @discord.ui.select(
        placeholder="เลือกยศ",
        min_values=1,
        max_values=10,
        options=[
            SelectOption(label="ยศ A", value="rank_a"),
            SelectOption(label="ยศ B", value="rank_b"),
            SelectOption(label="ยศ C", value="rank_c"),
            SelectOption(label="ยศ D", value="rank_d"),
            SelectOption(label="ยศ E", value="rank_e"),
        ]
    )
    async def select_rank(self, interaction: discord.Interaction, select: Select):
        self.ranks = select.values
        await interaction.response.send_message("เลือกเวลาที่ต้องออนไลน์:", view=TimeSelectView(self))

class TimeSelectView(View):
    def __init__(self, parent_view: RankSetupView):
        super().__init__()
        self.parent_view = parent_view

    @discord.ui.select(
        placeholder="เลือกเวลา",
        options=[
            SelectOption(label="10 นาที", value="10"),
            SelectOption(label="20 นาที", value="20"),
            SelectOption(label="30 นาที", value="30"),
            SelectOption(label="1 ชั่วโมง", value="60"),
        ]
    )
    async def select_time(self, interaction: discord.Interaction, select: Select):
        self.parent_view.selected_time = select.values[0]
        await interaction.response.send_message("เลือกจำนวนคอยที่จะได้รับ:", view=CoinSelectView(self.parent_view))

class CoinSelectView(View):
    def __init__(self, parent_view: RankSetupView):
        super().__init__()
        self.parent_view = parent_view

    @discord.ui.select(
        placeholder="เลือกจำนวนคอย",
        options=[
            SelectOption(label="10 คอย", value="10"),
            SelectOption(label="20 คอย", value="20"),
            SelectOption(label="30 คอย", value="30"),
            SelectOption(label="40 คอย", value="40"),
            SelectOption(label="50 คอย", value="50"),
            SelectOption(label="100 คอย", value="100"),
        ]
    )
    async def select_coins(self, interaction: discord.Interaction, select: Select):
        self.parent_view.selected_coins = select.values[0]
        await interaction.response.send_message("เลือกจำนวนครั้งที่สามารถสุ่มได้:", view=AttemptSelectView(self.parent_view))

class AttemptSelectView(View):
    def __init__(self, parent_view: RankSetupView):
        super().__init__()
        self.parent_view = parent_view

    @discord.ui.select(
        placeholder="เลือกจำนวนครั้ง",
        options=[
            SelectOption(label="1 ครั้ง", value="1"),
            SelectOption(label="2 ครั้ง", value="2"),
            SelectOption(label="3 ครั้ง", value="3"),
            SelectOption(label="4 ครั้ง", value="4"),
            SelectOption(label="5 ครั้ง", value="5"),
            SelectOption(label="ไม่จำกัด", value="0"),
        ]
    )
    async def select_attempts(self, interaction: discord.Interaction, select: Select):
        self.parent_view.selected_attempts = select.values[0]
        await interaction.response.send_message("การตั้งค่าสำเร็จ!", view=ConfirmView(self.parent_view))

class ConfirmView(View):
    def __init__(self, parent_view: RankSetupView):
        super().__init__()
        self.parent_view = parent_view

    @discord.ui.button(label="ยืนยันและสร้างการสุ่มยศ", style=ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(title="การสุ่มยศ", description="ยศที่จะสุ่มได้:", color=0x00ff00)
        for rank in self.parent_view.ranks:
            embed.add_field(name="ยศ", value=rank, inline=False)
        embed.add_field(name="เวลา", value=self.parent_view.selected_time, inline=False)
        embed.add_field(name="คอยที่จะได้รับ", value=self.parent_view.selected_coins, inline=False)
        embed.add_field(name="จำนวนครั้งที่สามารถสุ่มได้", value=self.parent_view.selected_attempts, inline=False)
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="set_rank")
@app_commands.checks.has_permissions(administrator=True)
async def set_rank(interaction: discord.Interaction):
    await interaction.response.send_message("เลือกยศที่จะสุ่ม:", view=RankSetupView())

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)}")
    except Exception as e:
        print(e)
    print(f"Bot online: {bot.user}")

async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())
