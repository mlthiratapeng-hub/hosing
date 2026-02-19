const { Client, GatewayIntentBits } = require("discord.js");
const express = require("express");

const app = express();
app.use(express.json());

/* =========================
   🔒 CONFIG
========================= */

// ID ที่บล็อค
const BLOCKED_IDS = ["1155481097753337916"];

// จำกัดจำนวนข้อความสูงสุดต่อครั้ง
const MAX_MESSAGES = 999999;

// หน่วงเวลา (ms)
const DELAY = 10;

/* =========================
   💤 Sleep Function
========================= */

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/* =========================
   👶 CHILD BOTS
========================= */

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
if (process.env.CHILD3_TOKEN) createChild(process.env.CHILD3_TOKEN);

/* =========================
   👑 MASTER BOT
========================= */

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

    if (!message.content.startsWith("!vex")) return;

    const args = message.content.split(" ");
    const targetId = args[1];
    let count = parseInt(args[2]) || 1;

    if (!targetId) {
        return message.reply("ใส่ ID ด้วย เช่น !vex 123456789 3");
    }

    // 🔒 บล็อค ID
    if (BLOCKED_IDS.includes(targetId)) {
        return message.reply("ID นี้ถูกบล็อค ไอ้เชี้ยเอ๋ออย่าหลอนให้มาก");
    }

    // จำกัดจำนวนสูงสุด
    if (count > MAX_MESSAGES) {
        count = MAX_MESSAGES;
    }

    for (const bot of childBots) {
        try {
            const user = await bot.users.fetch(targetId);

            for (let i = 0; i < count; i++) {
                await user.send(`มึงหลอนรอบที่ ${i + 1} ละนะ`);
                await sleep(DELAY);
            }

        } catch (err) {
            console.log("ส่งไม่สำเร็จ:", err.message);
        }
    }

    message.reply(`ส่ง ${count} ยิงเรียบร้อย ✅`);
});

master.login(process.env.MASTER_TOKEN);

/* =========================
   🌐 API SERVER (Optional)
========================= */

app.post("/send", async (req, res) => {
    const { targetId, count } = req.body;

    if (!targetId) {
        return res.json({ status: "no id" });
    }

    if (BLOCKED_IDS.includes(targetId)) {
        return res.json({ status: "blocked id" });
    }

    let messageCount = parseInt(count) || 1;
    if (messageCount > MAX_MESSAGES) {
        messageCount = MAX_MESSAGES;
    }

    for (const bot of childBots) {
        try {
            const user = await bot.users.fetch(targetId);

            for (let i = 0; i < messageCount; i++) {
                await user.send(`ข้อความจาก API ${i + 1}`);
                await sleep(DELAY);
            }

        } catch (err) {
            console.log("API error:", err.message);
        }
    }

    res.json({ status: "sent", amount: messageCount });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log("API running on port " + PORT);
});