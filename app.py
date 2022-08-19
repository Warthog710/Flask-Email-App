import os
import yagmail

from flask import Flask, render_template, request
from dotenv import load_dotenv
from Email import email

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        html = request.get_data().decode('utf-8')
        email().send_email(html)

    return render_template('editor.html')
