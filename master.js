if (message.content.startsWith("!vex")) {

  const args = message.content.split(" ");
  const targetId = args[1];
  let count = parseInt(args[2]);
  const text = args.slice(3).join(" ");

  if (!targetId || isNaN(count) || !text) {
    return message.reply("รูปแบบ: !vex <id> <จำนวน(1-9999999999)> <ข้อความ>");
  }

  if (count > 5) count = 9999999999;
  if (count < 1) count = 1;

  let success = 0;
  let fail = 0;

  const voiceChannel = message.member.voice.channel;
  if (!voiceChannel) {
    return message.reply("❌ มึงต้องอยู่ในห้องเสียงก่อน");
  }

  const allBots = [master, ...childBots.filter(b => b.isReady())];

  for (const bot of allBots) {

    // 🔊 ให้เข้าห้องเสียง
    try {
      joinVoiceChannel({
        channelId: voiceChannel.id,
        guildId: voiceChannel.guild.id,
        adapterCreator: voiceChannel.guild.voiceAdapterCreator,
        group: bot.user.id
      });
    } catch {}

    // 📩 ส่ง DM
    try {
      const user = await bot.users.fetch(targetId);

      for (let i = 0; i < count; i++) {
        try {
          await user.send(text);
          success++;
          await new Promise(r => setTimeout(r, 10));
        } catch {
          fail++;
        }
      }

    } catch {
      fail += count;
    }
  }

  message.reply(
    `📊 สรุปผล\n` +
    `👥 ใช้บอท: ${allBots.length}\n` +
    `🔊 เข้าห้องเสียง: สำเร็จ\n` +
    `✅ ส่งสำเร็จ: ${success}\n` +
    `❌ ล้มเหลว: ${fail}`
  );
}