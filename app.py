import io
import base64

from flask import Flask, render_template, request, send_file
from Database import database
from Email import email

app = Flask(__name__)
db = database()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        html = request.get_data().decode('utf-8')
        email(db).send_email(html, request)

    return render_template('editor.html')

@app.route('/image/<string:id>')
def image(id):
    try:
        result = db.get_image(id)
        image_type = result[0].split('/', maxsplit=1)[1]
        image = io.BytesIO(base64.b64decode(result[1]))

        return send_file(
            image,
            mimetype=result[0],
            as_attachment=False,
            download_name=f'{id}.{image_type}'
        )

    except Exception as e:
        return str(e)
