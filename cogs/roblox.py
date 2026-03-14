import discord
import random
import string
import asyncio

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def brute_force(target_password):
    while True:
        generated_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if generated_password == target_password:
            yield generated_password
            break
        else:
            continue

async def send_password(user, target_password):
    async for password in brute_force(target_password):
        await user.send(f"Correct Password Found: {password}")

@client.event
async def on_message(message):
    if message.content.startswith('/roblox'):
        await message.channel.send("Please mention a user with @username and provide the target password.")
        def check(m):
            return m.author == message.author and m.content.startswith('@')
        try:
            mention_msg = await client.wait_for('message', timeout=30.0, check=check)
            mentioned_user = mention_msg.mentions[0]
            await message.channel.send("Please enter the target password:")
            password_msg = await client.wait_for('message', timeout=30.0, check=lambda m: m.author == message.author)
            target_password = password_msg.content
            await message.channel.send(f"Starting brute force for {mentioned_user.name} with target password: {target_password}...")
            await send_password(mentioned_user, target_password)
        except asyncio.TimeoutError:
            await message.channel.send("Timed out waiting for user mention or password.")

async def setup(bot):
    await bot.add_cog(RobloxCog(bot))