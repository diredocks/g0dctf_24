from flask import Flask, render_template, url_for, request, render_template_string
import qrcode
import qrcode.image.svg
from uuid import uuid4
import json
import httpx
import os

app = Flask(__name__)
app.config['IWANT2PLAYWITHU'] = str(uuid4())

factory = qrcode.image.svg.SvgImage
flag = "g0d{tha7s_r3al1y_a_5la5h_h1t!}"

@app.route("/")
def index():
    return render_template("index.html")

@app.errorhandler(Exception)
def notfound(e):
    return {"status": "fail", "msg": "2yo0ng2s1mple"}

@app.route("/qrcode")
def getip():
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        x_forward_ip = request.environ['HTTP_X_FORWARDED_FOR']
    else:
        x_forward_ip = "null"
    #response_data = '''
    #    ip: {0}
    #    x-forward-ip: {1}
    #'''.format(request.remote_addr, x_forward_ip)
    response_data = x_forward_ip
    response_data = render_template_string(response_data)
    if isinstance(x_forward_ip, str) and len(x_forward_ip)>10:
        return {"status": "fail", "msg": "g0f0cky0urs31f"}
    #return render_template_string(response_data)
    return {"ip": request.remote_addr, "x-forward-for": response_data}

@app.route('/'+app.config['IWANT2PLAYWITHU'])
def local_only():
    if request.remote_addr != "127.0.0.1":
        return {"status": "fail", "msg": "loser, you have to be a local"}
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
    if "127." in request.form.get('url'):
        return {"status": "fail", "msg": "no number in url"}
    if "0.0" in request.form.get('url'):
        return {"status": "fail", "msg": "no number in url"}
    if "host" in request.form.get('url'):
        return {"status": "fail", "msg": "no localhost in url"}
    if '[' in request.form.get('url'):
        return {"status": "fail", "msg": "no ipv6 in url"}
    data_to_be_packed = httpx.get(request.form.get('url')).text
    img = qrcode.make(data_to_be_packed[:30], image_factory=factory)
    img.save('./static/generated/'+generated_code+'.svg')
    return {"status": "succ", "file_name": generated_code}
