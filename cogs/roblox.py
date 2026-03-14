import discord
from discord.ext import commands
import random
import string
import asyncio

class RobloxCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def brute_force(self, target_password):
        while True:
            generated_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            if generated_password == target_password:
                return generated_password
            await asyncio.sleep(0.01)  # Prevent overwhelming the CPU

    async def send_password(self, user, target_password):
        password = await self.brute_force(target_password)
        await user.send(f"Correct Password Found: {password}")

    @commands.command(name='roblox')
    async def roblox(self, ctx):
        await ctx.send("Please mention a user with @username and provide the target password.")
        
        def check_mention(m):
            return m.author == ctx.author and len(m.mentions) > 0

        try:
            mention_msg = await self.bot.wait_for('message', timeout=30.0, check=check_mention)
            mentioned_user = mention_msg.mentions[0]
            await ctx.send("Please enter the target password:")
            
            def check_password(m):
                return m.author == ctx.author

            password_msg = await self.bot.wait_for('message', timeout=30.0, check=check_password)
            target_password = password_msg.content
            await ctx.send(f"Starting brute force for {mentioned_user.name} with target password: {target_password}...")
            await self.send_password(mentioned_user, target_password)
        except asyncio.TimeoutError:
            await ctx.send("Timed out waiting for user mention or password.")

async def setup(bot):
    await bot.add_cog(RobloxCog(bot))