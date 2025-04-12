from flask import Flask, render_template, url_for, request, render_template_string
import qrcode
import qrcode.image.svg
from uuid import uuid4
import json
import httpx
import os
import re

app = Flask(__name__)
app.config['OHHOHO'] = str(uuid4())

factory = qrcode.image.svg.SvgImage
flag = "g0d{tha7s_r3al1y_a_5la5h_h1t!}"

@app.route("/")
def index():
    return render_template("index.html")

@app.errorhandler(Exception)
def notfound(e):
    return {"status": "fail", "msg": "这啥"}

@app.route("/qrcode")
def getip():
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        x_forward_ip = request.environ['HTTP_X_FORWARDED_FOR']
    else:
        x_forward_ip = "null"

    response_data = x_forward_ip
    response_data = render_template_string(response_data)
    if isinstance(x_forward_ip, str) and len(x_forward_ip)>10:
        return {"status": "fail", "msg": "I LOVE HEADER!"}
    
    return {"ip": request.remote_addr, "x-forward-for": response_data}

@app.route('/'+app.config['OHHOHO'])
def local_only():
    if request.remote_addr != "127.0.0.1":
        return {"status": "233", "msg": "卑鄙的外乡人..."}
    else:
        return flag

@app.route("/qrcode/generate", methods=['POST'])
def gen_qrcode():
    directory_path = "./static/generated"
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    if len(files) > 10:
        for file in files:
            file_path = os.path.join(directory_path, file)
            try:
                os.remove(file_path)
            except Exception as e:
                pass

    generated_code = str(uuid4())

    patterns = [
        (r"127\.", "不识数"),
        (r"0\.0", "不识数"),
        (r"host", "不认主"),
        (r"\[", "不认字"),
    ]
    for pattern, msg in patterns:
        if re.search(pattern, request.form.get('url')):
            return {"status": "fail", "msg": msg}

    data_to_be_packed = httpx.get(request.form.get('url')).text
    img = qrcode.make(data_to_be_packed[:30], image_factory=factory)
    img.save('./static/generated/'+generated_code+'.svg')
    return {"status": "succ", "file_name": generated_code}
