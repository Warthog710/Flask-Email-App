import io
import os
import base64

import flask_login
import flask

from Forms import LoginForm, CreateUserForm
from User import FlaskUser, CreateFlaskUser
from dotenv import load_dotenv
from Database import database
from Email import email

load_dotenv()

# Globals
login_manager = flask_login.LoginManager()
app = flask.Flask(__name__)
db = database()

# Init
app.secret_key = os.getenv('SECRET_KEY')
login_manager.login_view = 'login'
login_manager.init_app(app)

# Views
@login_manager.user_loader
def load_user(user_id):
    print(f'User Id: {user_id}')
    user = FlaskUser(db)
    user.get_user_from_id(user_id)
    return user

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm(flask.request.form)

    if flask.request.method == 'POST' and form.validate():
        user = FlaskUser(db)
        user.get_user_from_password(form.email.data, form.password.data)

        if user.is_authenticated:
            flask_login.login_user(user)

            #! Should check if the URL is safe for redirects
            next_page = flask.request.args.get('next')
            return flask.redirect(next_page or flask.url_for('index'))

        #? Bad login
        flask.flash('Email or password incorrect')

    return flask.render_template('login.html', form=form)

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.render_template('logout.html')

@app.route('/create_user', methods=['POST', 'GET'])
def create_user():
    form = CreateUserForm(flask.request.form)

    if flask.request.method == 'POST' and form.validate():
        CreateFlaskUser(db, form)
        return flask.redirect(flask.url_for('index'))

    return flask.render_template('createuser.html', form=form)

@app.route('/', methods=['POST', 'GET'])
@flask_login.login_required
def index():
    if flask.request.method == 'POST':
        html = flask.request.get_data().decode('utf-8')
        email(db).send_email(html, flask.request)

    return flask.render_template('editor.html')

@app.route('/image/<string:id>')
def image(id):
    try:
        result = db.get_image(id)
        image_type = result[0].split('/', maxsplit=1)[1]
        image = io.BytesIO(base64.b64decode(result[1]))

        return flask.send_file(
            image,
            mimetype=result[0],
            as_attachment=False,
            download_name=f'{id}.{image_type}'
        )

    except Exception as e:
        print(f'Failed to display image: {e}')
        return flask.abort(404)
