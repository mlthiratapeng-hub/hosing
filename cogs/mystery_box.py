import discord
from discord.ext import commands
from discord import app_commands
import json
import random

DATA_FILE = "config.json"

def load_data():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f,indent=4)

class RoleSelect(discord.ui.Select):

    def __init__(self,guild):

        options = []

        for role in guild.roles[:50]:
            options.append(
                discord.SelectOption(
                    label=role.name,
                    value=str(role.id)
                )
            )

        super().__init__(
            placeholder="เลือกยศที่จะสุ่ม",
            min_values=1,
            max_values=min(50,len(options)),
            options=options
        )

    async def callback(self,interaction:discord.Interaction):

        data = load_data()
        data["roles"] = self.values
        save_data(data)

        await interaction.response.send_modal(RateModal())


class RateModal(discord.ui.Modal,title="ตั้งค่าการสุ่ม"):

    coin_cost = discord.ui.TextInput(
        label="ใช้กี่คอยต่อการสุ่ม",
        placeholder="เช่น 50"
    )

    limit = discord.ui.TextInput(
        label="จำกัดจำนวนครั้งต่อคน",
        placeholder="เช่น 2 / 4 / 6 / ไม่จำกัด"
    )

    async def on_submit(self,interaction):

        data = load_data()

        data["cost"] = int(self.coin_cost.value)

        if self.limit.value.lower() == "ไม่จำกัด":
            data["limit"] = -1
        else:
            data["limit"] = int(self.limit.value)

        save_data(data)

        embed = discord.Embed(
            title="Mystery Box",
            description="ใช้คอยจากการออนห้องเสียงมาแลกสุ่มยศ",
            color=discord.Color.from_rgb(255,255,255)
        )

        embed.add_field(
            name="ค่าการสุ่ม",
            value=f"{data['cost']} คอย",
            inline=False
        )

        view = MysteryView()

        await interaction.response.send_message(
            "สร้างกล่องสุ่มเรียบร้อย",
            ephemeral=True
        )

        await interaction.channel.send(embed=embed,view=view)


class MysteryView(discord.ui.View):

    @discord.ui.button(label="รับคอย",style=discord.ButtonStyle.gray)
    async def claim(self,interaction,button):

        data = load_data()

        coins = data.get("coins",{}).get(str(interaction.user.id),0)

        await interaction.response.send_message(
            f"คุณมี {coins} คอย",
            ephemeral=True
        )


    @discord.ui.button(label="สุ่มยศ",style=discord.ButtonStyle.blurple)
    async def roll(self,interaction,button):

        data = load_data()

        user = str(interaction.user.id)

        coins = data.get("coins",{}).get(user,0)

        if coins < data["cost"]:
            await interaction.response.send_message(
                "คอยไม่พอ",
                ephemeral=True
            )
            return

        role_id = random.choice(data["roles"])
        role = interaction.guild.get_role(int(role_id))

        await interaction.user.add_roles(role)

        data["coins"][user] -= data["cost"]

        save_data(data)

        embed = discord.Embed(
            title="ผลการสุ่ม",
            description=f"คุณได้รับยศ {role.mention}",
            color=discord.Color.from_rgb(255,255,255)
        )

        await interaction.response.send_message(embed=embed)


class MysteryBox(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @app_commands.command(name="mystery_box")
    @app_commands.checks.has_permissions(administrator=True)

    async def mystery(self,interaction:discord.Interaction):

        view = discord.ui.View()

        view.add_item(RoleSelect(interaction.guild))

        await interaction.response.send_message(
            "เลือกยศที่ต้องการสุ่ม",
            view=view,
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(MysteryBox(bot))