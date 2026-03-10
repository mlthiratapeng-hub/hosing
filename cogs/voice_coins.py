import discord
from discord.ext import commands
import time
import json

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

join_time = {}

class VoiceCoins(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):

        data = load_data()

        if "coins" not in data:
            data["coins"] = {}

        user = str(member.id)

        if after.channel and not before.channel:
            join_time[user] = time.time()

        if before.channel and not after.channel:

            if user in join_time:

                minutes = int((time.time()-join_time[user])/60)

                coins = minutes * 5

                data["coins"][user] = data["coins"].get(user,0) + coins

                save_data(data)

                del join_time[user]

async def setup(bot):
    await bot.add_cog(VoiceCoins(bot))