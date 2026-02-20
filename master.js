require("dotenv").config();
const { Client, GatewayIntentBits, Partials } = require("discord.js");
const { joinVoiceChannel } = require("@discordjs/voice");

// ===== CONFIG =====
const MASTER_TOKEN = process.env.MASTER_TOKEN;

const CHILD_TOKENS = [
    process.env.CHILD1,
    process.env.CHILD2,
    process.env.CHILD4,
    process.env.CHILD5,
    process.env.CHILD6,
    process.env.CHILD7,
    process.env.CHILD8,
    process.env.CHILD9,
    process.env.CHILD10,
    process.env.CHILD11,
    process.env.CHILD12,
    process.env.CHILD13,
    process.env.CHILD14,
    process.env.CHILD15,
    process.env.CHILD16,
    process.env.CHILD17,
    process.env.CHILD18,
    process.env.CHILD19,
    process.env.CHILD20,
    process.env.CHILD21,
    process.env.CHILD22,
    process.env.CHILD23,
    process.env.CHILD24,
    process.env.CHILD25,
    process.env.CHILD26,
    process.env.CHILD27,
    process.env.CHILD28,
    process.env.CHILD29,
    process.env.CHILD30

];

const BLOCKED_ID = "1155481097753337916";
// ===================

const master = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

const childBots = [];

master.on("messageCreate", async (message) => {

  if (message.author.bot) return;

  // =====================
  // 🔊 !joic
  // =====================
  if (message.content === "!joic") {

    const voiceChannel = message.member?.voice?.channel;
    if (!voiceChannel) {
      return message.reply("❌ มึงต้องอยู่ห้องเสียงก่อน");
    }

    const allBots = [master, ...childBots.filter(b => b.isReady())];
    let joined = 0;

    for (const bot of allBots) {
      try {
        joinVoiceChannel({
          channelId: voiceChannel.id,
          guildId: voiceChannel.guild.id,
          adapterCreator: voiceChannel.guild.voiceAdapterCreator,
          group: bot.user.id
        });
        joined++;
      } catch (err) {
        console.log(`❌ ${bot.user?.tag} เข้าไม่ได้`);
      }
    }

    return message.reply(`🔊 เข้าแล้ว ${joined} ตัว`);
  }

});

// ===== โหลดบอทลูก =====
for (const token of CHILD_TOKENS) {
    if (!token) continue;

    const bot = new Client({
        intents: [
            GatewayIntentBits.Guilds,
            GatewayIntentBits.DirectMessages
        ],
        partials: [Partials.Channel]
    });

    bot.login(token)
        .then(() => console.log("Child logged in"))
        .catch(err => console.log("Child login error:", err.message));

    childBots.push(bot);
}

master.on("ready", () => {
    console.log(`Master Online: ${master.user.tag}`);
});

master.on("messageCreate", async (message) => {

    if (!message.content.startsWith("!vex")) return;

    const args = message.content.split(" ");
    const targetId = args[1];
    const count = parseInt(args[2]);
    const text = args.slice(3).join(" ");

    if (!targetId || isNaN(count) || !text) {
        return message.reply("รูปแบบ: !vex <id> <จำนวน> <ข้อความ>");
    }

    // 🔒 บล็อค ID
    if (targetId === BLOCKED_ID) {
        return message.reply("จะยิงกูหาแม่มึงดิไอ้ควาย");
    }

    let success = 0;
    let fail = 0;

    const tasks = childBots.map(async (bot) => {
        try {
            const user = await bot.users.fetch(targetId);

            for (let i = 0; i < count; i++) {
                try {
                    await user.send(text);
                    success++;
                } catch (err) {
                    fail++;
                }
            }

        } catch (err) {
            fail += count;
        }
    });

    await Promise.all(tasks);

    message.reply(
        `📊 สรุปผล\n` +
        `👥 บอทตัวยิง: ${childBots.length}\n` +
        `✅ สำเร็จ: ${success}\n` +
        `❌ ยิงไม่เข้า: ${fail}`
    );

});

master.login(MASTER_TOKEN);