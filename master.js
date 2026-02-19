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
const MAX_MESSAGES = 9999999999999999;

// หน่วงเวลาในแต่ละบอท (กัน rate limit)
const DELAY = 10;

/* =========================
   💤 Sleep
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

if (process.env.CHILD1_TOKEN) createChild(process.env.CHILD1_TOKEN);
if (process.env.CHILD2_TOKEN) createChild(process.env.CHILD2_TOKEN);
if (process.env.CHILD3_TOKEN) createChild(process.env.CHILD3_TOKEN);
if (process.env.CHILD4_TOKEN) createChild(process.env.CHILD4_TOKEN);
if (process.env.CHILD5_TOKEN) createChild(process.env.CHILD5_TOKEN);
if (process.env.CHILD6_TOKEN) createChild(process.env.CHILD6_TOKEN);
if (process.env.CHILD7_TOKEN) createChild(process.env.CHILD7_TOKEN);
if (process.env.CHILD8_TOKEN) createChild(process.env.CHILD8_TOKEN);
if (process.env.CHILD9_TOKEN) createChild(process.env.CHILD9_TOKEN);
if (process.env.CHILD10_TOKEN) createChild(process.env.CHILD10_TOKEN);
if (process.env.CHILD11_TOKEN) createChild(process.env.CHILD11_TOKEN);
if (process.env.CHILD12_TOKEN) createChild(process.env.CHILD12_TOKEN);
if (process.env.CHILD13_TOKEN) createChild(process.env.CHILD13_TOKEN);
if (process.env.CHILD14_TOKEN) createChild(process.env.CHILD14_TOKEN);
if (process.env.CHILD15_TOKEN) createChild(process.env.CHILD15_TOKEN);
if (process.env.CHILD16_TOKEN) createChild(process.env.CHILD16_TOKEN);
if (process.env.CHILD17_TOKEN) createChild(process.env.CHILD17_TOKEN);
if (process.env.CHILD18_TOKEN) createChild(process.env.CHILD18_TOKEN);
if (process.env.CHILD19_TOKEN) createChild(process.env.CHILD19_TOKEN);
if (process.env.CHILD20_TOKEN) createChild(process.env.CHILD20_TOKEN);

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
        return message.reply("ใส่ ID ด้วย เช่น !vex 123456789 2");
    }

    // 🔒 บล็อค ID
    if (BLOCKED_IDS.includes(targetId)) {
        return message.reply("มึงจะยิงกูหาพ่อมึงออไอ้หลอน");
    }

    // จำกัดจำนวน
    if (count > MAX_MESSAGES) {
        count = MAX_MESSAGES;
    }

    // 🚀 ส่งพร้อมกันระดับบอท
    const tasks = childBots.map(async (bot) => {
        try {
            const user = await bot.users.fetch(targetId);

            for (let i = 0; i < count; i++) {
                await user.send(`มึงหลอนรอบที่ ${i + 1} ละนะ จาก ${bot.user.username}`);
                await sleep(DELAY); // กัน rate limit
            }

        } catch (err) {
            console.log("Error:", err.message);
        }
    });

    await Promise.all(tasks);

    message.reply(`ส่ง ${count} ข้อความ จาก ${childBots.length} บอท เรียบร้อย ✅`);
});

master.login(process.env.MASTER_TOKEN);

/* =========================
   🌐 API (optional)
========================= */

app.post("/send", async (req, res) => {
    const { targetId } = req.body;

    if (!targetId) return res.json({ status: "no id" });
    if (BLOCKED_IDS.includes(targetId)) return res.json({ status: "blocked" });

    const tasks = childBots.map(async (bot) => {
        try {
            const user = await bot.users.fetch(targetId);
            await user.send("ข้อความจาก API");
        } catch (err) {
            console.log(err.message);
        }
    });

    await Promise.all(tasks);

    res.json({ status: "sent" });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log("API running on port " + PORT);
});