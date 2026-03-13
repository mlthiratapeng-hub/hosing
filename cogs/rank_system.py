import discord
from discord.ext import commands
from discord import app_commands
import random
import time

from database.rank_db import load,save
from cogs.rank_views import RollView

class RankSystem(commands.Cog):

    def __init__(self,bot):

        self.bot = bot
        self.db = load()

        self.voice_join = {}


    # ---------------- VC TIME ----------------

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):

        if member.bot:
            return

        if after.channel:

            self.voice_join[member.id] = time.time()

        if before.channel and not after.channel:

            if member.id in self.voice_join:

                spent = time.time() - self.voice_join[member.id]

                user = str(member.id)

                if user not in self.db:

                    self.db[user] = {
                        "coin":0,
                        "vc":0,
                        "roll":0
                    }

                self.db[user]["vc"] += spent

                save(self.db)

                del self.voice_join[member.id]


    # ---------------- COIN ----------------

    def get_coin(self,user):

        user = str(user)

        if user not in self.db:

            self.db[user] = {"coin":0,"vc":0,"roll":0}

        return self.db[user]["coin"]


    # ---------------- CLAIM ----------------

    async def claim_coin(self,interaction):

        user = str(interaction.user.id)

        need = self.db["config"]["vc_need"]
        reward = self.db["config"]["vc_coin"]

        if self.db[user]["vc"] < need:

            await interaction.user.send("คอยของคุณไม่พอ")
            return

        self.db[user]["coin"] += reward
        self.db[user]["vc"] = 0

        save(self.db)

        await interaction.response.send_message(
            f"ได้รับ {reward} คอย",
            ephemeral=True
        )


    # ---------------- ROLL ----------------

    async def roll(self,interaction):

        user = str(interaction.user.id)

        config = self.db["config"]

        price = config["price"]

        if self.db[user]["coin"] < price:

            await interaction.user.send("คอยของคุณไม่พอ")
            return

        if config["limit"] != 0:

            if self.db[user]["roll"] >= config["limit"]:

                await interaction.response.send_message(
                    "คุณสุ่มครบจำนวนแล้ว",
                    ephemeral=True
                )
                return

        self.db[user]["coin"] -= price
        self.db[user]["roll"] += 1

        roles = config["roles"]
        rates = config["rates"]

        role = random.choices(roles,weights=rates)[0]

        guild_role = interaction.guild.get_role(role)

        await interaction.user.add_roles(guild_role)

        embed = discord.Embed(
            title="🎲 สุ่มยศสำเร็จ",
            description=f"คุณได้รับ {guild_role.mention}",
            color=0x000000
        )

        if config["gif"]:

            embed.set_image(url=config["gif"])

        save(self.db)

        await interaction.response.send_message(embed=embed)


    # ---------------- SETUP ----------------

    @app_commands.command(name="set_rank")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_rank(self,interaction:discord.Interaction):

        embed = discord.Embed(
            title="ตั้งค่าระบบสุ่มยศ",
            description="พิมพ์ข้อมูลลงแชต\nตัวอย่าง\nprice 10\nlimit 3\nvc 600\ncoin 20\ngif url",
            color=0x000000
        )

        await interaction.response.send_message(embed=embed)


    # ---------------- CREATE PANEL ----------------

    @app_commands.command(name="create_roll_panel")
    @app_commands.checks.has_permissions(administrator=True)
    async def create_roll_panel(self,interaction:discord.Interaction):

        embed = discord.Embed(
            title="สุ่มยศ",
            description="กดปุ่มด้านล่างเพื่อสุ่ม",
            color=0x000000
        )

        view = RollView(self)

        await interaction.channel.send(embed=embed,view=view)

        await interaction.response.send_message(
            "สร้างแล้ว",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(RankSystem(bot))