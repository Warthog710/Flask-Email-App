from flask_login import UserMixin
from uuid_extensions import uuid7str
from bcrypt import hashpw, checkpw, gensalt

class FlaskUser(UserMixin):
    first_name = ''
    last_name = ''
    password = ''
    user_id = ''
    email = ''

    authenticated = False
    superuser = False
    active = False
    admin = False

    def __init__(self, db):
        self.__db = db

    def __setup_user(self, user_results):
        try:
            self.user_id = user_results[1]
            self.first_name = user_results[2]
            self.last_name = user_results[3]
            self.email = user_results[4]
            self.active = user_results[6]
            self.superuser = user_results[7]
            self.admin = user_results[8]
        except Exception as e:
            print(f'Failed to setup user: {e}')
        else:
            # Once setup, the user is authenticated
            self.authenticated = True

    def get_user_from_password(self, email, password):
        password = password.encode('utf-8')

        try:
            results = self.__db.get_users_from_email(email)
        except Exception as e:
            print(f'User not found with email {email}: {e}')
        else:
            for user in results:
                password_hash = bytes(user[5])

                if checkpw(password, password_hash):
                    return self.__setup_user(user)

            print('Unable to authenticate user...')

    def get_user_from_id(self, user_id):
        try:
            result = self.__db.get_user_from_id(user_id)
            self.__setup_user(result)
        except Exception:
            print(f'User not found with id {user_id}')

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return self.active

    def get_id(self):
        return self.user_id

class CreateFlaskUser:
    def __init__(self, db, form):
        user_id = uuid7str()
        first = form.first_name.data
        last = form.last_name.data
        email = form.email.data     

        # Hash password
        password_hash = hashpw(form.password.data.encode('utf-8'), gensalt())

        #? A user always starts as active
        is_active = True

        is_admin = form.is_admin.data
        is_super = form.is_super.data

        #? A superuser is always an admin
        if is_super:
            is_admin = True

        # Create User
        db.create_user(
            user_id,
            first,
            last,
            email,
            password_hash,
            is_active,
            is_super,
            is_admin
        )
