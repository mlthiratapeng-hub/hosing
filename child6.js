const { Client, GatewayIntentBits } = require("discord.js");
const axios = require("axios");

const client = new Client({
    intents: [GatewayIntentBits.Guilds, GatewayIntentBits.DirectMessages],
});

client.once("ready", async () => {
    console.log(`Child ready: ${client.user.tag}`);

    if (!global.childBots) global.childBots = [];
    global.childBots.push(client);

    await axios.post("http://localhost:3000/register", {
        name: client.user.tag
    });
});

client.login(process.env.CHILD7_TOKEN);