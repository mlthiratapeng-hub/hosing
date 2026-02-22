const { Client, GatewayIntentBits } = require("discord.js");
const axios = require("axios");

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.DirectMessages,
    GatewayIntentBits.MessageContent
  ],
});

client.once("ready", async () => {
  console.log(`Child ready: ${client.user.tag}`);

  if (!global.childBots) global.childBots = [];
  global.childBots.push(client);

  try {
    await axios.post("http://localhost:3000/register", {
      name: client.user.tag
    });
  } catch (err) {
    console.log("Register error:", err.message);
  }
});

client.login(process.env.CHILD1_TOKEN);

module.exports = client; // 👈 อันนี้สำคัญมากสำหรับ !all