require("dotenv").config();

const { Client, GatewayIntentBits } = require("discord.js");
const express = require("express");

const app = express();
app.use(express.json());

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

/* สร้าง child bots */
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

master.on("messageCreate", async (message) => {
    if (message.content.startsWith("!vex")) {
        const id = message.content.split(" ")[1];

        for (const bot of childBots) {
            try {
                const user = await bot.users.fetch(id);
                await user.send("@everyone @here อันนี้ดับมั้ย");
            } catch (err) {
                console.log("ส่งไม่สำเร็จ:", err.message);
            }
        }

        message.reply("ส่งคำสั่งไปบอทลูกแล้ว");
    }
});

master.login(process.env.MASTER_TOKEN);

/* ======================
   API SERVER
====================== */

app.post("/send", async (req, res) => {
    const { targetId } = req.body;

    for (const bot of childBots) {
        try {
            const user = await bot.users.fetch(targetId);
            await user.send("ข้อความจาก API");
        } catch (err) {
            console.log("API ส่งไม่สำเร็จ:", err.message);
        }
    }

    res.json({ status: "ok" });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log("API running on port " + PORT);
});