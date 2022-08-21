from wtforms import Form, StringField, PasswordField, BooleanField, validators

class LoginForm(Form):
    email = StringField('Email', [
        validators.Email(message='A valid email address is required'),
        validators.DataRequired()
    ])

    password = PasswordField('Password', [
        validators.DataRequired()
    ])

class CreateUserForm(Form):
    first_name = StringField('First Name', [
        validators.DataRequired()
    ])

    last_name = StringField('Last Name', [
        validators.DataRequired()
    ])

    email = StringField('Email', [
        validators.Email(message='A valid email address is required'),
        validators.DataRequired()
    ])

    password = PasswordField('Password', [
        validators.EqualTo('confirm'),
        validators.Length(min=6, max=72),
        validators.DataRequired()
    ])

    confirm = PasswordField('Repeat Password')
    is_admin = BooleanField('Admin')
    is_super = BooleanField('Superuser')
