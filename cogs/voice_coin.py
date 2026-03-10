import discord
from discord.ext import commands
import json
import time

FILE="data.json"

join_time={}

def load():

    try:
        with open(FILE) as f:
            return json.load(f)
    except:
        return {"coins":{}}

def save(data):

    with open(FILE,"w") as f:
        json.dump(data,f,indent=4)


class VoiceCoin(commands.Cog):

    def __init__(self,bot):
        self.bot=bot


    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):

        if member.bot:
            return

        if after.channel and not before.channel:

            join_time[member.id]=time.time()

        if before.channel and not after.channel:

            if member.id in join_time:

                minutes=int((time.time()-join_time[member.id])/60)

                coins=minutes*5

                data=load()

                user=str(member.id)

                data["coins"][user]=data["coins"].get(user,0)+coins

                save(data)

                del join_time[member.id]


async def setup(bot):

    await bot.add_cog(VoiceCoin(bot))