import discord
from discord.ext import commands
import sqlite3
import random

CARD_CHANNEL = 1483462143444521161
CHICKEN_CHANNEL = 1483462171630506097
HILO_CHANNEL = 1483462262344781960
SNOOKER_CHANNEL = 1483462337578143916

ADMIN = 1127935823195668480
ALLOWED = [1127935823195668480,1155481097753337916]

START_MONEY = 5000

class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect("casino.db")
        self.cursor = self.db.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            wallet INTEGER,
            bank INTEGER
        )
        """)
        self.db.commit()

    # ---------------- DB ----------------
    def get_user(self, user):
        self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user,))
        data = self.cursor.fetchone()

        if data is None:
            self.cursor.execute("INSERT INTO users VALUES(?,?,?)", (user, START_MONEY, 0))
            self.db.commit()
            return START_MONEY, 0

        return data[1], data[2]

    def add_wallet(self, user, amount):
        w, b = self.get_user(user)
        self.cursor.execute("UPDATE users SET wallet=? WHERE user_id=?", (w + amount, user))
        self.db.commit()

    def add_bank(self, user, amount):
        w, b = self.get_user(user)
        self.cursor.execute("UPDATE users SET bank=? WHERE user_id=?", (b + amount, user))
        self.db.commit()

    # ---------------- เช็คเงิน ----------------
    @commands.command(name="เช็คยอดเงิน")
    async def balance(self, ctx):
        w, b = self.get_user(ctx.author.id)

        embed = discord.Embed(title="ยอดเงิน", color=discord.Color.green())
        embed.add_field(name="เงินในตัว", value=w)
        embed.add_field(name="ธนาคาร", value=b)

        await ctx.send(embed=embed)

    # ---------------- ฝาก/ถอน ----------------
    @commands.command(name="ฝากเงิน")
    async def deposit(self, ctx, amount: int):
        w, b = self.get_user(ctx.author.id)

        if amount > w:
            return await ctx.send("เงินไม่พอ")

        self.add_wallet(ctx.author.id, -amount)
        self.add_bank(ctx.author.id, amount)

        await ctx.send("ฝากแล้ว")

    @commands.command(name="ถอนเงิน")
    async def withdraw(self, ctx, amount: int):
        w, b = self.get_user(ctx.author.id)

        if amount > b:
            return await ctx.send("เงินในธนาคารไม่พอ")

        self.add_bank(ctx.author.id, -amount)
        self.add_wallet(ctx.author.id, amount)

        await ctx.send("ถอนแล้ว")

    # ---------------- ให้เงิน ----------------
    @commands.command(name="ให้เงิน")
    async def give(self, ctx, member: discord.Member, amount: int):
        if ctx.author.id != ADMIN:
            return

        self.add_wallet(member.id, amount)
        await ctx.send(f"ให้เงิน {member.mention} {amount}")

    # ---------------- TOP ----------------
    @commands.command(name="top")
    async def top(self, ctx):
        self.cursor.execute("SELECT user_id,wallet FROM users ORDER BY wallet DESC")
        data = self.cursor.fetchall()

        embed = discord.Embed(title="อันดับเงิน", color=discord.Color.gold())

        desc = ""
        for i, (uid, money) in enumerate(data[:10], start=1):
            user = self.bot.get_user(uid)
            desc += f"{i}. {user} - {money}\n"

        embed.description = desc
        await ctx.send(embed=embed)

    # ---------------- ไพ่ (จั่ว/เปิด) ----------------
    @commands.command(name="ไพ่")
    async def card(self, ctx, bet: int):
        if ctx.channel.id != CARD_CHANNEL:
            return

        w, _ = self.get_user(ctx.author.id)
        if bet > w:
            return await ctx.send("เงินไม่พอ")

        player = random.randint(1, 13)
        bot = random.randint(1, 13)

        if player > bot:
            self.add_wallet(ctx.author.id, bet)
            result = "ชนะ x2"
        else:
            self.add_wallet(ctx.author.id, -bet)
            result = "แพ้"

        embed = discord.Embed(title="ไพ่")
        embed.add_field(name="คุณ", value=player)
        embed.add_field(name="บอท", value=bot)
        embed.add_field(name="ผล", value=result)

        await ctx.send(embed=embed)

    # ---------------- ตีไก่ ----------------
    @commands.command(name="ตีไก่")
    async def chicken(self, ctx, bet: int):
        if ctx.channel.id != CHICKEN_CHANNEL:
            return

        w, _ = self.get_user(ctx.author.id)
        if bet > w:
            return await ctx.send("เงินไม่พอ")

        if random.random() > 0.5:
            self.add_wallet(ctx.author.id, bet)
            result = "ชนะ x2"
        else:
            self.add_wallet(ctx.author.id, -bet)
            result = "แพ้"

        await ctx.send(result)

    # ---------------- ไฮโล (เลือกเลขจริง) ----------------
    @commands.command(name="ไฮโล")
    async def hilo(self, ctx, bet: int, guess: int):
        if ctx.channel.id != HILO_CHANNEL:
            return

        if guess < 1 or guess > 6:
            return await ctx.send("เลือก 1-6")

        w, _ = self.get_user(ctx.author.id)
        if bet > w:
            return await ctx.send("เงินไม่พอ")

        dice = random.randint(1, 6)

        if dice == guess:
            self.add_wallet(ctx.author.id, bet * 4)
            result = f"ออก {dice} ชนะ x5"
        else:
            self.add_wallet(ctx.author.id, -bet)
            result = f"ออก {dice} แพ้"

        await ctx.send(result)

    # ---------------- สนุ๊ก (5 ครั้ง) ----------------
    @commands.command(name="สนุ๊ก")
    async def snooker(self, ctx, bet: int):
        if ctx.channel.id != SNOOKER_CHANNEL:
            return

        w, _ = self.get_user(ctx.author.id)
        if bet > w:
            return await ctx.send("เงินไม่พอ")

        success = 0

        for _ in range(5):
            if random.random() > 0.45:
                success += 1
            else:
                break

        if success > 0:
            gain = int(bet * (1.2 * success))
            self.add_wallet(ctx.author.id, gain)
            await ctx.send(f"เข้า {success} ลูก ได้ {gain}")
        else:
            loss = bet // 3
            self.add_wallet(ctx.author.id, -loss)
            await ctx.send(f"พลาด เสีย {loss}")

    # ---------------- ขโมย ----------------
    @commands.command(name="ขโมย")
    async def steal(self, ctx, member: discord.Member):
        w, _ = self.get_user(member.id)

        if w < 10000:
            return await ctx.send("ขโมยไม่ได้")

        amount = w // 10

        self.add_wallet(member.id, -amount)
        self.add_wallet(ctx.author.id, amount)

        await ctx.send(f"ขโมยมา {amount}")

async def setup(bot):
    await bot.add_cog(Casino(bot))