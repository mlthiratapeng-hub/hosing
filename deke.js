const { Client, GatewayIntentBits } = require('discord.js');
const express = require('express');

const app = express();
app.use(express.json());

const client = new Client({
    intents: [GatewayIntentBits.DirectMessages],
});

client.login(process.env.CHILD_TOKEN);

client.once('ready', () => {
    console.log(`Child logged in as ${client.user.tag}`);
});

// API รับคำสั่งจาก Master
app.post('/send-dm', async (req, res) => {
    const { userId, message } = req.body;

    try {
        const user = await client.users.fetch(userId);
        await user.send(message);
        res.json({ status: "sent" });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.listen(3000, () => {
    console.log("Child API running on port 3000");
});