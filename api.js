const express = require("express");
const app = express();

app.use(express.json());

let clients = [];

app.post("/register", (req, res) => {
    clients.push(req.body.name);
    res.send("Registered");
});

app.post("/send", async (req, res) => {
    const { targetId } = req.body;

    global.childBots.forEach(async (bot) => {
        try {
            const user = await bot.users.fetch(targetId);
            user.send("@everyone @here อันนี้ดับมั้ย");
        } catch (err) {
            console.log("ส่งไม่สำเร็จ", err.message);
        }
    });

    res.send("Sent to children");
});

app.listen(3000, () => console.log("API Running"));
