import discord
from discord.ext import commands
from discord import app_commands
import json
import random

FILE = "data.json"

def load():

    try:
        with open(FILE) as f:
            return json.load(f)
    except:
        return {"coins":{}, "roles":[], "cost":50, "limit":-1}

def save(data):

    with open(FILE,"w") as f:
        json.dump(data,f,indent=4)


class MysteryView(discord.ui.View):

    @discord.ui.button(label="รับคอย",style=discord.ButtonStyle.gray)
    async def claim(self,interaction,button):

        data = load()

        user = str(interaction.user.id)

        coins = data["coins"].get(user,0)

        await interaction.response.send_message(
            f"คุณมี {coins} คอย",
            ephemeral=True
        )


    @discord.ui.button(label="สุ่มยศ",style=discord.ButtonStyle.blurple)
    async def roll(self,interaction,button):

        data = load()

        user = str(interaction.user.id)

        coins = data["coins"].get(user,0)

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

        save(data)

        embed = discord.Embed(
            title="ผลการสุ่ม",
            description=f"คุณได้รับ {role.mention}",
            color=discord.Color.from_rgb(255,255,255)
        )

        await interaction.response.send_message(embed=embed)


class RoleSelect(discord.ui.Select):

    def __init__(self,guild):

        options=[]

        for role in guild.roles[:50]:

            options.append(
                discord.SelectOption(
                    label=role.name,
                    value=str(role.id)
                )
            )

        super().__init__(
            placeholder="เลือก role",
            min_values=1,
            max_values=min(50,len(options)),
            options=options
        )

    async def callback(self,interaction):

        data = load()

        data["roles"]=self.values

        save(data)

        await interaction.response.send_modal(CostModal())


class CostModal(discord.ui.Modal,title="ตั้งค่าคอย"):

    cost = discord.ui.TextInput(label="คอยต่อการสุ่ม")

    async def on_submit(self,interaction):

        data = load()

        data["cost"]=int(self.cost.value)

        save(data)

        embed = discord.Embed(
            title="Mystery Box",
            description="ใช้คอยจากการออน voice มาแลกสุ่มยศ",
            color=discord.Color.from_rgb(255,255,255)
        )

        embed.add_field(
            name="ราคาการสุ่ม",
            value=f"{data['cost']} คอย"
        )

        view = MysteryView()

        await interaction.response.send_message(
            "สร้างกล่องสุ่มแล้ว",
            ephemeral=True
        )

        await interaction.channel.send(embed=embed,view=view)


class Mystery(commands.Cog):

    def __init__(self,bot):
        self.bot=bot

    @app_commands.command(name="mystery_box")
    @app_commands.checks.has_permissions(administrator=True)

    async def mystery(self,interaction):

        view = discord.ui.View()

        view.add_item(RoleSelect(interaction.guild))

        await interaction.response.send_message(
            "เลือก role ที่จะสุ่ม",
            view=view,
            ephemeral=True
        )


async def setup(bot):

    await bot.add_cog(Mystery(bot))