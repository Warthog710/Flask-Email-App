import os
import psycopg2

class database:
    def __init__(self):
        self.__user = os.getenv('POSTGRESQL_USER')
        self.__password = os.getenv('POSTGRESQL_PASSWORD')
        self.__host = os.getenv('POSTGRESQL_HOST')
        self.__port = os.getenv('POSTGRESQL_PORT')
        self.__dbname = os.getenv('POSTGRESQL_DBNAME')
        self.__schema = os.getenv('POSTGRESQL_SCHEMA')

        try:
            self.__db = psycopg2.connect(f'postgres://{self.__user}:{self.__password}@{self.__host}:{self.__port}/{self.__dbname}')
            self.__connected = True
        except Exception as e:
            print(f'Failed to connect to database: {e}')
            self.__connected = False

    def __del__(self):
        if self.__connected:
            self.__db.close()

    def __exec(self, query, values):
        if self.__connected:
            handle = self.__db.cursor()
            handle.execute(query, values)

            results = handle.fetchall()
            handle.close()

            # Raise exception on None
            if results is None:
                raise Exception('No database entry found.')

            return results
        
        else:
            raise Exception('The database is not connected.')

    def __exec1(self, query, values):
        if self.__connected:
            handle = self.__db.cursor()
            handle.execute(query, values)

            results = handle.fetchone()
            handle.close()

            # Raise exception on None
            if results is None:
                raise Exception('No database entry found.')

            return results
        
        else:
            raise Exception('The database is not connected.')

    def __exec0(self, query, values):
        if self.__connected:
            handle = self.__db.cursor()
            handle.execute(query, values)
            self.__db.commit()
            handle.close()

        else:
            raise Exception('The database is not connected.')

    def save_image(self, image_id, image_type, image_data):
        query = f'INSERT INTO "{self.__schema}".images (image_id, image_type, image_data) VALUES (%s, %s, %s);'
        values = (image_id, image_type, image_data,)
        self.__exec0(query, values)

    def get_image(self, id): 
        query = f'SELECT image_type, image_data FROM "{self.__schema}".images WHERE image_id=%s'
        values = (id,)
        return self.__exec1(query, values)

    def create_user(self, user_id, first, last, username, password, is_active, is_super, is_admin):
        query = f'INSERT INTO "{self.__schema}".users (user_id, first_name, last_name, email, password, \
        is_active, is_superuser, is_admin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
        values = (user_id, first, last, username, password, is_active, is_super, is_admin,)
        return self.__exec0(query, values)

    def get_users_from_email(self, email):
        query = f'SELECT * FROM "{self.__schema}".users WHERE email=%s;'
        values = (email,)
        return self.__exec(query, values)

    def get_user_from_id(self, user_id):
        query = f'SELECT * FROM "{self.__schema}".users WHERE user_id=%s;'
        values = (user_id,)
        return self.__exec1(query, values)
        