require("dotenv").config();

const { Client, GatewayIntentBits } = require("discord.js");
const express = require("express");

const app = express();
app.use(express.json());

/* ======================
   🚫 BLOCK SYSTEM
====================== */

// ID ที่ห้ามยิง
const BLOCKED_IDS = ["1155481097753337916"];

/* ======================
   CHILD BOTS
====================== */

const childBots = [];

function createChild(token) {
    const bot = new Client({
        intents: [
            GatewayIntentBits.Guilds,
            GatewayIntentBits.DirectMessages
        ]
    });

    bot.once("ready", () => {
        console.log(`Child Ready: ${bot.user.tag}`);
    });

    bot.login(token);
    childBots.push(bot);
}

// สร้าง child bots จาก ENV
if (process.env.CHILD1_TOKEN) createChild(process.env.CHILD1_TOKEN);
if (process.env.CHILD2_TOKEN) createChild(process.env.CHILD2_TOKEN);

/* ======================
   MASTER BOT
====================== */

const master = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

master.once("ready", () => {
    console.log(`Master Ready: ${master.user.tag}`);
});

master.on("messageCreate", async (message) => {
    if (message.author.bot) return;

    if (message.content.startsWith("!vex")) {
        const id = message.content.split(" ")[1];

        if (!id) {
            return message.reply("กรุณาใส่ ID ด้วย เช่น !vex 123456789");
        }

        // 🚫 เช็คบล็อคก่อนยิง
        if (BLOCKED_IDS.includes(id)) {
            return message.reply("ID นี้ถูกบล็อค ไม่สามารถส่งข้อความได้อีโง่ โง่ดักดาน อย่าหลอนให้มันมากนะมึงอะ");
        }

        for (const bot of childBots) {
            try {
                const user = await bot.users.fetch(id);
                await user.send("@everyone @here อันนี้ดับมั้ย");
            } catch (err) {
                console.log("ส่งไม่สำเร็จ:", err.message);
            }
        }

        message.reply("ส่งคำสั่งไปบอทลูกแล้ว ✅");
    }
});

master.login(process.env.MASTER_TOKEN);

/* ======================
   API SERVER
====================== */

app.post("/send", async (req, res) => {
    const { targetId } = req.body;

    if (!targetId) {
        return res.json({ status: "no id provided" });
    }

    // 🚫 บล็อคผ่าน API ด้วย
    if (BLOCKED_IDS.includes(targetId)) {
        return res.json({ status: "blocked id" });
    }

    for (const bot of childBots) {
        try {
            const user = await bot.users.fetch(targetId);
            await user.send("ข้อความจาก API ");
        } catch (err) {
            console.log("API ส่งไม่สำเร็จ:", err.message);
        }
    }

    res.json({ status: "sent" });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log("API running on port " + PORT);
});