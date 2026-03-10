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
        return {"coins":{}, "roles":{}}

def save(data):

    with open(FILE,"w") as f:
        json.dump(data,f,indent=4)


def weighted_random(roles):

    total = sum(roles.values())
    r = random.uniform(0,total)

    upto = 0

    for role,weight in roles.items():

        if upto + weight >= r:
            return role

        upto += weight


class MysteryView(discord.ui.View):

    @discord.ui.button(label="ดูคอย",style=discord.ButtonStyle.gray)
    async def coin(self,interaction,button):

        data = load()

        user=str(interaction.user.id)

        coins=data["coins"].get(user,0)

        await interaction.response.send_message(
            f"คุณมี {coins} คอย",
            ephemeral=True
        )


    @discord.ui.button(label="สุ่มยศ",style=discord.ButtonStyle.blurple)
    async def roll(self,interaction,button):

        data=load()

        user=str(interaction.user.id)

        coins=data["coins"].get(user,0)

        cost=data.get("cost",50)

        if coins < cost:

            await interaction.response.send_message(
                "คอยไม่พอ",
                ephemeral=True
            )
            return

        role_id=weighted_random(data["roles"])

        role=interaction.guild.get_role(int(role_id))

        await interaction.user.add_roles(role)

        data["coins"][user]-=cost

        save(data)

        embed=discord.Embed(
            title="ผลการสุ่ม",
            description=f"คุณได้รับ {role.mention}",
            color=discord.Color.from_rgb(255,255,255)
        )

        await interaction.response.send_message(embed=embed)


class RoleSelect(discord.ui.Select):

    def __init__(self,guild):

        options=[]

        for role in guild.roles:

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
            options=options[:50]
        )


    async def callback(self,interaction):

        self.roles=self.values

        await interaction.response.send_modal(PercentModal(self.roles))


class PercentModal(discord.ui.Modal,title="ตั้ง % ยศ"):

    percent=discord.ui.TextInput(
        label="ใส่ % เช่น 50,30,20",
        placeholder="ต้องเท่าจำนวน role ที่เลือก"
    )

    cost=discord.ui.TextInput(
        label="คอยต่อการสุ่ม",
        placeholder="เช่น 50"
    )

    def __init__(self,roles):

        super().__init__()

        self.roles=roles


    async def on_submit(self,interaction):

        data=load()

        percents=self.percent.value.split(",")

        role_data={}

        for i,role in enumerate(self.roles):

            role_data[role]=int(percents[i])

        data["roles"]=role_data
        data["cost"]=int(self.cost.value)

        save(data)

        embed=discord.Embed(
            title="Mystery Box",
            description="สุ่มยศจากการใช้คอย",
            color=discord.Color.from_rgb(255,255,255)
        )

        embed.add_field(
            name="ค่าการสุ่ม",
            value=f"{data['cost']} คอย"
        )

        view=MysteryView()

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

        view=discord.ui.View()

        view.add_item(RoleSelect(interaction.guild))

        await interaction.response.send_message(
            "เลือก role",
            view=view,
            ephemeral=True
        )


async def setup(bot):

    await bot.add_cog(Mystery(bot))