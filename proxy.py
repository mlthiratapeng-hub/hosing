import os
from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def proxy(path):
    # ส่งต่อ Request ไปที่ Discord โดยตรง
    target_url = f"https://discord.com/{path}"
    
    headers = dict(request.headers)
    headers.pop('Host', None) # ตัด Host ออกเพื่อไม่ให้ชนกับ Discord

    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            stream=True,
            timeout=30
        )
        # ตัด Header ที่ไม่จำเป็นออก
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        hdrs = [(n, v) for n, v in resp.raw.headers.items() if n.lower() not in excluded_headers]
        return Response(resp.iter_content(chunk_size=4096), status=resp.status_code, headers=hdrs)
    except Exception as e:
        return Response(f"Proxy Error: {str(e)}", status=500)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)