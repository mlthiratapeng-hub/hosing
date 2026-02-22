require("dotenv").config();

const {
  Client,
  GatewayIntentBits,
  Partials,
  ActionRowBuilder,
  ButtonBuilder,
  ButtonStyle,
  ModalBuilder,
  TextInputBuilder,
  TextInputStyle,
  Events
} = require("discord.js");

// ===== CONFIG =====
const MASTER_TOKEN = process.env.MASTER_TOKEN;

const CHILD_TOKENS = [
  process.env.CHILD1,
  process.env.CHILD2,
  process.env.CHILD3,
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

// ===== MASTER =====
const master = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildVoiceStates
  ],
  partials: [Partials.Channel]
});

const childBots = [];

// ===== โหลดบอทลูก =====
for (const token of CHILD_TOKENS) {
  if (!token) continue;

  const bot = new Client({
    intents: [
      GatewayIntentBits.Guilds,
      GatewayIntentBits.GuildVoiceStates
    ]
  });

  bot.login(token)
    .then(() => console.log("Child logged in"))
    .catch(err => console.log("Child login error:", err.message));

  childBots.push(bot);
}

// ===== READY =====
master.on("ready", () => {
  console.log(`Master Online: ${master.user.tag}`);
});

// ===== MESSAGE =====
master.on("messageCreate", async (message) => {

  if (message.author.bot) return;

  // =========================
  // 🔊 !joic
  // =========================
  if (message.content === "!joic") {

    const voiceChannel = message.member?.voice?.channel;
    if (!voiceChannel) {
      return message.reply("❌ มึงต้องอยู่ห้องเสียงก่อนไอ้ควาย");
    }

    let joined = 0;

    for (const bot of childBots) {
      if (!bot.isReady()) continue;

      const guild = bot.guilds.cache.get(voiceChannel.guild.id);
      if (!guild) continue;

      try {
        joinVoiceChannel({
          channelId: voiceChannel.id,
          guildId: guild.id,
          adapterCreator: guild.voiceAdapterCreator,
          selfDeaf: false,
          selfMute: false
        });

        joined++;
      } catch (err) {}
    }

    return message.reply(` บอทเข้าห้องแล้ว ${joined} ตัว`);
  }

  // =========================
  // 📩 !vex
  // =========================
  if (!message.content.startsWith("!vex")) return;

  const args = message.content.split(" ");
  const targetId = args[1];
  const count = parseInt(args[2]);
  const text = args.slice(3).join(" ");

  if (!targetId || isNaN(count) || !text) {
    return message.reply("รูปแบบ: !vex <id> <จำนวน> <ข้อความ>");
  }

  if (targetId === BLOCKED_ID) {
    return message.reply("จะยิงกูทำอะไรไอควาย");
  }

  if (count > 99999999999999999999999999) {
    return message.reply("จำกัดไม่เกิน 99999999999999999999999999 ครั้ง");
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
        } catch {
          fail++;
        }
      }

    } catch {
      fail += count;
    }
  });

  await Promise.all(tasks);

  message.reply(
    `📊 สรุปผลบอท\n` +
    `👥 บอททั้งหมดที่เป็นตัวยิง: ${childBots.length}\n` +
    `✅ ยิงติด: ${success}\n` +
    `❌ ยิงไม่ติด: ${fail}`
     );

// =============================
// Interaction
// =============================
master.on(Events.InteractionCreate, async (interaction) => {

    if (interaction.isButton() && interaction.customId === 'open_modal') {

        const modal = new ModalBuilder()
            .setCustomId('send_modal')
            .setTitle('ส่งข้อความ');

        const textInput = new TextInputBuilder()
            .setCustomId('msg_input')
            .setLabel('ข้อความ')
            .setStyle(TextInputStyle.Paragraph)
            .setRequired(true);

        const countInput = new TextInputBuilder()
            .setCustomId('count_input')
            .setLabel('จำนวน (1-5)')
            .setStyle(TextInputStyle.Short)
            .setRequired(true);

        modal.addComponents(
            new ActionRowBuilder().addComponents(textInput),
            new ActionRowBuilder().addComponents(countInput)
        );

        await interaction.showModal(modal);
    }

    if (interaction.isModalSubmit() && interaction.customId === 'send_modal') {

        const text = interaction.fields.getTextInputValue('msg_input');
        let count = parseInt(
            interaction.fields.getTextInputValue('count_input')
        );

        if (isNaN(count) || count < 1) count = 1;
        if (count > 5) count = 5;

        await interaction.reply({
            content: 'กำลังส่ง...',
            ephemeral: true
        });

        for (let i = 0; i < count; i++) {
            await interaction.channel.send(text);
        }
    }
});

// =============================
// LOGIN
// =============================
master.login(MASTER_TOKEN);